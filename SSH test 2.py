import os

import paramiko

"""
This here works!!!
"""

host = "woz.cs.missouriwestern.edu"
port = 22
username = "jrandleman"
password = "csc274.."

command = "ls"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port, username, password)

sftp = ssh.open_sftp()

path = "/home/jrandleman/GUI.py"
localpath = "GUI.py"
sftp.put(localpath, path)

sftp.close()
ssh.close()
"""
stdin, stdout, stderr = ssh.exec_command(command)
lines = stdout.readlines()
print(lines)
"""
