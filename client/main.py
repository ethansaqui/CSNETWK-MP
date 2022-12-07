import socket
import commands
import threading

bufferSize = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(5)

clientRunning = True

while(clientRunning):

    clientCommands = commands.Commands(client, bufferSize)
    
    commandString = None
    while commandString == None:
        try:
            commandString = input('')
        except KeyboardInterrupt:
           
            clientCommands.leaveCommand()
            clientRunning = False
            print("Exited client")
            break

    command = clientCommands.tokenizeCommandString(commandString)
    clientCommands.commandSwitch(command)
    
    thread = threading.Thread(target=clientCommands.threadRecvFromServer)
    thread.daemon = True
    thread.start()
    
    if clientRunning == False:
        break
    

client.close()