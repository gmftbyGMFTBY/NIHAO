import multiprocessing
import select
from time import sleep
from random import *
import threading

class test:
    def __init__(self):
        self.a = 1
    def run(self):
        while True:
            print(1)

def consumer(outputp):
    print(outputp.recv())
    outputp.send("No, fuck you!")

def readp(inputp):
    inputp.send('fuck you!')
    print(inputp.recv())

if __name__=="__main__":
    #(output_p,input_p)=multiprocessing.Pipe()
    #启动使用者进程
    a = test()
    cons_p = threading.Thread(target=test.run, args=(test,))
    cons_p.start()

    #read_p = multiprocessing.Process(target=readp,args=(input_p, ))
    #read_p.start()
