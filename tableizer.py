
tblFile = open("Bag of words table", "a")

with open("All files", "rt") as inFile:
    lines = inFile.read().split()

for line in lines:
    

tblFile.close()