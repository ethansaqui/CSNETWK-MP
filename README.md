# CSNETWK-MP
 
A basic chat program that utilizing UDP Socket connection that supports the following commands:

| Command                  | Description                                 | Sample Usage         |
|--------------------------|---------------------------------------------|----------------------|
| /join <server_ip> <port> | Connect to a server with IP and Port        | /join 127.0.0.1 5000 |
| /leave                   | Disconnect from current server              | /disconnect          |
| /register <handle>       | Register a unique handle or alias           | /register Milize     |
| /all <message>           | Send a message to all users                 | /all I have arrived! |
| /msg <handle> <message>  | Send a message to a specific user or handle | /msg Milize G valo?  |
| /?                       | Display this menu                           | /?                   |

Uses both a client and server, where multiple clients can converse using the server commands

### To run: 
1. Run main.py in the server directory
2. Run main.py in the client directory
3. Input commands as needed in the client to perform chat functions
