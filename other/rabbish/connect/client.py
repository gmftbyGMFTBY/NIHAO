#!/usr/bin/python

'''
    实现和其他客户端的全双工通信
'''

import socket
import select
import sys
import os

def BBS(client):
    # BBS model
    while True:
        # clear the screen
        os.system('clear')
        # show the message
        client.send(b"WANT")
        print(client.recv(1024).decode())
        data = input()
        if data == "exit":
            # exit the BBS
            print("client leave the BBS model")
            client.send(b"exit")
            return
        else:
            pass


class Duplexing_TCPClient:
    def __init__(self, host, port, size, timeout):
        '''
        host, port -> addr
        size       -> 一次传输的缓存大小
        timrout    -> select 轮询超时时间
        '''
        self.size = size
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.input_list = [sys.stdin, self.client]
        # select 轮询的超时时间
        self.timeout = timeout
        # 套接字是否正常连接
        self.connection = True
        # 发送计数器
        self.send_counter = 0
        # 接收计数器
        self.recv_counter = 0

    def check(self):
        # 全双工模式，异步检查是否存在标准输入或者是socket中存在可读数据
        # 如果确定存在可以读取的数据返回列表，否则返回False标志
        rlist, wlist, xlist = select.select(self.input_list, [], [], self.timeout)

        if rlist :
            return rlist
        else:
            return False

    def send_msg(self, msg):
        try:
            self.client.send(msg.encode())
            self.send_counter += 1
        except Exception as e:
            # 可能是 isinstance(msg, bytes) == False
            print(e)

    def recv_msg(self):
        try:
            data = self.client.recv(self.size).decode()
            self.recv_counter += 1
            return data
        except Exception as e:
            print(e)
            return False

    def run(self):
        # 运行测试函数
        running = True
        # send the name
        print("Input your name: ", end = '')
        name = input()
        self.send_msg(name)

        while running:

            result = self.check()
            if result :
                for file in result:
                    if file == self.client:
                        # 套接字中存在可读数据
                        data = self.recv_msg()

                        if data == '':
                            # 没有实际的数据，表明服务器没有发送数据过来
                            # 猜测可能的原因是服务器停止服务或者和服务器的连接中断
                            print("Out[%d]: The connection with the server may be broken ..." % self.send_counter)
                            self.close()
                            return False
                        else:
                            # 接收到客户端的数据
                            print(data)
                    else:
                        # 标准输入中的数据
                        data = input()
                        if data.strip() == 'exit':
                            # exit
                            running = False
                            break
                        elif data.strip() == "BBS":
                            # get into the BBS model
                            self.send_msg(data)
                            print("into the BBS model")
                            BBS(self.client)
                        else:
                            self.send_msg(data)

    def close(self):
        # 清理操作
        self.client.close()
        print("客户端关闭")
        self.connection = False

if __name__ == "__main__":
    host = ''
    port = 50001
    client = Duplexing_TCPClient(host, port, 1024, 3)
    client.run()
