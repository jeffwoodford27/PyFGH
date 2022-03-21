import getpass

"""
Author: Josiah Randleman
© Copyright 2021, Josiah Randleman, All rights reserved. jrandl516@gmail.com
"""

# Linux
# Windows ./resources/DataList.txt
username = getpass.getuser()
with open("/home/" + username + "/DataList.txt",  encoding="utf-8") as open_file:
    lines = open_file.readlines()
    a = 0
    x1 = lines[4].strip('\n')
    x2 = lines[5].strip('\n')
    #save_path = "./resources/"
    file_name = "Results.txt"
    #completeName = os.path.join(save_path, file_name)
    file = open(file_name, "w", encoding="utf-8")
    y = float(x1) + float(x2)
    results = [y]
    for x in results:
        file.write('%s\n' % x)
    file.close()
    #print(float(x1) + float(x2))