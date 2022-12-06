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
            self.serverMsg(jsonCommand, clientAddress)    
        
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
        reciever = jsonCommand["messageReceiver"]
        message = jsonCommand["message"]
        sender = serverUtilities.lookupTable.getClientFromAddressPort(clientAddress)["handle"]
        receiverAddress = serverUtilities.lookupTable.getClientFromHandle(reciever)
        
        if(receiverAddress == None):
            jsonMessage = {
                "command" : "msg",
                "message" : f"Error: Handle or alias not found."
            }
            self.sendJsonMessage(jsonMessage, clientAddress)    
            return
        
        #Condition: if client exists
        if serverUtilities.lookupTable.getClientFromHandle(reciever) != None:
            jsonMessage = {
                    "command" : "msg",
                    "toMessage" : f"[To {reciever}]: {message}",
                }
            self.sendJsonMessage(jsonMessage, clientAddress)
            
            jsonMessage = {
                    "command" : "msg",
                    "fromMessage": f"[From {sender}]: {message}"
                }
            self.sendJsonMessage(jsonMessage, receiverAddress["address"])
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
