#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#define PORT 3330
#define BACKLOG 10

int main(int argc, char* argv[])
{
    int sockfd, client_fd;
    struct sockaddr_in my_addr;         // server pos
    struct sockaddr_in remote_addr;     // client pos
    int sin_size;

    if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        printf("create connect failed!\n");
        exit(1);
    }

    my_addr.sin_family = AF_INET;
    my_addr.sin_port   = htons(PORT);       // 主机字节序转换网络字节序
    my_addr.sin_addr.s_addr = INADDR_ANY;
    bzero(&(my_addr.sin_zero), 8);

    if (bind(sockfd, (struct sockaddr*)&my_addr, sizeof(struct sockaddr)) == -1) {
        printf("bind error!\n");
        exit(1);
    }

    if (listen(sockfd, BACKLOG) == -1) {
        printf("listen error!\n");
        exit(1);
    }

    while (1) {
        sin_size = sizeof(struct sockaddr_in);
        if ((client_fd = accept(sockfd, (struct sockaddr*)&remote_addr, &sin_size)) == -1) {
            printf("accept error!\n");
            continue;
        }
        printf("Got on accept from: %s\n", inet_ntoa(remote_addr.sin_addr));
        pid_t pid = fork();
        if (pid == -1) {
            printf("fork error!\n");
            continue;
        }
        else if (pid == 0) {
            char buf[100] = "wocaonima";
            if (write(client_fd, buf, strlen(buf)) == -1) 
                printf("send error!\n");
            close(client_fd);
            exit(0);
        }
    }
    return 0;
}
