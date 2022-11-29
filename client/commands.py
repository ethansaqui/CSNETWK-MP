import socket

def tokenizeCommandString(commandString):
    if(not commandString): return None
    if(commandString[0] == '/'):
        return commandString[1:].split(' ')
    else:
        print("Invalid command! Start commands with a /")   
    
def checkParams(command, numParams, expectedParams):
    if numParams == expectedParams:
        return True
    print(f"Error: Expected {expectedParams} params for command [{command}], but {numParams} were given")
    return False

def commandSwitch(command):
    action = command[0]
    parameters = command[1:]
    
    if action == "join":
        if(checkParams("join", len(parameters), 2)):
            join(parameters[0], parameters[1])
    if action == "leave":
        return
    if action == "msg":
        if(checkParams("msg", len(parameters), 2)):
            return
    if action == "register":
        if(checkParams("register", len(parameters), 1)):
            return
    if action == "all":
        if(checkParams("all", len(parameters), 1)):
            return
    if action == "?":
        commandList()

    
def join():
    return

def commandList():
    print("""+==========================+=============================================+======================+
|         Command          |                 Description                 |     Sample Usage     |
+==========================+=============================================+======================+
| /join <server_ip> <port> | Connect to a server with IP and Port        | /join 127.0.0.1 5000 |
+--------------------------+---------------------------------------------+----------------------+
| /leave                   | Disconnect from the current server          | /disconnect          |
+--------------------------+---------------------------------------------+----------------------+
| /register <handle>       | Register a unique handle or alias           | /register Milize     |
+--------------------------+---------------------------------------------+----------------------+
| /all <message>           | Send a message to all users                 | /all I have arrived! |
+--------------------------+---------------------------------------------+----------------------+
| /msg <handle> <message>  | Send a message to a specific user or handle | /msg Milize G valo?  |
+--------------------------+---------------------------------------------+----------------------+
| /?                       | Display this menu                           | /?                   |
+--------------------------+---------------------------------------------+----------------------+""")
