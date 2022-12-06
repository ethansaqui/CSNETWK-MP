import socket
import lookupTable

class serverUtilities:
    lookupTable = lookupTable.lookupTable()
    
    def __init__(self, localAddress, localPort, bufferSize, server):
        self.localAddress = localAddress
        self.localPort = localPort
        self.bufferSize = bufferSize
        self.server = server
        self.client = None #ADDED
    
    def sendJsonMessage(self, jsonMessage, clientAddress):
        
        self.server.sendto(str(jsonMessage).encode(), clientAddress)
        return

    def sendJsonMessageAll(self, jsonMessage, clientAddress_List):
        i = 0
        while i < len(clientAddress_List):
            print( "doing this ")
            print(clientAddress_List[i])
            self.server.sendto(str(jsonMessage).encode(), clientAddress_List[i])
            i+= 1
        return
    
    
    def parseJsonCommand(self, jsonCommand, clientAddress):
        command = jsonCommand['command']
        
        if command == None:
            jsonMessage = {
                "error" : "no command was received"
            }
            self.sendJsonMessage(jsonMessage, clientAddress)
        
        if command == "join":
            self.client = self.serverJoin(clientAddress)
               
        if command == "all":
            self.serverAll(jsonCommand, clientAddress)
            
        if command == "register":
            self.serverRegister(jsonCommand, clientAddress)
        
        #ADDED    
        if command == "msg":
            sender = self.client
            self.serverMsg(jsonCommand, sender, clientAddress)    
        
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
        return serverUtilities.lookupTable.getClientFromAddressPort(clientAddress)["handle"]
    
    def serverAll(self, jsonCommand, clientAddress):
        message = jsonCommand["message"]
        client_list = serverUtilities.lookupTable.getOtherClients(clientAddress)
        print(client_list)
        jsonMessage = {
            "command" : "all",
            "message" : f"{message}"
        }
        self.sendJsonMessageAll(jsonMessage, client_list)
        
        # TODO insert code to send the message to all clients in the server
        return
    
    #ADDED
    def serverMsg(self, jsonCommand, sender, clientAddress):
        reciever = jsonCommand["messageReceiver"]
        message = jsonCommand["message"]
        
        #Condition: if client exists
        if serverUtilities.lookupTable.getClientFromHandle(reciever) != None:
            jsonMessage = {
                    "command" : "msg",
                    "toMessage" : f"[To {reciever}]: {message}",
                    "fromMessage": f"[From {sender}]: {message}"
                }
            self.sendJsonMessage(jsonMessage, clientAddress)
            return
        #Condition: client does not exist
        jsonMessage = {
            "command" : "msg",
            "message" : f"Error: Handle or alias not found."
        }
        self.sendJsonMessage(jsonMessage, clientAddress)    
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
