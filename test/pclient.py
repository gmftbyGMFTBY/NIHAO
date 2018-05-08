#!/usr/bin/python3

# Author: GMFTBY
# Time  : 2018.5.5

'''
This script with the server.py to test whether the server work well
'''

import socket, time

host = ''
port = 50005

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.send(b'lantian')
        time.sleep(0.0005)
        s.send(b'lt970106')

        time.sleep(2)

        # talk to myself
        s.send(b'4')
        time.sleep(0.0005)
        s.send(b'1')
        time.sleep(0.0005)
        s.send(b'lantian')
        time.sleep(0.0005)
        s.send(b'1')
        time.sleep(0.0005)
        s.send(b'lantian')
        time.sleep(0.0005)
        s.send(b'hello gmftbys!')

        print(s.recv(1024).decode())

        # feedback
        succ = int(s.recv(1).decode())
        print(succ, "successful!")
        for i in range(succ):
            print(s.recv(1024).decode())
            time.sleep(0.0005)

