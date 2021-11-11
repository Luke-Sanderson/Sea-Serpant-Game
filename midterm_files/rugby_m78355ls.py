import sys
import os
#python3 rugby (student number).py [input file path] [output file path]
def calcScore(inputString):
    score1 = 0
    score2 = 0

    for char in inputString:

        if char == 't':
            if prev == '1':
                score1 += 5
            else: score2 += 5
        if char == 'c':
            if prev == '1':
                score1 += 2
            else: score2 += 2
        if char == 'p':
            if prev == '1':
                score1 += 3
            else: score2 += 3
        if char == 'd':
            if prev == '1':
                score1 += 3
            else: score2 += 3

        prev = char

    if score1 > score2:
        print("T1 wins!")
    elif score1 < score2:
        print("T2 wins!")
    else:
        print("Its a draw!")

    outputString = str(score1)+":"+str(score2)
    print(outputString)

    return outputString


for root, dirs, files in os.walk(sys.argv[1]):
    for file in files:
        with open(os.path.join(root, file)) as inputFile:
            outputString = calcScore(inputFile.read())

        with open(os.path.join(sys.argv[2], file[:-4]+"_m78355ls.txt"),"w") as outputFile:
            outputFile.write(outputString)
