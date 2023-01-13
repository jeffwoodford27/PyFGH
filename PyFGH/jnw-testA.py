from multiprocessing import Process, Queue
import threading
from threading import Thread
import time

def f(q):
    print('entering f')
    inputitem = q.get()
    print(str(inputitem) + ' taken from queue')
    outputitem = [50,200,2]
    if (inputitem[1] == 20):
        raise Exception("foo")
    q.put(outputitem)
    return

if __name__ == '__main__':
    q = Queue()

    inputitem = [10, 20, 30]
    p = Thread(target=f, args=(q,))
    p.start()
    time.sleep(1)
    q.put(inputitem)
    try:
        p.join()
    except Exception as e:
        print("from parent, exception is "+str(e))
    outputitem = q.get()
    print('received outputitem = '+str(outputitem))
