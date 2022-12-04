import socket
import lookupTable

class serverUtilities:
    lookupTable = lookupTable.lookupTable()
    
    def __init__(self, localAddress, localPort, bufferSize, server):
        self.localAddress = localAddress
        self.localPort = localPort
        self.bufferSize = bufferSize
        self.server = server
    
    def sendJsonMessage(self, jsonMessage, clientAddress):
        self.server.sendto(str(jsonMessage).encode(), clientAddress)
        return
    
    def parseJsonCommand(self, jsonCommand, clientAddress):
        command = jsonCommand['command']
        
        if command == None:
            jsonMessage = {
                "error" : "no command was received"
            }
            self.sendJsonMessage(jsonMessage, clientAddress)
        
        if command == "join":
            self.serverJoin(clientAddress)
            
        if command == "all":
            self.serverAll(jsonCommand, clientAddress)
            
        if command == "register":
            self.serverRegister(jsonCommand, clientAddress)
        
        # FOR DEBUG PURPOSES ONLY, REMOVE AFTER 
        if command == "kill":
            return False
            
        return True
            
    def serverJoin(self, clientAddress):
        if not serverUtilities.lookupTable.getClientFromAddressPort(clientAddress):
            serverUtilities.lookupTable.addClient(clientAddress)
        
        jsonMessage = {
            "command" : "join",
            "message" : f"You have successfully connected to {self.localAddress} {self.localPort}"
        }
        self.sendJsonMessage(jsonMessage, clientAddress)
        return
    
    def serverAll(self, jsonCommand):
        message = jsonCommand["message"]
        jsonMessage = {
            "command" : "all",
            "message" : f"{message}"
        }
        
        # TODO insert code to send the message to all clients in the server
        return
    
    def serverRegister(self, jsonCommand, clientAddress):
        handle = jsonCommand["handle"]
        if(serverUtilities.lookupTable.addHandle(clientAddress, handle)):
            jsonMessage = {
                "command" : "register",
                "message" : f"Successful registration! Welcome {handle}"
            }
            self.sendJsonMessage(jsonMessage, clientAddress)
            return
        print("failure")
        jsonMessage = {
            "command" : "register",
            "message" : f"Failure to register under handle \'{handle}\'"
        }
        self.sendJsonMessage(jsonMessage, clientAddress)
        return
    
