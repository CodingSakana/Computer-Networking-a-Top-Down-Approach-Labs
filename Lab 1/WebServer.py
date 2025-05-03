#!/usr/bin/env python3
#import socket module
# http://192.168.1.106:55555/HelloWorld.html
# http://192.168.1.106:55555/Architecture.html
from datetime import datetime, timezone
from socket import *
import sys # In order to terminate the program
serverSocket = socket(AF_INET, SOCK_STREAM)     # TCP connection
#Prepare a sever socket
#Fill in start
ServerPort = 55555
serverSocket.bind(('', ServerPort))
serverSocket.listen(1)
#Fill in end
while True:
    #Establish the connection
    print('Ready to serve...')
    #Fill in start
    connectionSocket, addr = serverSocket.accept()
    #Fill in end
    try:
        #Fill in start
        message = connectionSocket.recv(1024).decode()
        #Fill in end
        print(message)
        filename = message.split()[1]   # split the message with "space" (defalt)
        f = open(filename[1:])
        #Fill in start
        outputdata = f.read()
        #Fill in end
        #Send one HTTP header line into socket
        #Fill in start
        now_utc = datetime.now(timezone.utc)
        http_date = now_utc.strftime("%a, %d %b %Y %H:%M:%S GMT")
        HTTPHeader = (
            "HTTP/1.1 200 OK\r\n"
            f"Date: {http_date}\r\n"
            "Server: Linux-sssakana@sssakana-A320M-S2H\r\n"
            f"Content-Length: {len(outputdata)}\r\n"
            "Content-Type: text/html\r\n"
            "\r\n"
        )
        connectionSocket.send(HTTPHeader.encode())
        #Fill in end
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()
    except IOError:
        #Send response message for file not found
        #Fill in start
        now_utc = datetime.now(timezone.utc)
        http_date = now_utc.strftime("%a, %d %b %Y %H:%M:%S GMT")
        HTTPHeader = (
            "HTTP/1.1 404 Not Found\r\n"
            f"Date: {http_date}\r\n"
            "Server: Linux-sssakana@sssakana-A320M-S2H\r\n"
            "Content-Type: text/html\r\n"
            "\r\n"
        )
        connectionSocket.send(HTTPHeader.encode())
        connectionSocket.send("\r\n".encode())
        #Fill in end
        #Close client socket
        #Fill in start
        connectionSocket.close()
        #Fill in end
serverSocket.close()
sys.exit() #Terminate the program after sending the corresponding data