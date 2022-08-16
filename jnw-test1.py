import numpy as np
import sys
import time

#This testing file has an improved method for converting between point number and the multidimensional index.

def IndexToPoint(D,N,idx):
    pt = idx[D-1]
    for j in reversed(range(D-1)):
        pt = pt * N[j]
        pt = pt + idx[j]
    return pt

def IndexToPointOld(D,N,idx):
    pt = idx[0]
    for j in range(1,D):
        pt = pt * N[j]
        pt = pt + idx[j]
    return pt

def PointToIndexOld(D,N,pt):
    idx = np.zeros(D,dtype=int)
    p = pt
    for j in range(D-1,-1,-1):
        idx[j] = p % N[j]
        p = p // N[j]
    return idx

def PointToIndex(D,N,pt):
    idx = np.zeros(D,dtype=int)
    p = pt
    for j in range(D):
        idx[j] = p % N[j]
        p = p // N[j]
    return idx

class MatrixObj:
    def __init__(self,D,N,dtype):
        self.D = D
        self.N = N
        self.Npt = np.prod(N)
        self.matrix = np.zeros((self.Npt,self.Npt),dtype=dtype)

    def setValueByPoint(self,pt1,pt2,val):
        self.matrix[pt1][pt2] = val
        return

    def setValueByIndex(self,idx1,idx2,val):
        self.matrix[IndexToPoint(self.D,self.N,idx1)][IndexToPoint(self.D,self.N,idx2)] = val
        return

    def getValueByPoint(self,pt1,pt2):
        return self.matrix[pt1][pt2]

    def getValueByIndex(self,idx1,idx2):
        return self.matrix[IndexToPoint(self.D,self.N,idx1)][IndexToPoint(self.D,self.N,idx2)]


def AlphaAndBetaToCounter(alpha, beta, D, NValues):
    counter = np.zeros(D * 2, int)
    # I am uncertain about the ability to modify the input parameters,
    # for now, I will create duplicate variables
    modalpha = alpha
    modbeta = beta
    # alpha first
    for x in range(D):
        # print("Current modalpha is: "+str(modalpha))
        if (not x + 1 == D):
            npprod = np.prod(NValues[:D - (x + 1)])

            manytimesalpha = modalpha // (npprod)
            modalpha -= manytimesalpha * (npprod)
            manytimesbeta = modbeta // (npprod)
            modbeta -= manytimesbeta * (npprod)
        else:
            manytimesalpha = modalpha // 1
            modalpha -= manytimesalpha
            manytimesbeta = modbeta // 1
            modbeta -= manytimesbeta
        # Set Values
        counter[(x * 2) + 1] = manytimesalpha
        counter[(x * 2)] = manytimesbeta

    return counter

def NewCounter(D,  N, alpha, beta):
    alphaidx = PointToIndex(D, N, alpha)
    betaidx = PointToIndex(D, N, beta)
    counter = np.zeros(D * 2, int)
    for j in range(D):
        counter[2 * j] = betaidx[D - j - 1]
        counter[2 * j + 1] = alphaidx[D - j - 1]
    return counter

#D = 3
#N = [11,11,11]

D = 3
N = [3,3,3]

Npt = np.prod(N)

for alpha in range(Npt):
    for beta in range(Npt):
        print(alpha,beta,NewCounter(D,N,alpha,beta))



#for pt in range(Npt):
#    print(pt,PointToIndex(D,N,pt),IndexToPoint(D,N,PointToIndex(D,N,pt)))

#t0 = time.perf_counter()
#for alpha in range(Npt):
#    print ("alpha = " + str(alpha))
#    for beta in range(Npt):
#        nelsoncounter = AlphaAndBetaToCounter(alpha,beta,D,N)
#        jeffcounter = NewCounter(D,N,alpha,beta)
#        print(n, nelsoncounter, jeffcounter)
#t1 = time.perf_counter()
#print(t1-t0)
#print(sys.getsizeof(nelsoncounter))

#t0 = time.perf_counter()
#for alpha in range(Npt):
#    print ("alpha = " + str(alpha))
#    for beta in range(Npt):
#        nelsoncounter = AlphaAndBetaToCounter(alpha,beta,D,N)
#        print(alpha,beta,nelsoncounter)
#        jeffcounter = NewCounter(D,N,alpha,beta)
#        print(alpha, beta, jeffcounter)
#t1 = time.perf_counter()
#print(t1-t0)
#print(sys.getsizeof(jeffcounter))


