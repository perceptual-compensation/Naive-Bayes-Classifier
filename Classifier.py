import json
import numpy as np

with open("Results.json") as f:
    data = json.load(f)
with open("Sense counts.json") as f:
    senseCounts = json.load(f)
with open("Word senses.json") as f:
    wordSenses = json.load(f)

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
        for i in w:
            sentMatrix[np.array(s), i] += 1
    for i in paraWords:
        paraMatrix[np.array(list(paraSenses)), i] += 1
