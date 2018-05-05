#include <stdio.h>
#include <stdlib.h>
#include <netdb.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <string.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <fcntl.h>

#define MAXDATASIZE 256
#define PORT 4444
#define BACKLOG 10
#define STDIN 0
#define TABLESIZE 100
#define NAMESIZE 20

struct table {
    char name[NAMESIZE];
    int pid;
    int fd;
    int exist;
};

struct table users[TABLESIZE];

int add_user(char* name, int pid, int fd)
{
    int flag  = 0;
    int index = 0;
    for (int i = 0; i < TABLESIZE; i ++) {
        if (users[i].exist == 0) {
            // empty block
            flag = 1;
            index = i;
        }
    }
    if (flag == 0) return -1;
    strcpy(users[index], name);
    users[index].pid = pid;
    users[index].fd  = fd;
    return 1;
}

int main(int argc, char* argv[])
{
    // init the users table
    memset(users, '\0', sizeof(users));

    int sockfd, client_fd;
    int sin_size;
    struct sockaddr_in my_addr, remote_addr;
    char buf[256];
    char buff[256];
    char send_str[256];
    int recvbytes;
    fd_set rfd_set, wfd_set, efd_set;
    struct timeval timeout;
    int ret;

    if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        printf("create socket error!\n");
        exit(1);
    }
    bzero(&my_addr, sizeof(struct sockaddr_in));
    my_addr.sin_family = AF_INET;
    my_addr.sin_port = htons(PORT);
    inet_aton("127.0.0.1", &my_addr.sin_addr);

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
        if((client_fd = accept(sockfd, (struct sockaddr*)&remote_addr, &sin_size)) == -1) {
            printf("accept error!\n");
            exit(1);
        }

        fcntl(client_fd, F_SETFD, O_NONBLOCK);

        // get one connection and the name from client
        recvbytes = recv(client_fd, buff, MAXDATASIZE, 0);
        buff[recvbytes] = '\0';
        fflush(stdout);

        pid_t pid = fork();
        if (pid == -1) {
            printf("fork error!\n");
            exit(1);
        }
        else if (pid == 0) {
            // subprocess exec
            printf("the subprocess will handle the connection\n");
        }
        else {
            // super process add the user into the table
            ret = add_user(buff, pid, client_fd);
            if (ret == -1) {
                // wrong with the table, cancle the connection
                printf("wrong with the user table\n");
            }
        }
    }
    return 0;
}
