/********************************************************************************
 * Files         : client.h
 * Description   : the client part of network.
 * Author        : Shenhanwen
 * Last Modified : 2018.5.7
 ********************************************************************************/

#ifndef __CLIENT_H
#define __CLIENT_H


#include "chat.h"


 /********************************************************************************
  * Description : Declaration of all needed functions from client.c. (add all needed function from client.c here)
  * Author      : Guojiayan
  * Date        : 2018.5.6
  ********************************************************************************/
extern int init_net (const char *);
extern int signin (const char *, const char *);
extern int signup (const char *, const char *);
extern int inform_net ();

extern int load_friends_list (char friendlist[][MAX_LENGTH], int *);
extern int load_group_list (char gourplist[][MAX_LENGTH], int *);
extern int send_msg (const char *, const char *, int );

extern int search_friends (const char *, char friendname[][MAX_LENGTH], int *);
extern int add_friend_request (const char *);

extern int agree_add_friend(const char* friendname);
extern int refuse_add_friend(const char* friendname);

extern int request_chathistory (const char *, char namelist[][MAX_LENGTH], char msglist[][MAX_LENGTH]);

extern int agree_recv_file ();
extern int refuse_recv_file ();
extern int request_useravator ();
extern int send_a_file (const char *path, const char *friendname);

extern int send_useravator (int);

#endif
