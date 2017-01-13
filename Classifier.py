import json
import numpy as np

with open("Results.json") as f:
    data = json.load(f)
with open("Sense counts.json") as f:
    senseCounts = json.load(f)
with open("Word senses.json") as f:
    wordSenses = json.load(f)

senseCountTotal = sum(senseCounts.values())
words = dict(zip(wordSenses.keys(), range(len(wordSenses.keys()))))
senses = dict(zip(senseCounts.keys(), range(len(senseCounts.keys()))))

sentMatrix = np.full((len(senses), len(words)), 0.1)
paraMatrix = np.full((len(senses), len(words)), 0.1)

for para in data:
    paraWords = set()
    paraSenses = set()
    for sentence in para:
        w = [words[i] for i in sentence["Words"]]
        s = [senses[i] for i in sentence["Senses"]]
        paraWords.update(w)
        paraSenses.update(s)
        sentMatrix[np.ix_(s, w)] += 1
    paraMatrix[np.ix_(list(paraSenses), list(paraWords))] += 1

paraMatrix = np.log(paraMatrix / paraMatrix.sum(axis=1)[:, None])
sentMatrix = np.log(sentMatrix / sentMatrix.sum(axis=1)[:, None])

# np.save("Paragraph matrix.npy", paraMatrix)
# np.save("Sentence matrix.npy", sentMatrix)

def classifier(targetWord, wordBag, source="paragraph", fullPosterior=False):
    targetSenses = wordSenses[targetWord]
    senseScores = {}
    for s in targetSenses.keys():
        senseScores[s] = np.log(wordSenses[targetWord][s] / sum(wordSenses[targetWord].values()))
        if source == "word":
            continue
        elif source == "sentence":
            conditionalProb = sentMatrix[senses[s]]
        else:
            conditionalProb = paraMatrix[senses[s]]
        senseScores[s] += np.sum(conditionalProb[[words[w] for w in wordBag if words.get(w)]])
    if not fullPosterior:
        return sorted(senseScores, key=senseScores.get)[-1]
    return senseScores

def batchClassifier(wordBag, source="paragraph"):
    posteriorSenses = []
    for word in wordBag:
        posteriorSenses.append(classifier(word, wordBag, source))
    return posteriorSenses
