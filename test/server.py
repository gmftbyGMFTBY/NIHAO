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

import socket
import sys, select, os, time
from multiprocessing import *

def pack_msg():
    # pack the msg to information class
    pass

class infomation:
    '''
    1. The msg class send to the subprocess, have many types
    2. Server recv and send the msg in this type
    3. The information may be the request or the data need to forward to other users ...
    4. Information finally need to unpack at handle to send
    5. Information can be create by Server or handle
    '''
    def __init__(self):
        # init the msg class
        pass

    def get_msg_type(self):
        # return [number of the msg, type of the msg]
        pass

    def set_msg_type(self):
        pass

    def get_msg_data(self):
        # this function may be the iterations
        pass

    def set_msg_data(self):
        pass

    def unpack_msg(self):
        pass

class handle:
    '''
    The subprocess handle the connections with the clients
    Before quit from the server, need to send a quit msg or the wrong quit send
    the empty string
    '''
    def __init__(self):
        # using socket and addr to init the subprocess
        pass

    def detect_request(self):
        # detect [server msg, client msg]
        pass

    def send_msg(self):
        # send the information to sercer
        pass

    def recv_msg(self):
        # recv the information from the server
        pass

    def serve_forever(self):
        # mainloop 
        pass

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

    def append_user(self, uid, uname, pipeline):
        # create the user entry and the subprocess
        if self.usertable[uid]: 
            # the uid of the user is already existed, WRONG!
            return False
        self.usertable[uid] = [uname, pipeline]
        return True

    def delete_user(self, uid):
        # delete the user entry and the subprocess
        if not self.usertable.get(uid):
            # the user is not in the table, WRONG
            return False
        del self.usertable[uid]
        return True

    def search_user(self, uid):
        # search the user table and process table, return [uname, piepline]
        if self.usertable.get(uid): return self.usertable[uid]
        else: return False

    def detect_request(self):
        # use select function to detect the msg from the subprocess
        # detect the pipe line of the processes(clients - users)
        readlist = [pipe for user in self.usertable]
        rlist, _, _ = select.select(readlist, [], [], 0.1)
        if not rlist: return None
        else: return rlist

    def recv_msg(self, pipeline):
        return pipeline.recv()

    def send_msg(self, pipeline, msg):
        # send the msg to the subprocess
        pipeline.send(msg)

    def data_getter(self):
        # get the data from the server(sql), need to pack into the informtion class
        # using the sql interface
        pass

    def data_setter(self):
        # change the data on the server(sql), need to unpack
        # using  the sql interface
        pass

    def verify(self):
        # verify the user
        pass

    def get_accept(self):
        # mainloop
        # this process get the connection from the clients and create the
        # the subprocess to handle them.
        while self.run:
            conn, addr = self.socket.accept()
            print("connected by", addr)
            # verification the user
            res = self.verify()
            # if the user is in the database
            if res: uid, uname = res
            else:
                conn.close()
                continue

            # create the subprocess
            fpipe, spipe = Pipe(duplex = True)
            handler = handle(conn, addr, spipe)
            self.append_user(uid, uname, fpipe)
            # start the subprocess to server the specifial client
            subprocess = Process(target = handler.serve_forever)
            subprocess.start()

            # append the user into the table to record
            self.append_user(uid, uname, fpipe)

            # the end of the handler is in the `delete_user` function to do this 
    
    def serve_forever(self):
        # start subprocess to get the connect
        s1 = Process(target = self.get_accept)
        s1.start()

        # check to serve all the subprocess of the client connectors
        while True:
            print(self.usertable, end='\r')
            
            res = self.detect_request()
            if not res: continue

            # get the IO operations from the subprocess in the user tables
            for rfile in res:
                msg = self.recv_msg()

                # analyse the msg

                # action
                self.action()

    def action(self):
        # this action contain all the move in the server
        pass


if __name__ == "__main__":
    host   = ''
    port   = 50000
    print("Server begin ...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # init the socket of the server
        s.bind((host, port))
        s.listen(5)
        Server = server(s, host, port)
        Server.serve_forever()
    print("Server end   ...")
