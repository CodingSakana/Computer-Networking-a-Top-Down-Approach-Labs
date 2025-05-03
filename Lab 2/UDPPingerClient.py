#!/usr/bin/env python3
from socket import *
import time
serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1.0)
RTT_list = []
Tout = 0
for i in range(0, 10):
    sendTime = time.time()
    pingMessage = f"Ping {i} {sendTime}"
    clientSocket.sendto(pingMessage.encode(), (serverName, serverPort))
    try:
        response, address = clientSocket.recvfrom(2048)
        receiveRime = time.time()
        RTT = (receiveRime - sendTime) * 1e6
        print(f"Receive {i} Message: {response.decode()}")
        print(f"RTT {i}: {RTT:.2f}ms")
        RTT_list.append(RTT)
    except timeout:
        print(f"Request {i} timed out.")
        Tout += 1
sum = 0
for i in RTT_list:
    sum += i
averagePing = sum/(10 - Tout)
LPR = Tout/10 * 100
print(f"Average Ping: {averagePing:.2f}ms")
print(f"Loss Packet Rate: {LPR:.0f}%")
clientSocket.close()