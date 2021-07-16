import os

from self import self

import GUI
from util import DataObject
from multiprocessing import Process, Lock, Queue


# This is the parent process
def parent(q):
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
    # holder.setModelData(DataObject.holdData.model_data)
    q.put(holder)
    return


# This is the child process
# Do something then pass the results back to the parent
# child back to the parent
def child1(q):
    print('This is the child process: ', os.getpid())
    holder1 = q.get()
    print("Molecule: ", holder1.molecule, " This is from the child process")
    print("Q1 equation: ", holder1.q_equation1, " This is from the child process")
    print("Q2 equation: ", holder1.q_equation2, " This is from the child process")
    print("Q3 equation: ", holder1.q_equation3, " This is from the child process")
    print("N1: ", holder1.N1, " This is from the child process")
    print("L1: ", holder1.L1, " This is from the child process")
    print("N2: ", holder1.N2, " This is from the child process")
    print("L2: ", holder1.L2, " This is from the child process")
    print("N3: ", holder1.N3, " This is from the child process")
    print("L3: ", holder1.L3, " This is from the child process")
    print("T : ", holder1.t, " This is from the child process")
    print("G : ", holder1.g, " This is from the child process")
    print("V : ", holder1.v, " This is from the child process")
    # print("File Name : ", holder1.file_name, " This is from the child process")
    # print("Model Data : ", holder1.model_data, " This is from the child process")

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
