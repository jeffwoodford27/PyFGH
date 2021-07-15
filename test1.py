import os

from self import self

import GUI
from util import DataObject
from multiprocessing import Process, Lock, Queue


# This is the parent process
def parent(q):
    GUI.main_window()
    print('The interface is started')
    print(os.getpid())
    holder = DataObject.InputData()
    holder.setN1(DataObject.holdData.N1)
    holder.setN2(DataObject.holdData.N2)
    q.put(holder)
    return


# This is the child process
# Do something then pass the results back to the parent
# child back to the parent
def child1(q):
    print('This is the child process ', os.getpid())
    holder1 = q.get()
    print(holder1.N1, holder1.N2)
    return


if __name__ == '__main__':
    """
    parent()  # This is the parent process
    child1()  # This is the child process
    """
    q = Queue()
    parent(q)
    p2 = Process(target=child1, args=(q,))
    p2.start()
    p2.join()
    print('done')
