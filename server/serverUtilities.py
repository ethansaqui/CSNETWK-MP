import socket
import lookupTable
import json

class serverUtilities:
    lookupTable = lookupTable.lookupTable()
    
    def __init__(self, localAddress, localPort, bufferSize, server):
        self.localAddress = localAddress
        self.localPort = localPort
        self.bufferSize = bufferSize
        self.server = server
        
    def sendClientMessage(self, message, clientAddress):
        jsonMessage = {
            "message" : message,
        }
        self.sendJsonMessage(jsonMessage, clientAddress)
    
    def sendJsonMessage(self, jsonMessage, clientAddress):
        jsonString = json.dumps(jsonMessage)
        self.server.sendto(jsonString.encode(), clientAddress)
        return

    def sendJsonMessageAll(self, jsonMessage, clientAddress_List):
        i = 0
        jsonString = json.dumps(jsonMessage)
        while i < len(clientAddress_List):
            try:
                self.server.sendto(jsonString.encode(), clientAddress_List[i])
            except: raise
            i += 1
        return
    
    
    def parseJsonCommand(self, jsonCommand, clientAddress):
        command = jsonCommand['command']
        
        if command == None:
            self.sendClientMessage("[Error] No command was received", clientAddress)
        
        if command == "join":
            self.client = self.serverJoin(clientAddress)
        
        if(serverUtilities.lookupTable.getClientFromAddressPort(clientAddress) != None):
            
            if command == "all":
                self.serverAll(jsonCommand, clientAddress)
                
            if command == "register":
                self.serverRegister(jsonCommand, clientAddress)
            
            #ADDED    
            if command == "msg":
                self.serverMsg(jsonCommand, clientAddress)
                
            if command == "leave":
                self.serverLeave(clientAddress)
            
            # FOR DEBUG PURPOSES ONLY, REMOVE AFTER 
            if command == "kill":
                return False
        else:
            self.sendClientMessage("[Error] You are not connected to the server", clientAddress)
        return True
    
    def serverLeave(self, clientAddress):
        self.sendClientMessage("[Server] Connection has been closed, どうも", clientAddress)
        serverUtilities.lookupTable.removeClient(clientAddress)
        return
            
    def serverJoin(self, clientAddress):
        if not serverUtilities.lookupTable.getClientFromAddressPort(clientAddress):
            serverUtilities.lookupTable.addClient(clientAddress) 
            
        message = f"[Server] You have successfully connected to {self.localAddress} {self.localPort} Message Board"
        self.sendClientMessage(message, clientAddress)
            
        return 
    
    def serverAll(self, jsonCommand, clientAddress):
        message = jsonCommand["message"]
        client_list = serverUtilities.lookupTable.getOtherClients(clientAddress)
        client = serverUtilities.lookupTable.getClientFromAddressPort(clientAddress)
        sender = serverUtilities.lookupTable.getClientFromAddressPort(clientAddress)["handle"]
        
        if(not client["registered"]):
            self.sendClientMessage("[Error] Message not sent. Please register first.", clientAddress)
            return
        
        if((not message.isspace()) and message != ""):
            print("entered sending part")
            jsonMessage = {
                "command" : "all",
                "message" : f"{sender}: {message}"
            }
            print("test")
            self.sendJsonMessageAll(jsonMessage, client_list)
            return
        else:
            self.sendClientMessage("[Error] Please enter a message", clientAddress)
    
    #ADDED
    def serverMsg(self, jsonCommand, clientAddress):
        reciever = jsonCommand["handle"]
        message = jsonCommand["message"]
        client = serverUtilities.lookupTable.getClientFromAddressPort(clientAddress)
        sender = serverUtilities.lookupTable.getClientFromAddressPort(clientAddress)["handle"]
        receiverAddress = serverUtilities.lookupTable.getClientFromHandle(reciever)

        if(not client["registered"]):
            self.sendClientMessage("[Error] Message not sent. Please register first.", clientAddress)
            return
            
        if(receiverAddress == None):
            self.sendClientMessage("[Error] Handle or alias not found", clientAddress)
            return
       
        receiverAddress = receiverAddress["address"]
        if (reciever != sender):
            if((not message.isspace()) and message != ""): 
                if serverUtilities.lookupTable.getClientFromHandle(reciever) != None:
                    sendMessage = f"[To {reciever}]: {message}"
                    self.sendClientMessage(sendMessage, clientAddress)
                    
                    recMessage = f"[From {sender}]: {message}"
                    self.sendClientMessage(recMessage, receiverAddress)
                    return
            else:
                self.sendClientMessage("[Error] Please enter a message", clientAddress)  
                return  
        else:
            self.sendClientMessage("[Error] You cannot send a private message to yourself.", clientAddress)  
    
    def serverRegister(self, jsonCommand, clientAddress):
        cmd = "register"
        handle = jsonCommand["handle"]
        
        if(serverUtilities.lookupTable.getClientFromAddressPort(clientAddress)["registered"]):
            error = f"[Error] You are already registered"
            self.sendClientMessage(error, clientAddress) 
            return 
        
        if(serverUtilities.lookupTable.addHandle(clientAddress, handle)):
            message = f"Successful registration! Welcome {handle}"
            self.sendClientMessage(message, clientAddress) 
            return
        
        error = f"[Error] Failure to register under handle {handle}"
        self.sendClientMessage(error, clientAddress) 
        return
