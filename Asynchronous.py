import time
from multiprocessing import Process, Lock,  Queue
import os


def parent(title, x, y):
    print(title)

    print('process id:', os.getpid())



def child(lock, total, x, y, sleepTime):
    lock.acquire()
    parent('child process 1', 10, 10)
    total.put(x+y)
    print('x and y are added')
    lock.release()
    time.sleep(sleepTime)



if __name__ == '__main__':
    lock = Lock()
    total = Queue()
    parent('Parent process', 10, 10)
    print('created x and y in the parent')
    p = Process(target=child, args=(lock, total, 10, 10, 3))
    p.start()
    p.join()
    print(total.get())
