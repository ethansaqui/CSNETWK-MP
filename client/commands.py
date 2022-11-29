def parseCommandString(commandString):
    if(not commandString): return None
    if(commandString[0] == '/'):
        word = ''
        for letter in commandString[1:]:
            if(letter == ' '):
                return word
            word += letter
        return word
    else:
        print("Invalid command! Start commands with a /")
    