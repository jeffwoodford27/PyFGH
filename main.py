import csv
import os
import paramiko
import GUI
from util import pyfghutil
from multiprocessing import Process, Queue, Pool
import GUItoCalc as GTC
from multiprocessing import Pool
import time
from util import DataObject
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
    # print("Filename: ", holder1.file_name)
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



    def SSH_connection():
        #TODO Make new files for the remote main!
        #TODO Add these variables to the remote files!

        DataObject.test.testing = holder1
        DataObject.test.N1 = holder1.N1
        DataObject.test.N2 = holder1.N2
        DataObject.test.N3 = holder1.N3
        DataObject.test.L1 = holder1.L1
        DataObject.test.L2 = holder1.L2
        DataObject.test.L3 = holder1.L3
        print("N1: ", DataObject.test.N1)

        header = [holder1.N1, holder1.N2, holder1.N3, holder1.L1, holder1.L2, holder1.L3]
        header2 = [holder1.PES]
        header3 = [holder1.EquilMolecule]

        with open('countries.csv', 'w', encoding='UTF8') as j:
            writer = csv.writer(j)

            # write the header
            writer.writerow(header)

            # write the data
            #writer.writerow(data)

            #writer.writerow(data2)
            f.close()

        with open('PES.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(header2)

            # write the data
            #writer.writerow(data)

            #writer.writerow(data2)
            f.close()

        with open('EquilMolecule.csv', 'w', encoding='UTF8') as a:
            writer = csv.writer(a)

            # write the header
            writer.writerow(header3)

            # write the data
            #writer.writerow(data)

            #writer.writerow(data2)
            a.close()

        host = "euclid.chem.missouriwestern.edu" #holder1.host
        port = 22
        username = "jrandleman" #holder1.user
        password = "Huskers1"#holder1.password

        command = "python3 RemoteMain.py"
        command2 = "rm RemoteMain.py"
        command3 = "rm GUItoCalc.py"
        command4 = "rm Vmatrix.py"
        command5 = "rm Tmatrix.py"
        command6 = "rm Gmatrix.py"
        command7 = "rm -vr util"
        command8 = "rm -vr __pycache__"

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        sftp = ssh.open_sftp()

        path12 = "/home/" + username + "/EquilMolecule.csv"
        localpath12 = "EquilMolecule.csv"
        sftp.put(localpath12, path12)

        path11 = "/home/" + username + "/PES.csv"
        localpath11 = "PES.csv"
        sftp.put(localpath11, path11)

        path10 = "/home/" + username + "/countries.csv"
        localpath10 = "countries.csv"
        sftp.put(localpath10, path10)

        path = "/home/" + username + "/RemoteMain.py"
        localpath = "RemoteMain.py"
        sftp.put(localpath, path)

        path1 = "/home/" + username + "/RemoteGUItoCalc.py"
        localpath1 = "RemoteGUItoCalc.py"
        sftp.put(localpath1, path1)

        path2 = "/home/" + username + "/RemoteVmatrix.py"
        localpath2 = "RemoteVmatrix.py"
        sftp.put(localpath2, path2)

        path3 = "/home/" + username + "/RemoteTmatrix.py"
        localpath3 = "RemoteTmatrix.py"
        sftp.put(localpath3, path3)

        path4 = "/home/" + username + "/RemoteGmatrix.py"
        localpath4 = "RemoteGmatrix.py"
        sftp.put(localpath4, path4)

        command10 = "mkdir util"

        stdin, stdout, stderr = ssh.exec_command(command10)

        path5 = "/home/" + username + "/util/DataObject.py"
        localpath5 = "./util/DataObject.py"
        sftp.put(localpath5, path5)

        path6 = "/home/" + username + "/util/model_objects.py"
        localpath6 = "./util/model_objects.py"
        sftp.put(localpath6, path6)

        path7 = "/home/" + username + "/util/pyfghutil.py"
        localpath7 = "./util/pyfghutil.py"
        sftp.put(localpath7, path7)
        """
        stdin, stdout, stderr = ssh.exec_command(command)
        stdin, stdout, stderr = ssh.exec_command(command2)
        stdin, stdout, stderr = ssh.exec_command(command3)
        stdin, stdout, stderr = ssh.exec_command(command4)
        stdin, stdout, stderr = ssh.exec_command(command5)
        stdin, stdout, stderr = ssh.exec_command(command6)
        stdin, stdout, stderr = ssh.exec_command(command7)
        stdin, stdout, stderr = ssh.exec_command(command8)
        """

        """
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
                #stdin, stdout, stderr = ssh.exec_command(command4)

        """

        sftp.close()
        ssh.close()

    if holder1.remote == 1:
        SSH_connection()

        GTC.passToCalc(holder1)
        q.put("object on queue")

    else:
        GTC.passToCalc(holder1)
        q.put("object on queue")

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

    # At this point, insert the data into the handler

    ReturnData = q.get()  # an object of type OutputData
    print(ReturnData)
    return


if __name__ == '__main__':
    datagrabber()
    print('done')
