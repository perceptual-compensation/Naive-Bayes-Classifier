import re
import json

paraMatch = re.compile("^<p ")
sentMatch = re.compile("^<s ")
wordMatch = re.compile("lemma=(.+?)[ >]")
senseMatch = re.compile("lexsn=(.+?)[ >]")

sentence = 0
data = []
senseCount = {}
wordSenses = {}

with open("All files", "rt") as inFile:
    lines = inFile.read().split("\n")

tblFile = open("Bag of words table", "wt")

for line in lines:
    if paraMatch.search(line):
        if data:
            data[-1][-1]["Words"] = list(data[-1][-1]["Words"])
            data[-1][-1]["Senses"] = list(data[-1][-1]["Senses"])
        data.append([])
    elif sentMatch.search(line):
        sentence += 1
        if data[-1]:
            data[-1][-1]["Words"] = list(data[-1][-1]["Words"])
            data[-1][-1]["Senses"] = list(data[-1][-1]["Senses"])
        data[-1].append({"Words" : set(), "Senses" : set()})
    elif wordMatch.search(line):
        word = wordMatch.search(line).groups()[0]
        senses = senseMatch.search(line).groups()[0].split(";")
        if not wordSenses.get(word):
            wordSenses[word] = {}
        data[-1][-1]["Words"].add(word)
        for sense in senses:
            if not senseCount.get(sense):
                senseCount[sense] = 0
            senseCount[sense] += 1
            if not wordSenses[word].get(sense):
                wordSenses[word][sense] = 0
            wordSenses[word][sense] += 1
            data[-1][-1]["Senses"].add(sense)
            tblFile.write("\t".join((str(len(data)), str(sentence), 
                    word, sense)) + "\n")

tblFile.close()

data[-1][-1]["Words"] = list(data[-1][-1]["Words"])
data[-1][-1]["Senses"] = list(data[-1][-1]["Senses"])

with open("Results.json", "wt") as f:
    f.write(json.dumps(data, sort_keys=True, indent=4))
with open("Word senses.json", "wt") as f:
    f.write(json.dumps(wordSenses, sort_keys=True, indent=4))
with open("Sense counts.json", "wt") as f:
    f.write(json.dumps(senseCount, sort_keys=True, indent=4))