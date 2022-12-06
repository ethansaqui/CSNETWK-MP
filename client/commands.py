import socket
import json

class Commands:
    address = None
    port = None
    isConnected = False
    
    def __init__(self, client, bufferSize):
        self.bufferSize = bufferSize
        self.client = client
        self.commandList = ['join', 'leave', 'msg', 'register', 'all', '?', 'kill']
    
    def sendJsonMessage(self, jsonMessage, serverAddress):
        self.client.sendto(str(jsonMessage).encode(), serverAddress)
        return
    
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
            self.leaveCommand()
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
                    self.registerCommand(parameters[0])
                    return
                
            if action == "all":
                message = ' '.join(command[1:])
                self.allCommand(message)
            
            #FOR DEBUG PURPOSES ONLY, REMOVE AFTER
            if action == "kill":
                print(Commands.address)
                print(Commands.port)
                jsonMessage = {
                    "command" : "kill"
                }
                self.client.sendto(str(jsonMessage).encode(), (Commands.address, int(Commands.port)))
        else:
            print("Connect to a server first!")
            
        if action == "?":
            self.commandHelp()
            return

        return
        
    def joinCommand(self, address, port):
        destinationServer = (address, int(port))
    
        try:
            jsonMessage = {
                "command": "join",
            }
            self.client.settimeout(5)
            self.sendJsonMessage(jsonMessage, destinationServer)
            
            Commands.address = address
            Commands.port = int(port)
            Commands.isConnected = True
            
        except socket.error as error:
            print(f"Connection Error: {error}")
            
        return

    def leaveCommand(self):
        
        jsonMessage = {
            "command" : "leave",
        }
        self.sendJsonMessage(jsonMessage, (Commands.address, Commands.port))
        Commands.address = None
        Commands.port = None
        Commands.isConnected = False
    
    
    def msgCommand(self, messageReceiver, message):
        jsonMessage = {
            "command" : "msg",
            "messageReceiver" : messageReceiver,
            "message" : message,
        }
        self.sendJsonMessage(jsonMessage, (Commands.address, Commands.port))
        return
    
    def registerCommand(self, handle):
        jsonMessage = {
            "command" : "register",
            "handle" : handle
        }
        self.sendJsonMessage(jsonMessage, (Commands.address, Commands.port))
        return

    def allCommand(self, message):
        jsonMessage = {
            "command" : "all",
            "message" : f"{message}"
        }
        try:
            self.sendJsonMessage(jsonMessage, (Commands.address, Commands.port))
        except socket.error as error:
            print(f"Message Send Error: {error}")
        return

    def receiveFromServer(self):
        message, address = self.client.recvfrom(self.bufferSize)
        return message, address
    
    def threadRecvFromServer(self):
        while True:
            try:
                message, address = self.receiveFromServer()
                message = message.decode()
                messageJson = json.loads(message.replace("\'","\""))
                command = self.parseServerMessageCommand(messageJson)
                printMessage = messageJson["message"]
                print(f"{command} {printMessage}")
            except:
                continue
        
    def parseServerMessageCommand(self, json):
        command = json["command"]
        
        if command == None:
            print("[Command Not Found]")
            return
            
        if command == "join":
            return "[Server Joined]"
            
        if command == "all":
            sender = json["sender"]
            return f"[All From {sender}]"
            
        if command == "register":
            return "[Registered]"
        
        if command == "msg":
            return "[Private]"
        
        if command == "leave":
            return "[Server Exited]"
        
        if command == "error":
            return "[Error]"
        
        
        return True           
    
    def commandHelp(self):
        print("""    +==========================+=============================================+======================+
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
        

