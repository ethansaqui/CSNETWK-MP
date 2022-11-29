import socket

def tokenizeCommandString(commandString):
    if(not commandString): return None
    if(commandString[0] == '/'):
        return commandString[1:].split(' ')
    else:
        print("Invalid command! Start commands with a /")   

def commandSwitch(command):
    action = command[0]
    parameters = command[1:]
    
    print(action)
    print(parameters)
    if command == "join":
        return
    if command == "leave":
        return
    if command == "msg":
        return
    if command == "register":
        return
    if command == "all":
        return
    if command == "?":
        return
