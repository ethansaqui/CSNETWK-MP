import socket
import lookupTable

class serverUtilities:
    lookupTable = lookupTable.lookupTable()
    
    def __init__(self, localAddress, localPort, bufferSize, server):
        self.localAddress = localAddress
        self.localPort = localPort
        self.bufferSize = bufferSize
        self.server = server
        self.client = None
        
    def sendClientMessage(self, command, message, clientAddress):
        jsonMessage = {
            "command" : command,
            "message" : message,
        }
        self.sendJsonMessage(jsonMessage, clientAddress)
    
    def sendJsonMessage(self, jsonMessage, clientAddress):
        
        self.server.sendto(str(jsonMessage).encode(), clientAddress)
        return

    def sendJsonMessageAll(self, jsonMessage, clientAddress_List):
        i = 0
        while i < len(clientAddress_List):
            print(clientAddress_List[i])
            try:
                self.server.sendto(str(jsonMessage).encode(), clientAddress_List[i])
            except: raise
            
            i += 1
        return
    
    
    def parseJsonCommand(self, jsonCommand, clientAddress):
        command = jsonCommand['command']
        
        if command == "join":
                self.client = self.serverJoin(clientAddress)
                
        
        if(serverUtilities.lookupTable.getClientFromAddressPort(clientAddress) != None):
            
            if command == None:
                self.sendClientMessage("error", "no command was received", clientAddress)
            
            
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
            self.sendClientMessage("error", "You are not connected to the server", clientAddress)
        return True
    
    def serverLeave(self, clientAddress):
        self.sendClientMessage("leave", "Connection has been closed, どうも", clientAddress)
        serverUtilities.lookupTable.removeClient(clientAddress)
        return
            
    def serverJoin(self, clientAddress):
        cmd = "join"
        if not serverUtilities.lookupTable.getClientFromAddressPort(clientAddress):
            serverUtilities.lookupTable.addClient(clientAddress) 
        
        message = f"You have successfully connected to {self.localAddress} {self.localPort}"
        self.sendClientMessage(cmd, message, clientAddress)
            
        return serverUtilities.lookupTable.getClientFromAddressPort(clientAddress)["handle"]
    
    def serverAll(self, jsonCommand, clientAddress):
        message = jsonCommand["message"]
        client_list = serverUtilities.lookupTable.getOtherClients(clientAddress)
        sender = serverUtilities.lookupTable.getClientFromAddressPort(clientAddress)["handle"]
        print(client_list)
        jsonMessage = {
            "command" : "all",
            "sender" : sender,
            "message" : f"{message}"
        }
        self.sendJsonMessageAll(jsonMessage, client_list)
        return
    
    #ADDED
    def serverMsg(self, jsonCommand, clientAddress):
        cmd = "msg"
        reciever = jsonCommand["messageReceiver"]
        message = jsonCommand["message"]
        sender = serverUtilities.lookupTable.getClientFromAddressPort(clientAddress)["handle"]
        receiverAddress = serverUtilities.lookupTable.getClientFromHandle(reciever)
        
        if(receiverAddress == None):
            self.sendClientMessage("error", "Handle or alias not found", clientAddress)
 
            return
        
        #Condition: if client exists
        if serverUtilities.lookupTable.getClientFromHandle(reciever) != None:
            message = f"[To {reciever}]: {message}"
            self.sendClientMessage(cmd, message, clientAddress)
            
            message = f"[From {sender}]: {message}"
            self.sendClientMessage(cmd, message, receiverAddress)
            return
        
        #Condition: client does not exist
        self.sendClientMessage("error", "Handle or alias not found.", clientAddress)  
        return
    
    def serverRegister(self, jsonCommand, clientAddress):
        cmd = "register"
        handle = jsonCommand["handle"]
        if(serverUtilities.lookupTable.addHandle(clientAddress, handle)):
            message = f"Successful registration! Welcome {handle}"
            self.sendClientMessage(cmd, message, clientAddress) 

            return
        error = f"Failure to register under handle {handle}"
        self.sendClientMessage("error", error, clientAddress) 
        return
