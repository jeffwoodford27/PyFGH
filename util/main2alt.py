import numpy as np
import scipy
from scipy import linalg
import sys
import pyfghutil
import Tmatrix as Tmatrix2
import Vmatrix as Vmatrix2
import Gmatrix2
import pandas

np.set_printoptions(threshold=sys.maxsize)

def getPotentialEnergySurface(atomlist, NValues, fname):
    df = pandas.read_csv(fname,names=['q1','q2','q3','x1','y1','x2','y2','x3','y3','en'])
    pes = pyfghutil.PotentialEnergySurface(atomlist, NValues, df)
    return pes
def mainFunc():
    atomlist = []
    atomlist.append(pyfghutil.Atom(8,16))
    atomlist.append(pyfghutil.Atom(1,1))
    atomlist.append(pyfghutil.Atom(1,1))
    dimensions = 3
    NValue = [0]*dimensions
    NValue[0] = 7
    NValue[1] = 7
    NValue[2] = 7
    LValue = [0]*dimensions
    LValue[0] = 0.7
    LValue[1] = 0.7
    LValue[2] = 0.7
    Tapprox = 3
    Vtype = "File"

    if (Vtype == "File"):
        PES = getPotentialEnergySurface(atomlist, NValue, "waterpot-data.csv")
        #GMatrix = Gmatrix2.calcGMatrix(atomlist, NValue, PES)
        GMatrix = Gmatrix2.calcGMatrix(atomlist, NValue, PES, None)
        Vmodel = None
        
    if (Vtype == "Model"):
        Vmodel = []
        Vmodel.append(pyfghutil.HarmonicOscillatorModel(919,0.37))
        Vmodel.append(pyfghutil.HarmonicOscillatorModel(919,0.37))
        Vmodel.append(pyfghutil.HarmonicOscillatorModel(919,0.37))
        mu = [919]*3
        
        PES = None
        GMatrix = Gmatrix2.calcGMatrix(atomlist, NValue, None, mu)
        #Vmodel.append(pyfghutil.MorseOscillatorModel(919,0.149302,1.151087))
        #Vmodel.append(pyfghutil.MorseOscillatorModel(919,0.149302,1.151087))
        #Vmodel.append(pyfghutil.MorseOscillatorModel(919,0.149302,1.151087))
    params = pyfghutil.Parameters(dimensions, NValue, LValue, Tapprox, Vtype, Vmodel, PES, GMatrix)
    print("TMat")
    tmatrix = Tmatrix2.TMatrixCalc(params, dimensions)
    #pandas.DataFrame(tmatrix).to_csv("TMat.csv")
    print("VMat")
    vmatrix = Vmatrix2.VMatrixCalc(params, dimensions)
    print("HMat")
    hmatrix = tmatrix + vmatrix
    print("Eigen")
    eigenval = np.sort(scipy.linalg.eigvals(hmatrix))*219474.6
    print(eigenval)
    print(eigenval[1]-eigenval[0])
    print(eigenval[2]-eigenval[0])
    print(eigenval[3]-eigenval[0])
if __name__ == "__main__":
	mainFunc()
