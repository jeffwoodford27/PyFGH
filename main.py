import os
import paramiko
import GUI
from util import pyfghutil
from multiprocessing import Process, Queue, Pool
import GUItoCalc as GTC
from multiprocessing import Pool
import time
from tqdm import *

"""
This one uses Queues
This communicates by using SSH
Also connected to test3.py
Author: Josiah Randleman
© Copyright 2021, Josiah Randleman, All rights reserved. jrandl516@gmail.com
"""

# This is the parent process
def datamuncher(q):
    print('This is the child process: ', os.getpid())
    holder1 = q.get()
    print(holder1.message)
    print("N1: ", holder1.N1)
    print("L1: ", holder1.L1)
    print("N2: ", holder1.N2)
    print("L2: ", holder1.L2)
    print("N3: ", holder1.N3)
    print("L3: ", holder1.L3)
    #print("Filename: ", holder1.file_name)
    data = [holder1.equilibrium_file, holder1.N1, holder1.L1, holder1.N2,
            holder1.L2, holder1.N3, holder1.L3]



    print("Energy from Main: ", holder1.PES.pts[0].en)
    save_path = "./resources/"
    file_name = "DataList.txt"
    completeName = os.path.join(save_path, file_name)
    file = open(completeName, "w", encoding="utf-8")
    for x in data:
        file.write('%s\n' % x)
    file.close()

    #GTC.passToCalc(holder1)

    q.put("object on queue")

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

# this is the parent process
def datagrabber():
    q = Queue()
    p1 = Process(target=datamuncher, args=(q,))
    p1.start()
    time.sleep(1)
    holder = GUI.main_window()
    print('The interface is started Process: ', os.getpid())

    holder.setMessage("This is from the parent")
    # holder.setModelData(DataObject.holdData.model_data)  # look into pickling possibly un-pickling
    q.put(holder)

    #At this point, insert the data into the handler

    ReturnData = q.get()  # an object of type OutputData
    print(ReturnData)
    return


if __name__ == '__main__':
    datagrabber()
    print('done')
