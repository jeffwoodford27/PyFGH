import numpy as np
import scipy
from scipy import linalg
import sys
import pyfghutil
import Tmatrix2
import Vmatrix2
import Gmatrix2
import pandas

np.set_printoptions(threshold=sys.maxsize)

def getPotentialEnergySurface(atomlist, NValues, fname):
    df = pandas.read_csv(fname,names=['q1','q2','q3','x1','y1','x2','y2','x3','y3','en'])
    pes = pyfghutil.PotentialEnergySurface(atomlist, NValues, df)
    return pes

atomlist = []
atomlist.append(pyfghutil.Atom(8,16))
atomlist.append(pyfghutil.Atom(1,1))
atomlist.append(pyfghutil.Atom(1,1))
dimensions = 3
NValue = np.zeros(dimensions,int)
NValue[0] = 7
NValue[1] = 7
NValue[2] = 7
LValue = np.zeros(dimensions,float)
LValue[0] = 0.7
LValue[1] = 0.7
LValue[2] = 0.7
Tapprox = 4
Vtype = "File"

if (Vtype == "File"):
    PES = getPotentialEnergySurface(atomlist, NValue, "waterpot-data.csv")
    GMatrix = Gmatrix2.calcGMatrix(atomlist, NValue, PES)
else:
    PES = None
    GMatrix = None

if (Vtype == "Model"):
    Vmodel = []
    Vmodel.append(pyfghutil.HarmonicOscillatorModel(919,0.37))
    Vmodel.append(pyfghutil.HarmonicOscillatorModel(919,0.37))
    Vmodel.append(pyfghutil.HarmonicOscillatorModel(919,0.37))
    #Vmodel.append(pyfghutil.MorseOscillatorModel(919,0.149302,1.151087))
    #Vmodel.append(pyfghutil.MorseOscillatorModel(919,0.149302,1.151087))
    #Vmodel.append(pyfghutil.MorseOscillatorModel(919,0.149302,1.151087))
else:
    Vmodel = None
params = pyfghutil.Parameters(dimensions, NValue, LValue, Tapprox, Vtype, Vmodel, PES, GMatrix)
tmatrix = Tmatrix2.TMatrixCalc(params, dimensions)
vmatrix = Vmatrix2.VMatrixCalc(params, dimensions)
hmatrix = tmatrix + vmatrix
eigenval = np.sort(scipy.linalg.eigvals(hmatrix))*219474.6
print(eigenval)
print(eigenval[1]-eigenval[0])
print(eigenval[2]-eigenval[0])
print(eigenval[3]-eigenval[0])
