#!/usr/bin/env python3

from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
tcpSerSock.bind(('', 8888))  # Bind to all available interfaces on port 8888
tcpSerSock.listen(5)         # Allow up to 5 pending connections
# Fill in end.

while 1:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(4096).decode()  # Fill in start.  # Fill in end.
    print(message)
    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)
    try:
        # Check whether the file exists in the cache
        f = open(filetouse[1:], "r")                       
        outputdata = f.readlines()                         
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())             
        tcpCliSock.send("Content-Type:text/html\r\n".encode())
        # Fill in start.
        for line in outputdata:
            tcpCliSock.send(line.encode())
        # Fill in end.
        print('Read from cache')    
    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":  
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)  # Fill in start.  # Fill in end.
            hostn = filename.replace("www.","",1)          
            print(hostn)                                   
            try:
                # Connect to the socket to port 80
                c.connect((hostn, 80))  # Fill in start.   
                # Fill in end.
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = c.makefile('rwb', 0)                
                fileobj.write(("GET " + "http://" + filename + " HTTP/1.0\n\n").encode())   
                # Read the response into buffer
                buff = fileobj.readlines()  # Fill in start.   
                # Fill in end.
                # Create a new file in the cache for the requested file.  
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                tmpFile = open("./" + filename,"wb")   
                # Fill in start.   
                for line in buff:
                    tmpFile.write(line)
                    tcpCliSock.send(line)
                # Fill in end.    
            except:
                print("Illegal request")                                                
        else:
            # HTTP response message for file not found
            tcpCliSock.send("HTTP/1.0 404 Not Found\r\n".encode())  # Fill in start.   
            tcpCliSock.send("Content-Type:text/html\r\n".encode())  # Fill in end.
    # Close the client and the server sockets     
    tcpCliSock.close()  
# Fill in start.   
tcpSerSock.close()  # This will actually never be reached due to the infinite loop
# Fill in end.
