from PyFGH.util import pyfghutil
from PyFGH import molecule_gui
import multiprocessing as mp
import numpy as np
import time
try:
    import psi4
except:
    pass

#def calcPsi4Energy(psi4method, psimol):
#    return psi4.energy(psi4method, molecule=psimol)

def calcPsi4Energy(psi4method, psimol):
    psimol = psimol.splitlines()
    return float(psimol[2].split()[1])

def calcPESfromPsi4(D, N, equil, pes, cores, psi4method):
    try:
        pass
    except:
        raise ("Psi4 could not be found")

    S = equil.getSymbolList()
    x = equil.getXList()
    y = equil.getYList()
    z = equil.getZList()
    Q = equil.getCharge()
    Mult = equil.getMultiplicity()

    Npts = np.prod(N)

    paramz = []

    if (D == 1):
        mol_geom = """
        {q} {mult}
        {s1} {x1} {y1} {z1}
        {s2} {x2} {y2} {z2}
        """

        psimol = psi4.geometry(mol_geom.format(q=Q, mult=Mult,
                                               s1=S[0], x1=0, y1=0, z1=z[0],
                                               s2=S[1], x2=0, y2=0, z2=z[1]))
        try:
            emin = calcPsi4Energy(psi4method, psimol)
        except:
            raise Exception("Unknown/unsupported method " + psi4method + " or other Psi4 error.")

        for pt in range(Npts):
            mol = pes.getPointByPt(pt).getMolecule()
            z = mol.getZList()
            psimol = psi4.geometry(mol_geom.format(q=Q, mult=Mult,
                                                   s1=S[0], x1=0, y1=0, z1=z[0],
                                                   s2=S[1], x2=0, y2=0, z2=z[1]))

            paramz.append((psi4method,psimol))

    elif (D == 3):
        mol_geom = """
        {q} {mult}
        {s1} {x1} {y1} {z1}
        {s2} {x2} {y2} {z2}
        {s3} {x3} {y3} {z3}
        """

#        psimol = psi4.geometry(mol_geom.format(q=Q, mult=Mult,
#                                               s1=S[0], x1=x[0], y1=y[0], z1=0,
#                                               s2=S[1], x2=x[1], y2=y[1], z2=0,
#                                               s3=S[2], x3=x[2], y3=y[2], z3=0))

        psimol = mol_geom.format(q=Q, mult=Mult,
                                                       s1=S[0], x1=x[0], y1=y[0], z1=0,
                                                       s2=S[1], x2=x[1], y2=y[1], z2=0,
                                                       s3=S[2], x3=x[2], y3=y[2], z3=0)

        try:
            emin = calcPsi4Energy(psi4method, psimol)
        except:
            raise Exception("Unknown/unsupported method " + psi4method + " or other Psi4 error.")

        for pt in range(Npts):
            mol = pes.getPointByPt(pt).getMolecule()
            x = mol.getXList()
            y = mol.getYList()
#            psimol = psi4.geometry(mol_geom.format(q=Q, mult=Mult,
#                                                   s1=S[0], x1=x[0], y1=y[0], z1=0,
#                                                   s2=S[1], x2=x[1], y2=y[1], z2=0,
#                                                   s3=S[2], x3=x[2], y3=y[2], z3=0))
            psimol = mol_geom.format(q=Q, mult=Mult,
                                     s1=S[0], x1=x[0], y1=y[0], z1=0,
                                     s2=S[1], x2=x[1], y2=y[1], z2=0,
                                     s3=S[2], x3=x[2], y3=y[2], z3=0)

            paramz.append((psi4method,psimol))

    else:
        raise ("Invalid call to Psi4 driver")

    p = mp.Pool(cores)
    en = p.starmap(calcPsi4Energy,paramz)
    p.close()
    for pt in range(Npts):
        pes.getPointByPt(pt).setEnergy(en[pt] - emin)

    for pt in range(10):
        print(pes.getPointByPt(pt).getEnergy())
    return


if __name__ == '__main__':

    eqfilename = "./testingfiles/water-equil.csv"
    pesfilename = "./testingfiles/water-potential.csv"

    D = 3
    N = np.array([11,11,11],dtype=int)
    L = [1.1,1.1,1.65]
    cores = 2

    equil = molecule_gui.readEqfile(eqfilename)
    Nat = equil.getNatom()
    pes = molecule_gui.generatePESCoordinates_Psi4(D, N, L, equil)

    mol_geom = """
    {q} {mult}
    {s1} {x1} {y1} {z1}
    {s2} {x2} {y2} {z2}
    """

    Q = equil.getCharge()
    Mult = equil.getMultiplicity()
    S = equil.getSymbolList()
    x = equil.getXList()
    y = equil.getYList()
    z = equil.getZList()

    psimol = mol_geom.format(q=Q, mult=Mult, s1=S[0], x1=x[0], y1=y[0], z1=0, s2=S[1], x2=x[1], y2=y[1], z2=0)

    psi4method = None

    calcPESfromPsi4(D, N, equil, pes, 4, psi4method)


