import multiprocessing

import GUI

"""
This is the API to share data between files. When you test the code out, run the code from API.py and not GUI.py. Only 
because if you run the code from GUI.py the variables will not transfer to the API class. So when testing the code out, 
just run it from API.py. For the variables to transfer to API.py, in the GUI hit calculate and then select either yes or no
from the next box. FYI these boxes do the same thing right now. Once you select either yes or no, the window will be destroyed
and the variables will transfer from GUI.py into API.py. 

Once the GUI window is destroyed, you can access the variables by using GUI. and then entering the filename. For example,
GUI.molecule_api will return the molecule that was selected. 

Also there is an error with selecting a file for the equilibrium coordinates. I am working on it. For testing purposes,
just skip that part for now. 

Author: Josiah Randleman
"""
#TODO: possibly make a restart button


class API:

    print('This CPU has ', multiprocessing.cpu_count(), ' cores.')
    print('Molecule is: ' + GUI.molecule_api)
    print('Q\u2081 is: ' + GUI.q_equation1_api)
    print('Q\u2082 is: ' + GUI.q_equation2_api)
    print('Q\u2083 is: ' + GUI.q_equation3_api)
    print('N\u2081 is: ' + GUI.text1_api)
    print('L\u2081 is: ' + GUI.text2_api)
    print('N\u2082 is: ' + GUI.text3_api)
    print('L\u2082 is: ' + GUI.text4_api)
    print('N\u2083 is: ' + GUI.text5_api)
    print('L\u2083 is: ' + GUI.text6_api)
    print('T is: ' + GUI.t_api)
    print('G is: ' + GUI.g_api)
    print('V for Q\u2081: ' + GUI.v1_api)
    print('V for Q\u2082: ' + GUI.v2_api)
    print('V for Q\u2083: ' + GUI.v3_api)
