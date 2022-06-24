import multiprocessing as mp
import numpy as np

def f(x,y):
    foo = np.zeros((2,2),dtype=float)
    foo[0,0] = x
    foo[0,1] = y
    foo[1,0] = -y
    foo[1,1] = -x
    return foo

if __name__ == '__main__':
    p = mp.Pool(2)
    paramz = [(1,2),(3,4)]
    blocks = p.starmap(f, paramz)
    p.close()

    print(blocks[0])