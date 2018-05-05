#include <stdio.h>                                                                         
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <netdb.h>

#define PORT 3333
#define MAXDATASIZE 100

/*
   this is a test client for the server writing in C, and server is writing in Python
 */

int main(int argc, char* argv[])
{
    int sockfd, recvbytes;
    char buf[MAXDATASIZE];
    struct hostent* host;
    struct sockaddr_in serv_addr;

    if (argc < 2) {
        printf("Please enter the server's hostname!\n");
        exit(1);
    }
    
    if ((host = gethostbyname(argv[1])) == NULL) {
        printf("gethostbyname error!\n");
        exit(1);
    }

    if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        printf("socket create error!\n");
        exit(1);
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port   = htons(PORT);
    serv_addr.sin_addr   = *((struct in_addr *)host->h_addr);
    bzero(&(serv_addr.sin_zero), 8);

    if (connect(sockfd, (struct sockaddr*)&serv_addr, sizeof(struct sockaddr)) == -1) {
        printf("connect error!\n");
        exit(1);
    }

    if ((recvbytes = read(sockfd, buf, MAXDATASIZE)) == -1) {
        printf("recv error!\n");
        exit(1);
    }
    buf[recvbytes] = '\0';
    printf("get %s\n", buf, recvbytes);
    close(sockfd);
    return 0;
}
