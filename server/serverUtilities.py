import socket

class serverUtilities:
    
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
        
        if command == "kill":
            return False
            
        return True
            
    def serverJoin(self, clientAddress):
        # insert code to check register lookup table
        # if in lookup has registered name, set user as the name
        
        jsonMessage = {
            "server" : f"You have successfully connected to {self.localAddress} {self.localPort}"
        }
        self.sendJsonMessage(jsonMessage, clientAddress)
        return