import multiprocessing
import select
from time import sleep
from random import *
import threading

def consumer(outputp):
    outputp.send("No, fuck you!")

def readp(inputp):
    inputp.send('fuck you!')
    print(inputp.recv())

if __name__=="__main__":
    (output_p,input_p)=multiprocessing.Pipe()
    #启动使用者进程
    output_p.send("aaaa")
    input_p.send("????")
    print(output_p.recv())
