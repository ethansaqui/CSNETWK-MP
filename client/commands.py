import socket
# TODO
# Check if server exists on joinCommand
# Implement other functions
# Server functions as well
# I can't specify them because I honestly have no idea

class Commands:
    address = None
    port = None
    
    def __init__(self, client, bufferSize):
        self.bufferSize = bufferSize
        self.client = client
    
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
        
        return
        
    def joinCommand(self, address, port):
        destinationServer = (address, int(port))
        print(destinationServer)
    
        try:
            self.client.settimeout(5)
            self.client.sendto("Requesting connection...".encode(), destinationServer)
            self.client.recvfrom(self.bufferSize)
            
            Commands.address = address
            Commands.port = int(port)
            print(f"Successfully connected to: {Commands.address} on port {Commands.port}")
        except socket.error as exc:
            print(f"Connection Error: {exc}")
            
        return

    def msgCommand(self, handle, message):
        return

    def allCommand(self, message):
        self.client.sendto(str.encode(message, 'utf-8'), (Commands.address, Commands.port))
        return
    
    def leaveCommand(self): 
        Commands.address = None
        Commands.port = None
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
