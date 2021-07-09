import time
from multiprocessing import Process, Lock, Queue


from util import InputData

# This is the parent process
def parent():
    print('The interface is started')
    import GUI



# This is the child process
# Do something then pass the results back to the parent
# child back to the parent
def child1():
    print('THis is the child process')
    print(InputData.output.items.model_data, ' This is from the child process')
    print(InputData.output.items.molecule, ' This is from the child process')
    print(InputData.output.items.q_equation1, ' This is from the child process')
    print(InputData.output.items.q_equation2, ' This is from the child process')
    print(InputData.output.items.q_equation3, ' This is from the child process')
    print(InputData.output.items.N1, ' This is from the child process')
    print(InputData.output.items.L1, ' This is from the child process')
    print(InputData.output.items.N2, ' This is from the child process')
    print(InputData.output.items.L2, ' This is from the child process')
    print(InputData.output.items.N3, ' This is from the child process')
    print(InputData.output.items.L3, ' This is from the child process')
    print(InputData.output.items.t, ' This is from the child process')
    print(InputData.output.items.g, ' This is from the child process')
    print(InputData.output.items.v, ' This is from the child process')
    print(InputData.output.items.model_data, ' This is from the child process')


if __name__ == '__main__':
    parent()  # This is the parent process
    child1()  # This is the child process
    print('done')
