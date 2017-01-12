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

paraMatrix /= paraMatrix.sum(axis=1)[:, None]
sentMatrix /= sentMatrix.sum(axis=1)[:, None]

np.save("Paragraph matrix.npy", paraMatrix)
np.save("Sentence matrix.npy", sentMatrix)

def classifier(targetWord, wordBag, source="paragraph"):
    targetSenses = wordSenses[targetWord]
    senseScores = {}
    for s in targetSenses.keys():
        if source == "word":
            senseScores[s] = wordSenses[targetWord][s]
            continue
        elif source == "sentence":
            conditionalProb = sentMatrix[senses[s]]
        else:
            conditionalProb = paraMatrix[senses[s]]
        posterior = senseCounts[s] / senseCountTotal
        for w in wordBag:
            
