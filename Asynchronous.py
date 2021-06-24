import time
from multiprocessing import Process, Lock, Queue
import os
from util import InputData


def info(title, ):
    print(title)

    print('process id:', os.getpid())


def parent():
    print('The interface is started')
    import GUI


def child1(lock, sleepTime):
    lock.acquire()
    info('child process 1', )
    # total.put(x + y)
    print('variables are retrieved')
    lock.release()
    time.sleep(sleepTime)


def child2():
    info('child process 2', )
    print(int(InputData.output.items.N1) + int(InputData.output.items.N2))


if __name__ == '__main__':
    lock = Lock()
    total = Queue()
    info('Parent process', )
    parent()
    p = Process(target=child1, args=(lock, 3))
    p.start()
    p.join()
    child2()
    print('done')

    # print(total.get())
