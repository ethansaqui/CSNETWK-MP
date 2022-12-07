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
        try:
            jsonString = json.dumps(jsonMessage)
            self.client.sendto(jsonString.encode(), serverAddress)
        except Exception as e: print(f"[Error] {e}")
            
        return
    
    def tokenizeCommandString(self, commandString):
        if(not commandString): return None
        if(commandString[0] == '/'):
            return commandString[1:].split(' ')
        else:
            print("[Error] Invalid command! Start commands with a /")   
        
    def checkParams(self, command, numParams, expectedParams):
        if command == "msg" and numParams > 2:
            return True
        if numParams == expectedParams:
            return True
        print(f"[Error] Expected {expectedParams} params for command [{command}], but {numParams} were given")
        return False

    def commandSwitch(self, command):
        if command == None:
            return
        
        if command[0] not in self.commandList:
            print("[Error] Invalid command!")
            return
        
        action = command[0]
        parameters = command[1:]
        
        if action == "join":
            if(self.checkParams("join", len(parameters), 2)):
                self.joinCommand(parameters[0], parameters[1])
            return
        
        if action == "?":
            self.commandHelp()
            return        
        
        if Commands.isConnected:
                            
            if action == "leave":
                if(self.checkParams("leave", len(parameters), 0)):
                    self.leaveCommand()
                return
            
            if action == "msg":
                parameters = len(command) - 1
                
                if(self.checkParams("msg", parameters, 2)):
                    receiverName = command[1]
                    message = ' '.join(command[2:])
                    self.msgCommand(receiverName, message)
                    
            if action == "register":
                if(self.checkParams("register", len(parameters), 1)):
                    self.registerCommand(parameters[0])
                    return
                
            if action == "all":
                message = ' '.join(command[1:])
                self.allCommand(message)
            
            #FOR DEBUG PURPOSES ONLY, REMOVE AFTER
            if action == "kill":
                jsonMessage = {
                    "command" : "kill"
                }
                self.client.sendto(str(jsonMessage).encode(), (Commands.address, int(Commands.port)))
        else:
            print("[Error] Connect to a server first!")

        return
        
    def joinCommand(self, address, port):
        try:
            destinationServer = (address, int(port))
        except Exception as error:
            print("[Error] Invalid address port")
            return
            
    
        try:
            jsonMessage = {
                "command": "join",
            }
            self.client.settimeout(5)

            self.sendJsonMessage(jsonMessage, destinationServer)
            message, senderAddress = self.receiveFromServer()
            message = message.decode()
            messageJson = json.loads(message.replace("\'","\""))
            printMessage = messageJson["message"]
            command = self.parseServerMessageCommand(messageJson)
            print(f"{command} {printMessage}")
            
            Commands.address = address
            Commands.port = int(port)
            Commands.isConnected = True
            
        except socket.error as error:
           print("[Connection Error] Server does not exist")
            
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
        except Exception as error:
            print(f"[Message Send Error] {error}")
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
            return f"{sender}:"
            
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
        

