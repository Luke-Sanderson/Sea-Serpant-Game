import sys
morseCodeChart = {'.-':'a','-...':'b','-.-.':'c','-..':'d','.':'e','..-.':'f','--.':'g','....':'h','..':'i','.---':'j','-.-':'k','.-..':'l','--':'m','-.':'n','---':'o','.--.':'p','--.-':'q','.-.':'r','...':'s','-':'t','..-':'u','...-':'v','.--':'w','-..-':'x','-.--':'y','--..':'z'}
with open(sys.argv[1]) as inputFile:
    inputString = inputFile.read()

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

if inputString[0] == "H":
    outputString = decryptHex(inputString)
elif inputString[0] == "C":
    outputString = decryptCaesar(inputString)
else:
    outputString = decryptMorse(inputString)

print(outputString)
with open(sys.argv[2],"w") as outputFile:
    outputFile.write(outputString)
