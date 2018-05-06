#!/usr/bin/python3

# Author: GMFTBY
# Time  : 2018.5.5

'''
This script with the server.py to test whether the server work well
'''

import socket, time

if __name__ == "__main__":
    host = ''
    port = 50000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(b'Hello world!')
        time.sleep(100)
