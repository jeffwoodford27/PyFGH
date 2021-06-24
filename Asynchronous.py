import time
from multiprocessing import Process, Lock, Queue
import os
from util import InputData



def info(title,):
    print(title)

    print('process id:', os.getpid())



def parent():
    print('The interface is started')
    import GUI


def child(lock, sleepTime):
    lock.acquire()
    info('child process 1',)
    #total.put(x + y)
    print('variables are retrieved')
    lock.release()
    time.sleep(sleepTime)


if __name__ == '__main__':
    lock = Lock()
    total = Queue()
    info('Parent process',)
    parent()
    p = Process(target=child, args=(lock, 3))
    p.start()
    p.join()
    print(InputData.output.items.molecule)
    print(InputData.output.items.N1)
    print('done')

    #print(total.get())
