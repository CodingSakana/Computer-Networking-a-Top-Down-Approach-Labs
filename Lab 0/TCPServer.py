#!/usr/bin/env python3
from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)      # 配置套接字的监听状态。
print("The server is ready to receive")
while True:
    connectionSocket, addr = serverSocket.accept()
    message = connectionSocket.recv(1024).decode()
    modifiedMessage = message.upper()
    connectionSocket.send(modifiedMessage.encode())
    connectionSocket.close()
