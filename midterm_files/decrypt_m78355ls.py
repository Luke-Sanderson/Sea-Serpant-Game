import sys
import os
morseCodeChart = {'.-':'a','-...':'b','-.-.':'c','-..':'d','.':'e','..-.':'f','--.':'g','....':'h','..':'i','.---':'j','-.-':'k','.-..':'l','--':'m','-.':'n','---':'o','.--.':'p','--.-':'q','.-.':'r','...':'s','-':'t','..-':'u','...-':'v','.--':'w','-..-':'x','-.--':'y','--..':'z'}

def decryptMorse(str):
    output = ""
    morseArr = str[11:].split()
    for morse in morseArr:
        if morse == "/":
            output += " "
        else:
            output += morseCodeChart[morse]
    return output

def decryptCaesar(str):
    output = ""
    for char in str[18:]:
        if char != " ":
            output += chr(ord(char) - 3)
        else: output += " "
    return output

def decryptHex(str):
    output = ""
    hexArr = str[4:].split()
    for hex in hexArr:
        output += chr(int(hex,16))
    return output

def decrypt(inputString):
    if inputString[0] == "H":
        outputString = decryptHex(inputString)
    elif inputString[0] == "C":
        outputString = decryptCaesar(inputString)
    else:
        outputString = decryptMorse(inputString)

    return outputString.lower()

for root, dirs, files in os.walk(sys.argv[1]):
    for file in files:
        with open(root + file) as inputFile:
            outputString = decrypt(inputFile.read())

        with open(sys.argv[2]+file[:-4]+"_m78355ls.txt","w") as outputFile:
            outputFile.write(outputString)
