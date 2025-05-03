#include <iostream>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <cstring>

const int MAX_LISTEN_QUEUE = 5;

int main(int argc, char *argv[]){
    int listenfd, connfd;

    struct sockaddr_in cliaddr, servaddr;
    std::memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(80);
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);

    listenfd = socket(AF_INET, SOCK_STREAM, 0);
    bind(listenfd, (sockaddr *)&servaddr, sizeof(servaddr));
    listen(listenfd, MAX_LISTEN_QUEUE);
    while(true){
        char buf[2048];
        unsigned clilen = sizeof(cliaddr);
        connfd = accept(listenfd, (sockaddr *)&cliaddr, &clilen);
        int n = recv(connfd, &buf, sizeof(buf) - 1, 0);
        
    }

}