import numpy as np
import scipy as scipy
import scipy.linalg
import math
import sys
import pandas as pd
from pathlib import Path
import csv

class InputError(Exception):
    def __init__(self,msg):
        self.message = msg

# Input: a prompt for keyboard entry of an integer, the min and max values that the integer may have
# Output: The integer that is input, provided that is falls between intmin and intmax
        
def inputValidInt (prompt, intmin, intmax):
    validinput = False
    while (not validinput):
        inputint = input(prompt)
        if (type(inputint) is int):
            for i in range(intmin,intmax+1):
                if (inputint == i):
                    validinput = True
                    break
    return inputint

# Input: a prompt for keyboard entry of a float
# Output: The float that is input, provided that it is nonnegative.

def inputNonNegativeFloat (prompt):
    validinput = False
    while (not validinput):
        inputfloat = input(prompt)
        if (type(inputfloat) is int):
            inputfloat = float(inputfloat)
        if ((type(inputfloat) is float) and (inputfloat >= 0)):
            validinput = True
    return inputfloat

# Input: a prompt for keyboardd entry of a float
# Output: the float that is input, provided that it is positive.

def inputPositiveFloat (prompt):
    validinput = False
    while (not validinput):
        inputfloat = input(prompt)
        if (type(inputfloat) is int):
            inputfloat = float(inputfloat)
        if ((type(inputfloat) is float) and (inputfloat > 0)):
            validinput = True
    return inputfloat

# Input: a prompt for keyboard entroy of a float
# Output: The float that is input (may be any float).

def inputFloat (prompt):
    validinput = False
    while (not validinput):
        inputfloat = input(prompt)
        if (type(inputfloat) is int):
            inputfloat = float(inputfloat)
        if (type(inputfloat) is float):
            validinput = True
    return inputfloat

# Input: a prompt for keyboard entry of a filename
# Output: The filename, provided that the file exists.

def inputValidFilename (prompt):
    validinput = False
    while (not validinput):
        fname = raw_input(prompt)
        if (Path(fname).is_file()):
            validinput = True
        else:
            print ("file not found\n")
    return fname

# Object storing the parameters for the Harmonic Oscillator model.
# V(q) = (1/2)kq^2
# mu is needed for the kinetic energy calculation.

class HarmonicOscillatorModel:
    def __init__(self):
        self.k = inputPositiveFloat("\nEnter k (in units of hartree/bohr^2) :\n")

# Object storing the parameters for the Morse Oscillator Model:
# V(q) = De*(1-exp(-a*q))^2
# mu is needed for the kinetic energy calculation.
        
class MorseOscillatorModel:
    def __init__(self):
        self.De = inputPositiveFloat("\nEnter De (in units of hartree):\n")
        self.a = inputPositiveFloat("\nEnter a (in units of bohr^-1):\n")

# The class that holds the calculation parameters needed for the FGH calculation to proceed.
        
class Molecule:
    def __init__(self, D, Vinput):

        # Input the number of points per dimension.  N must be odd for the FGH method.
        
        self.N = self.inputN(D)

        # Input the length of each dimension.  Must be a positive float.
        
        self.L = self.inputL(D)

        # Input the reduced mass of each dimension.  Must be a positive float.
        
        self.mu = self.inputmu(D)

        # Input how the potential energy is to be computed.
        # If Vinput = 0: a model function is used.  The model object is stored in the Vmodel list, and the type of model is stored in the Vtype array.
        # If Vinput = 1: data is read from a CSV file.  The data is stored in Vdata.  There must be Npt = N1 * N2 * N3 * ... * ND number of points.
        # The file must have 1 column with Npt rows, as follows.
        # Let each q run from q_min to q_max, in steps of Delta q.
        # Then the CSV data has the form:
        #
        # V(q1_min,q2_min,...,q(D-1)_min,qD_min)
        # V(q1_min,q2_min,...,q(D-1)_min,qD_min+Delta qD)
        # V(q1_min,q2_min,...,q(D-1)_min,qD_min+2 Delta qD)
        # ...
        # V(q1_min,q2_min,...,q(D-1)_min,qD_max)
        # V(q1_min,q2_min,...,q(D-1)_min + Delta q(D-1),qD_min)
        # V(q1_min,q2_min,...,q(D-1)_min + Delta q(D-1),qD_min + Delta qD)
        # ...
        #
        # This function does not check to see if the values make sense, only that the correct number of values were input.
        
        self.Vtype = None
        self.Vmodel = None
        self.Vdata = None
        if (Vinput == 0):    # Potential energy comes from a model
            self.Vtype = scipy.zeros(D,int)
            self.Vmodel = []
            for i in range(0,D):
                self.Vtype[i] = inputValidInt("\nFor dimension " + str(i+1) + " enter (0) Harmonic Oscillator model or (1) Morse oscillator model:\n",0,1)
                if (self.Vtype[i] == 0):  # Model is harmonic oscillator
                    Vobj = HarmonicOscillatorModel()
                    self.Vmodel.append(Vobj)
                elif (self.Vtype[i] == 1): # Model is Morse oscillator
                    Vobj = MorseOscillatorModel()
                    self.Vmodel.append(Vobj)
        elif (Vinput == 1):  # Potential energy comes from a file
            validRead = False
            while (not validRead):
                fname = inputValidFilename("\nEnter filename for potential energy data:\n")
                Npt = 1
                for i in range(0,D):
                    Npt = Npt * self.N[i]
                self.Vdata = scipy.zeros(Npt,float)
                with open(fname,'r') as f:
                    idx = 0
                    csv_reader = csv.reader(f,delimiter=',')
                    for row in csv_reader:
                        self.Vdata[idx] = row[0]
                        idx = idx + 1
                if (Npt == idx):
                    print("Read " + str(idx) + " points from file " + fname + " (expecting " + str(Npt) + ").\n")
                    validRead = True
                else:
                    print("error: expecting " + str(Npt) + " points, but read " + str(idx) + " points\n")
                    
    def inputN(self,D):
        N = scipy.zeros(D,int)
        for i in range(0,D):
            validN = False
            while (not validN):
                N[i] = inputValidInt("\nEnter N for dimension " + str(i+1) + " (max 99):\n",1,99)
                if (N[i] % 2 == 1):
                    validN = True
                else:
                    print("error: N must be odd for the FGH method")
        return N
    
    def inputL(self,D):
        L = scipy.zeros(D,float)
        for i in range(0,D):
            validL = False
            while (not validL):
                Lmin = inputFloat("\nEnter minimum L for dimension " + str(i+1) + ":\n")
                Lmax = inputFloat("\nEnter maximum L for dimension " + str(i+1) + ":\n")
                if (Lmax > Lmin):
                    validL = True
                else:
                    print("error: max L must be greater than min L")
            L[i] = Lmax - Lmin
        return L

    def inputmu(self,D):
        mu = scipy.zeros(D,float)
        for i in range(0,D):
            mu[i] = inputNonNegativeFloat("Input mu for dimension " + str(i+1) + ":\n")
        return mu






    
