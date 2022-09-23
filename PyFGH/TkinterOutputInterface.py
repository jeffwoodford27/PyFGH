import numpy as np



class WavefunctionData:
    def __init__(self,wfn):
        self.wfn = wfn

    def displayGraph(self):
        x = np.array([(i*0.15 - 0.75) for i in range(11)], dtype=float)
        # in this method, take the data stored in self.wfn and create a graph
        pass


Neig = 10
wfn = np.zeros([Neig,11],dtype=float)

wfn[0] = [5.620948663068036e-09, 7.516713986034454e-09, 3.5815783726449676e-08, 1.429761598530566e-08, 4.0423797837071565e-08, 5.018620962751152e-08, 2.9200717614568785e-08, 9.90464098883949e-09, 2.5516302823135235e-09, -1.0053198802988102e-10, 6.892598644053881e-10]

wfnobj = []
for i in range(Neig):
    wfnobj.append(WavefunctionData(wfn[i]))
    
# your code here to create the window

# on click of a button:

    btn.append(Button(master,text=num1[i],command=wfnobj[i].displayGraph))

