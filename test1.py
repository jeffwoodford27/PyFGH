import os
import time

import GUI
from util import DataObject
from multiprocessing import Process, Lock, Queue

"""
This one uses Queues
"""


# This is the parent process
def parent(q):
    print('This is the parent process: ', os.getpid())
    holder1 = q.get()
    print(holder1.message)
    print("Molecule: ", holder1.molecule)
    print("Q1 equation: ", holder1.q_equation1)
    print("Q2 equation: ", holder1.q_equation2)
    print("Q3 equation: ", holder1.q_equation3)
    print("N1: ", holder1.N1)
    print("L1: ", holder1.L1)
    print("N2: ", holder1.N2)
    print("L2: ", holder1.L2)
    print("N3: ", holder1.N3)
    print("L3: ", holder1.L3)
    print("T : ", holder1.t)
    print("G : ", holder1.g)
    print("V : ", holder1.v)
    print("Values from the sum of N and L: ", holder1.sum)
    # print("File Name : ", holder1.file_name, " This is from the child process")
    # print("Model Data : ", holder1.model_data, " This is from the child process")

    return


def child1():
    q = Queue()
    p1 = Process(target=parent, args=(q,))
    p1.start()
    time.sleep(1)
    GUI.main_window()
    print('The interface is started Process: ', os.getpid())
    holder = DataObject.InputData()

    holder.setMolecule(DataObject.holdData.molecule)
    holder.setQ1(DataObject.holdData.q_equation1)
    holder.setQ2(DataObject.holdData.q_equation2)
    holder.setQ3(DataObject.holdData.q_equation3)
    holder.setN1(DataObject.holdData.N1)
    holder.setL1(DataObject.holdData.L1)
    holder.setN2(DataObject.holdData.N2)
    holder.setL2(DataObject.holdData.L2)
    holder.setN3(DataObject.holdData.N3)
    holder.setL3(DataObject.holdData.L3)
    holder.setT(DataObject.holdData.t)
    holder.setG(DataObject.holdData.g)
    holder.setV(DataObject.holdData.v)
    holder.setFileName(DataObject.holdData.file_name)
    v = int(DataObject.holdData.N1) + int(DataObject.holdData.N2) + int(DataObject.holdData.N3) + int(DataObject.holdData.L1) + \
        int(DataObject.holdData.L2) + int(DataObject.holdData.L3)
    holder.setMessage("This is from the child")
    holder.set_sum(v)
    # holder.setModelData(DataObject.holdData.model_data)  # look into pickling possibly un-pickling
    q.put(holder)


if __name__ == '__main__':
    child1()
    print('done')
