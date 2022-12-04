class lookupTable:

    table = []
    
    def __init__(self):
        return
    
    def addClient(self, addressPort):
        clientNumber = lookupTable.table.__len__()
        newClient = {
            "handle" : f"Client {addressPort[1]}{clientNumber}",
            "address" : addressPort,
        }
        lookupTable.table.append(newClient)
        print(lookupTable.table)
        return
    
    def addHandle(self, addressPort, handle):
        client = self.getClientFromAddressPort(addressPort)
        isExist = self.getClientFromHandle(handle)
        if client != None and handle != client["handle"] and isExist == False:
            client["handle"] = handle
        else:
            return False
        print(lookupTable.table)
        return True
    
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
    