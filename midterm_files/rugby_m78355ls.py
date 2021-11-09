import sys
#python3 rugby (student number).py [input file path] [output file path]

with open(sys.argv[1]) as inputFile:
    inputString = inputFile.read()

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
            score1 += 1
        else: score2 += 1

    prev = char

if score1 > score2:
    print("T1 wins!")
elif score1 < score2:
    print("T2 wins!")
else:
    print("Its a draw!")

outputString = str(score1)+":"+str(score2)
print(outputString)
with open(sys.argv[2],"w") as outputFile:
    outputFile.write(outputString)
