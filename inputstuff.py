import numpy as np
import scipy as scipy
import scipy.linalg
import math
import sys
import pandas as pd


def inputValidInt (prompt, intmin, intmax):
    validinput = 0
    while (not validinput):
        inputint = input(prompt)
        if (type(inputint) is int):
            for i in range(intmin,intmax+1):
                if (inputint == i):
                    validinput = 1
                    break
    return (inputint)

def inputPositiveFloat (prompt):
    validinput = 0
    while (not validinput):
        inputfloat = input(prompt)
        if (type(inputfloat) is int):
            inputfloat = float(inputfloat)
        if ((type(inputfloat) is float) and (inputfloat > 0)):
            validinput = 1
    return (inputfloat)

def calcHarmonic (D, N, L, mu, k):
    Npt = N[0]
    Vpot = scipy.zeros(Npt,float)
    for i 


D = inputValidInt("\nEnter the number of dimensions (only 1 is currently supported):\n",1,1)

N = scipy.zeros(D,int)
L = scipy.zeros(D,float)
mu = scipy.zeros(D,float)
k = scipy.zeros(D,float)
De = scipy.zeros(D,float)
a = scipy.zeros(D,float)

Vflag = inputValidInt("\nIs potential energy: (0) computed from a model, or (1) input from file?\n",0,1)

if (Vflag == 0):
    Vmodel = inputValidInt("\nDo you want to use: (0) harmonic oscillator model, or (1) Morse oscillator model?\n",0,1)
    for i in range(0,D):
        mu[i] = inputPositiveFloat("\nEnter mu for dimension " + str(i+1) + " :\n")
        validL = 0
        while (not validL):
            Lmin = inputPositiveFloat("\nEnter minimum L for dimension " + str(i+1) + ":\n")
            Lmax = inputPositiveFloat("\nEnter maximum L for dimension " + str(i+1) + ":\n")
            if (Lmax > Lmin):
                validL = 1
            else:
                print("error: max L must be greater than min L\n")
        L[i] = Lmax - Lmin
        validN = 0
        while (not validN):
            N[i] = inputValidInt("\nEnter N for dimension " + str(i+1) + ":\n")
            if (N[i] % 2 == 1):
                validN = 1
            else:
                print("error: N must be odd for the FGH method\n")
        if (Vmodel == 0):
            k[i] = inputPositiveFloat("\nEnter k for dimension " + str(i+1) + "(in units of hartree/bohr^2) :\n")
        elif (Vmodel == 1):
            De[i] = inputPositiveFloat("\nEnter De for dimension " + str(i+1) + "(in units of hartree):\n")
            a[i] = inputPositiveFloat("\nEnter a for dimension " + str(i+1) + "(in units of bohr^-1):\n")

    if (Vmodel == 0):
        Vpot = calcHarmonic(D,N,L,mu,k)
    elif (Vmodel == 1):
        Vpot = calcMorse(D,N,L,mu,De,a)

elif (Vflag == 1):
    pass



