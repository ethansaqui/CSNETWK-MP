import socket

class Commands:
    def __init__(self, address, port):
        self.address = address
        self.port = port
    
    def tokenizeCommandString(self, commandString):
        if(not commandString): return None
        if(commandString[0] == '/'):
            return commandString[1:].split(' ')
        else:
            print("Invalid command! Start commands with a /")   
        
    def checkParams(self, command, numParams, expectedParams):
        if numParams == expectedParams:
            return True
        print(f"Error: Expected {expectedParams} params for command [{command}], but {numParams} were given")
        return False

    def commandSwitch(self, command):
        action = command[0]
        parameters = command[1:]
        
        if action == "join":
            if(self.checkParams("join", len(parameters), 2)):
                self.joinCommand(parameters[0], parameters[1])
                
        if action == "leave":
            return
        
        if action == "msg":
            handle = command[1]
            message = ' '.join(command[2:])
            parameters = [handle, message]
            if(self.checkParams("msg", len(parameters), 2)):
                self.msgCommand(parameters[0], parameters[1])
                
        if action == "register":
            if(self.checkParams("register", len(parameters), 1)):
                return
            
        if action == "all":
            msg = ' '.join(command[1:])
            self.allCommand(msg)
            
        if action == "?":
            self.commandList()

        
    def joinCommand(self, address, port):
        return

    def msgCommand(self, handle, message):
        print(message)
        print(handle)

    def allCommand(self, msg):
        print(msg)
        return

    def commandList(self):
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
