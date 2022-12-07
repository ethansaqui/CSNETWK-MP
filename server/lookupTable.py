class lookupTable:

    table = []
    
    def __init__(self):
        return
    
    def addClient(self, addressPort):
        clientNumber = lookupTable.table.__len__()
        newClient = {
            "handle" : f"Guest {addressPort[1]}{clientNumber}",
            "address" : addressPort,
            "registered": False
        }
        lookupTable.table.append(newClient)
        return
    
    def addHandle(self, addressPort, handle):
        client = self.getClientFromAddressPort(addressPort)
        isExist = self.getClientFromHandle(handle)
        if client != None and handle != client["handle"] and isExist == None:
            client["handle"] = handle
            client["registered"]= True
        else:
            return False
        return True
    
    def removeClient(self, addressPort):
        for client in lookupTable.table:
            if(client["address"] == addressPort):
                lookupTable.table.remove(client)
        return None
    
    def getClientFromAddressPort(self, addressPort):
        for client in lookupTable.table:
            if(client["address"] == addressPort):
                return client
        return None
    
    def getClientFromHandle(self, handle):
        for client in lookupTable.table:
            if(client["handle"] == handle):
                return client
        return None
    
    def getOtherClients(self, addressPort):
        client_list = []
        for client in lookupTable.table:
            client_list.append(client["address"])
        return client_list
    