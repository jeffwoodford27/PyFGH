import os
import time
import paramiko
import GUI
from util import DataObject
from multiprocessing import Process, Queue

"""
This one uses Queues
This communicates by using SSH
Also connected to test3.py
Author: Josiah Randleman
© Copyright 2021, Josiah Randleman, All rights reserved. jrandl516@gmail.com
"""


class Bob:
    def __init__(self):
        self.sum = 0

    def setSum(self, sum):
        self.sum = sum
        return


# This is the parent process
def datamuncher(q):
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
    print("Filename: ", holder1.file_name)
    print("V : ", holder1.v)
    print("Values from the sum of N and L: ", holder1.sum)
    data = [holder1.molecule, holder1.q_equation1, holder1.q_equation2,
            holder1.q_equation3, holder1.N1, holder1.L1, holder1.N2,
            holder1.L2, holder1.N3, holder1.L3, holder1.t,
            holder1.g, holder1.v]
    save_path = "./resources/"
    file_name = "DataList.txt"
    completeName = os.path.join(save_path, file_name)
    file = open(completeName, "w", encoding="utf-8")
    for x in data:
        file.write('%s\n' % x)
    file.close()

    DataObject.holdData.user2 = holder1.user


    def SSH_connection():
        host = holder1.host
        port = 22
        username = holder1.user
        password = holder1.password
        command = "python3 test3.py"
        command2 = "rm DataList.txt"
        command3 = "rm test3.py"
        command4 = "rm Results.txt"

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        sftp = ssh.open_sftp()

        path = "/home/" + username + "/DataList.txt"
        localpath = "./resources/DataList.txt"
        sftp.put(localpath, path)
        path2 = "/home/" + username + "/test3.py"
        localpath2 = "test3.py"
        sftp.put(localpath2, path2)
        stdin, stdout, stderr = ssh.exec_command(command)
        stdin, stdout, stderr = ssh.exec_command(command2)
        stdin, stdout, stderr = ssh.exec_command(command3)
        path3 = "/home/" + username + "/Results.txt"
        localpath3 = "./resources/Results.txt"
        sftp.get(path3, localpath3)
        stdin, stdout, stderr = ssh.exec_command(command4)
        sftp.close()
        ssh.close()



    if holder1.remote == 'Yes':
        SSH_connection()

    Charles = Bob()
    Charles.setSum(holder1.sum)
    q.put(Charles)
    # print("File Name : ", holder1.file_name, " This is from the child process")
    # print("Model Data : ", holder1.model_data, " This is from the child process")
    return


def datagrabber():
    q = Queue()
    p1 = Process(target=datamuncher, args=(q,))
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
    v = int(DataObject.holdData.N1) + int(DataObject.holdData.N2) + int(DataObject.holdData.N3) + int(
        DataObject.holdData.L1) + \
        int(DataObject.holdData.L2) + int(DataObject.holdData.L3)
    holder.setMessage("This is from the child")
    holder.set_sum(v)
    holder.set_host(DataObject.holdData.host)
    holder.set_user(DataObject.holdData.user)
    holder.set_password(DataObject.holdData.password)
    holder.set_remote(DataObject.holdData.remote)
    # holder.setModelData(DataObject.holdData.model_data)  # look into pickling possibly un-pickling
    q.put(holder)
    Charles = q.get()
    print(Charles.sum)

    return


if __name__ == '__main__':
    datagrabber()
    print('done')
