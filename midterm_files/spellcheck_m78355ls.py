import sys
import os
import re

upperChange = 0
puncChange = 0
numChange = 0
totalWord = 0
corrWord = 0
incorrWord = 0
def format(str):
    global upperChange
    global puncChange
    global numChange

    punctuation = ['.','?','!',',',':',';','-','‒','(',')','[',']','{','}',"'",'"','…']
    for char in str:
        if re.match("[a-z]",char) or char == " " or char == "\n":
            continue
        if(re.match("[A-Z]",char)):
            upperChange += 1
        elif(re.match("[0-9]",char)):
            numChange += 1
            str = str.replace(char,"",1)
        elif(char in punctuation):
            puncChange += 1
            str = str.replace(char,"",1)

        # else:
        #     puncChange += 1
        #     str = str.replace(char,"",1)

    str = str.lower()
    return str

def check(str):
    global totalWord
    global corrWord
    global incorrWord

    wordsToCheck = str.split()

    with open(sys.argv[1]) as dictionary:
        dictWords = dictionary.readlines()
        for word in wordsToCheck:
            found = False
            totalWord += 1
            for dictWord in dictWords:
                #print(word + " : " + dictWord)
                if dictWord.rstrip() == word:
                    found = True
                    break
            if found:
                corrWord += 1
            else:
                incorrWord += 1

for root, dirs, files in os.walk(sys.argv[2]):
    for file in files:
        upperChange = 0
        puncChange = 0
        numChange = 0
        totalWord = 0
        corrWord = 0
        incorrWord = 0
        with open(os.path.join(root, file)) as inputFile:
            formatted = format(inputFile.read())
            check(formatted)

        with open(os.path.join(sys.argv[3], file[:-4]+"_m78355ls.txt"),"w") as outputFile:
            outputFile.write("m78355ls\n")
            outputFile.write("Formatting ###################\n")
            outputFile.write("Number of upper case words changed: " + str(upperChange) + "\n")
            outputFile.write("Number of punctuations removed: " + str(puncChange) + "\n")
            outputFile.write("Number of numbers removed: " + str(numChange) + "\n")
            outputFile.write("Spellchecking ###################\n")
            outputFile.write("Number of words: " + str(totalWord) + "\n")
            outputFile.write("Number of correct words: " + str(corrWord) + "\n")
            outputFile.write("Number of incorrect words: " + str(incorrWord) + "\n")
