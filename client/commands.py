import socket

class Commands:
    address = None
    port = None
    isConnected = False
    
    def __init__(self, client, bufferSize):
        self.bufferSize = bufferSize
        self.client = client
        self.commandList = ['join', 'leave', 'msg', 'register', 'all', '?']
    
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
        if command == None:
            return
        
        if command[0] not in self.commandList:
            print("Invalid command!")
            return
        
        action = command[0]
        parameters = command[1:]
        
        if action == "join":
            if(self.checkParams("join", len(parameters), 2)):
                self.joinCommand(parameters[0], parameters[1])
                
        if action == "leave":
            print(f"Disconnected from: {Commands.address} {Commands.port}")
            Commands.address = None
            Commands.port = None
            Commands.isConnected = False
            return
        
        if Commands.isConnected:
            if action == "msg":
                receiverName = command[1]
                message = ' '.join(command[2:])
                parameters = [receiverName, message]
                if(self.checkParams("msg", len(parameters), 2)):
                    self.msgCommand(parameters[0], parameters[1])
                    
            if action == "register":
                if(self.checkParams("register", len(parameters), 1)):
                    return
                
            if action == "all":
                message = ' '.join(command[1:])
                self.allCommand(message)
        else:
            print("Connect to a server first!")
            
        if action == "?":
            self.commandHelp()
        
        return
        
    def joinCommand(self, address, port):
        destinationServer = (address, int(port))
        print(destinationServer)
    
        try:
            self.client.settimeout(5)
            self.client.sendto("Client connected".encode(), destinationServer)
            self.client.recvfrom(self.bufferSize)
            
            Commands.address = address
            Commands.port = int(port)
            Commands.isConnected = True
            print(f"Successfully connected to: {Commands.address} on port {Commands.port}")
        except socket.error as error:
            print(f"Connection Error: {error}")
            
        return

    def msgCommand(self, messageReceiver, message):
        return
    
    def registerCommand(self, clientName):
        return

    def allCommand(self, message):
        jsonMessage = str({'message' : message}).encode()
        try:
            self.client.sendto(jsonMessage, (Commands.address, Commands.port))
        except socket.error as error:
            print(f"Message Send Error: {error}")
        return

    def commandHelp(self):
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
