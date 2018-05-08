#!/usr/bin/python3

# Author: GMFTBY
# Time:   2018.4.23

'''
The server writing in Python

1. Using multiprocessing module to create processes to handle the connections
   with the clients
2. Server process using the Pipe to exchange the message with the processes
3. Using the select system function to detect the IO operations
'''

import socket, random, threading
import sys, select, os, time
from multiprocessing import *

def pack_msg(count, msgtype, data):
    # pack the msg to information class, data is the list
    infor = information()
    infor.msgtype = msgtype
    if msgtype == 1:
        infor.sender = data[0]
        infor.recvnumber = int(data[1])
        infor.recever = data[2: (2 + infor.recvnumber)]
        infor.content = data[2 + infor.recvnumber]
    else:
        infor.msgtype = msgtype
        infor.count = count
        infor.set_msg_data(*data)
    return infor

def get_msg(count, sock):
    # get the number, type, content of the msg
    data = []
    for i in range(count): data.append(sock.recv(1024).decode())
    return data

class information:
    '''
    1. The msg class send to the subprocess, have many types
    2. Server recv and send the msg in this type
    3. The information may be the request or the data need to forward to other users ...
    4. Information finally need to unpack at handle to send
    5. Information can be create by Server or handle
    6. Content
        1. type:
            0. unknow
            1. talk msg
                sender, recevernumber, recever(s), content
            2. create group
            3. operate group
            4. register
            # 5. login
            6. exit from client
            7. make friend
            8. in group
            9. in BBS
            10. user set
            11. send file
            12. get users
            13. chat record
            14. out group
            15. delete friend
            16. get back the msg
            17. exit from server
            18. talk feedback, successfully or not
        2. count: the number of the msgs
        3. content: the count of the msg
    '''
    def __init__(self):
        self.msgtype = 0
        self.count = 0
        self.content = []

class handle:
    '''
    The subprocess handle the connections with the clients
    Before quit from the server, need to send a quit msg or the wrong quit send
    the empty string
    '''
    def __init__(self, s, addr, pipe, name):
        # using socket and addr to init the subprocess
        self.socket = s
        self.addr = addr
        self.pipe = pipe
        self.name = name

    def __del__(self):
        self.socket.close()
        self.pipe.close()
        print(self.addr, "close the connection")

    def detect_request(self):
        # detect [self.socket(r), self.pipe(r)]
        rlist = [self.pipe, self.socket]
        rlist, _, _ = select.select(rlist, [], [], 0.01)
        return rlist

    def send_msg(self, msg):
        # send the information class to server
        self.pipe.send(msg)

    def serve_forever(self):
        # mainloop
        while True:
            for fileno in self.detect_request():
                if isinstance(fileno, socket.socket):
                    msg_count = self.socket.recv(1).decode()
                    if not msg_count:
                        # client close the connection, `__del__`
                        infor = information()
                        infor.msgtype, infor.count, infor.content = 6, 1, self.name
                        self.pipe.send(infor)    # call the server to chaneg the table
                        exit(0)
                    else:
                        # send from client
                        msg_count = int(msg_count)
                        msgtype = int(self.socket.recv(1).decode())
                        infor = pack_msg(msg_count, msgtype, get_msg(msg_count, self.socket))
                        self.pipe.send(infor)
                else:
                    # send to the client connected or do something with the connections(17)
                    infor = fileno.recv()
                    if infor.msgtype == 17:
                        self.socket.send(b"Verify failed")
                        self.socket.close()
                        self.pipe.close()
                        exit(0)
                    elif infor.msgtype == 1:
                        self.socket.send(infor.content.encode('utf8'))
                    elif infor.msgtype == 18:
                        self.socket.send(str(infor.count).encode())
                        for i in range(infor.count):
                            self.socket.send(infor.content[i].encode())
                    else: pass

class server:
    '''
    1. The server class stand for the interface of the client
    2. Server hold all the msg, all messages send by the Server, subprocess
       Only play the roles to forwarding it
    '''
    def __init__(self, s, host, port):
        # create the server and bind ..., also need to create some tables
        self.socket = s
        self.host = host
        self.port = port

        # create the basic table for running time
        # (ID, Username, pipeline)
        self.usertable  = {}
        self.usernumber = 0

        # server running
        self.run = True
        self.processes = []

    def append_user(self, uid, uname, pipeline):
        if self.usertable.get(uid): 
            # the uid of the user is already existed, WRONG!
            return False
        self.usertable[uid] = [uname, pipeline]
        return True

    def delete_user(self, name):
        for key, user in self.usertable.items():
            if user[0] == name:
                del self.usertable[key]
                return True
        return False

    def search_user(self, name):
        for key, user in self.usertable.items():
            if user[0] == name: return user[1]
        return None

    def detect_request(self):
        readlist = [user[1] for key, user in self.usertable.items()]
        rlist, _, _ = select.select(readlist, [], [], 0.01)
        return rlist

    def data_getter(self):
        # get the data from the server(sql), need to pack into the informtion class
        # using the sql interface
        pass

    def data_setter(self):
        # change the data on the server(sql), need to unpack
        # using  the sql interface
        pass

    def verify(self, name, passwd):
        # verify the user
        return 1

    def get_accept(self):
        # accept the connection of the server
        while self.run:
            conn, addr = self.socket.accept()
            print("connected by", addr)

            # verify, only the successful verifacation can create the count on the table
            name = conn.recv(1024).decode()
            passwd = conn.recv(1024).decode()
            uid = self.verify(name, passwd)
            if not uid:
                conn.close()
                continue

            # create the subprocess
            fpipe, spipe = Pipe(duplex = True)
            handler = handle(conn, addr, spipe, name)
            self.append_user(uid, name, fpipe)

            # start the subprocess to server the specifial client
            subprocess = Process(target=handler.serve_forever)
            subprocess.start()

            # append the user into the table to record
            self.processes.append(subprocess)
            # the end of the handler is in the `delete_user` function to do this 
    
    def serve_forever(self):
        # start subprocess to get the connect
        s1 = threading.Thread(target = self.get_accept)
        s1.start()

        # check to serve all the subprocess of the client connectors
        while True:
            res = self.detect_request()
            for rfile in res:
                msg = rfile.recv()    # get the information class
                # action
                if msg.msgtype == 1:
                    # the talk msg to other clients(users), need to send the feedbakc for the sender
                    succ, failer = True, []
                    for i in range(msg.recvnumber):
                        new_infor = information()
                        new_infor.msgtype, new_infor.sender, new_infor.recever, new_infor.content = 1, msg.sender, msg.recever[i], msg.content
                        searchres = self.search_user(new_infor.recever)
                        if searchres: searchres.send(new_infor)
                        else:
                            succ = False
                            failer.append(new_infor.recever)
                    # send the feedback msg
                    infor = information()
                    infor.msgtype, infor.count, infor.content = 18, len(failer), failer
                    rfile.send(infor)
                elif msg.msgtype == 6:
                    # quit from the client
                    if self.delete_user(msg.content): print(f"Delete user {msg.content}")
                    else: print(f"{msg.content} do not exist")
                else: pass

if __name__ == "__main__":
    host  = ''
    port  = 50005
    print("Server begin ...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # init the socket of the server
        s.bind((host, port))
        s.listen(5)
        Server = server(s, host, port)
        Server.serve_forever()
    print("Server end   ...")
