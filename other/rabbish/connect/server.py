#!/usr/bin/python

'''
    该模块完成服务器类
        1. 和客户端全双工通信 (yes)
        2. 采用多路复用的 I/O 处理技术实现多客户端连接处理 (yes)
        3. 实现客户端之间的双工通信  单用户对单用户　(yes)
        4. 实现客户端之间的双工通信  单用户对多用户的广播 (yes)
        5. 实现客户端和客户端或者服务端之间的文件的发送，使用 nc 实现
    和服务器的通信默认是没有前缀的，但是和其他的客户通信是需要前缀的
        1. 服务器通信没有前缀
            `Msg`
        2. 和其他的客户端单对单的双工通信需要前缀
            `TO:Name:Msg`
        3. 和其他的客户端的单对多的双工通信需要前缀
            `BC:3:Name1:Name2:Name3:Msg`
'''

import socket
import socketserver
import threading
import sys
import select
import io
import os
import time

def handle_BBS(name, request):
    # server BBS model
    print("server handle the BBS model for", name)
    while True:
        data = request.recv(1024).decode()
        if data.strip() == "exit" or data.strip() == '':
            print("exit the Model BBS for", name)
            return
        elif data.strip() == "WANT":
            # show the message
            with open("bbs") as f:
                content = f.read()
                request.send(content.encode())
            # request.send(b"nothing is here!")
        else:
            print(data)


class MyTCPHandle(socketserver.BaseRequestHandler):
    def handle(self):
        name = self.request.recv(1024).decode()
        print(name + " get connection with server!")
        # 收到一个链接，加入 GUT 表中,测试的时候 Name 是 port, IP 是 ip + port
        GUT.add_table(name, self.client_address[0] + str(self.client_address[1]))
    
        # 
        send_counter = 0
        recv_counter = 0
        running = True

        while running:

            # 覆写该函数实现对连接请求的响应, delay 3 sec
            input_list = [self.request, sys.stdin]

            # 检查是否存在有对应的 io 对象可以加入,输入用户名，这里的用户名在测试的时候是端口号
            # 如果程序执行的速度非常快的话，会导致死锁

            # 这里感觉含香没有必要加入到文件等待队列中，可以直接的判断是否存在有对应的接收消息然后直接将消息读取出来
            # 如果这一步存在有消息的话，可以直接的发送 send 到对应的服务器上去，也不需要使用文件的方式来存储文件中的数据
            # 从而加快时间
            if GCT.exist(name):
                # 如果存在有发送给当前线程对应的客户端的消息，直接转发给客户端
                for item in GCT.table[name]:
                    self.request.send(item[1].encode())
                GCT.delete_table_many(name)

            rlist, wlist, xlist = select.select(input_list, [], [], 3)
    
            for file in rlist:
                if file == sys.stdin:
                    # 服务器从标准输入中获取数据
                    data = input()
                    
                    if data == 'exit':
                        running = False
                        break
                    elif data.startswith('TO'):
                        # 需要向其他的客户端发送消息,TO:Name:Msg (测试的时候Name使用port并且假定一定在线)
                        result = data.split(':')
                        receiver = result[1]
                        msg = ':'.join(result[2:])
                        # 构建 IO 对象,起始使用 ... : 起头书写文件
                        GCT.add_table(receiver, "server", msg)
                    elif data.startswith('BC'):
                        # 广播
                        result = data.split(":")
                        recever_number = int(result[1])
                        receivers = result[2:(2+recever_number)]
                        msg = ":".join(result[2+recever_number:])
                        for user in receivers:
                            GCT.add_table(user, "server", msg)
                    else:
                        users = GUT.get_all_user()
                        for user in users:
                            GCT.add_table(str(user), "server", data)
                elif file == self.request:
                    # 从套接字中获取数据并输出
                    data = self.request.recv(1024).decode()
                    if data and not data.startswith("TO") and not data.startswith("BC"):
                        # 正常发往服务器的通信
                        if data.strip() == "BBS":
                            # client get into the BBS Model
                            handle_BBS(name, self.request)
                        else:
                            print(name + ': ' + data)
                            recv_counter += 1
                    elif data.startswith("TO"):
                        # 需要向其他的客户端发送消息,TO:Name:Msg (测试的时候Name使用port并且假定一定在线)
                        result = data.split(':')
                        receiver = result[1]
                        msg = name + ': ' + ":".join(result[2:])
                        # 构建 IO 对象,这里还存在有通过当前的 self.client_address 查找对应的用户名的操作，但是在测试阶段省去了
                        GCT.add_table(receiver, str(self.client_address[1]), msg)
                    elif data.startswith('BC'):
                        # 广播
                        result = data.split(":")
                        recever_number = int(result[1])
                        receivers = result[2:(2+recever_number)]
                        msg = name + ':' + ":".join(result[2+recever_number:])
                        for user in receivers:
                            GCT.add_table(user, str(self.client_address[1]), msg)
                    else:
                        pass
                else:
                    # 和别的用户的交互
                    for line in file.readlines():
                        res = line.strip().split(':')
                        sender = res[0]
                        data = ':'.join(res[1:])
                        if data:
                            print(sender, data)
                            # 补充信息并完成信息转接
                            data = sender + ':' + data
                            self.request.send(data.encode())
                            send_counter += 1
                    # 读完可以关闭这个句柄，然后删除(垃圾回收)
                    file.close()
        # delete the user in the GUT
        GUT.delete_table((name, self.client_address[1]))

class Duplexing_Threading_TCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class Global_User_Table:
    def __init__(self):
        self.table = {}
        self.user_count = 0
        self.lock = threading.Lock()

    def add_table(self, name, ip):
        self.lock.acquire()
        if self.table.get(name) is None:
            # add
            self.table[name] = ip
        self.lock.release()

    def delete_table(self, name):
        self.lock.acquire()
        if self.table.get(name) is not None:
            del self.table[name]
        self.lock.release()

    def exist(self, name):
        self.lock.acquire()
        if self.table.get(name) is None:
            self.lock.release()
            return False
        else:
            self.lock.release()
            return True
    
    def get_all_user(self):
        return list(self.table.keys())

class Global_Comm_Table:
    def __init__(self):
        self.table = {}
        self.counter = 0
        self.lock = threading.Lock()

    def add_table(self, receiver, sender, iowrapper):
        self.lock.acquire()
        if self.table.get(receiver) is None:
            self.table[receiver] = [(sender, iowrapper)]
        else:
            self.table[receiver].append((sender, iowrapper))
        self.lock.release()

    def delete_table(self, receiver, sender):
        # 只删除指定的消息 (sender, receiver)
        self.lock.acquire()
        if self.table.get(receiver) is None:
            self.lock.release()
            return 
        for item in self.table[receiver]:
            if item[0] == sender:
                self.table[receiver].remove(item)
                break
        self.lock.release()

    def delete_table_many(self, receiver):
        # 删除当前的接受者的所有的列表文件接收器 iowrapper
        self.lock.acquire()
        if self.table.get(receiver) is None:
            self.lock.release()
            return
        del self.table[receiver]
        self.lock.release()

    def exist(self, receiver):
        self.lock.acquire()
        if self.table.get(receiver) is None:
            self.lock.release()
            return False
        else:
            self.lock.release()
            return True

if __name__ == "__main__":
    host = ''
    port = 50001
    print("server begin ...");

    server = Duplexing_Threading_TCPServer((host, port), MyTCPHandle)
    with server:
        GUT = Global_User_Table()
        GCT = Global_Comm_Table()
        ip, port = server.server_address
        server.serve_forever()
