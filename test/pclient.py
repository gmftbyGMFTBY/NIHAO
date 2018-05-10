#!/usr/bin/python3

# Author: GMFTBY
# Time  : 2018.5.5

'''
This script with the server.py to test whether the server work well
'''

import socket, time

host = ''
port = 50000

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.send(b'lantian')
        time.sleep(0.0005)
        s.send(b'lt970106')

        time.sleep(0.01)

        '''
        # get the user table from the server
        s.send(b'1')
        time.sleep(0.01)
        s.send(b'12')
        time.sleep(0.01)
        s.send(b'lantian')
        time.sleep(0.01)

        t = s.recv(1).decode()
        for i in range(int(t)):
            time.sleep(0.01)
            print(s.recv(1024))
        '''

        # talk to myself
        # send the file
        '''
        data = []
        with open('test.py') as f:
            while True:
                res = f.read(1020).encode()
                if res: data.append(res)
                else: break

        s.send(str(len(data) + 3).encode())
        time.sleep(0.05)
        s.send(b'11')
        time.sleep(0.05)
        s.send(b'lantian')
        time.sleep(0.005)
        s.send(b'1')
        time.sleep(0.05)
        s.send(b'lantian')
        time.sleep(0.05)
        for res in data: s.send(res)

        print(s.recv(1024))
        time.sleep(0.05)
        count = s.recv(1020).decode()
        time.sleep(0.05)
        with open("./fuck", 'w') as f:
            for i in range(int(count)):
                time.sleep(0.05)
                f.write(s.recv(1020).decode())
        print("write successfully !")

        # feedback
        succ = int(s.recv(1).decode())
        print(succ, "successful!")
        for i in range(succ):
            print(s.recv(1024).decode())
            time.sleep(0.0005)
        '''
        # become the friend
        s.send(b'2')
        time.sleep(0.01)
        s.send(b'7')
        time.sleep(0.01)
        s.send(b"lantian")
        time.sleep(0.01)
        s.send(b"lantian")
        print(s.recv(1024))

