#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main(int argc, char* argv[])
{
    struct timeval tv;
    fd_set readfds;
    tv.tv_sec = 10;
    tv.tv_usec = 500000;
    FD_ZERO(&readfds);          // clear the readfds set
    FD_SET(0, &readfds);        // add the stdin into the readfds set

    select(1, &readfds, NULL, NULL, &tv);

    if (FD_ISSET(0, &readfds)) {
        printf("In\n");
    }
    else {
        printf("timeout\n");
    }
    return 0;
}
