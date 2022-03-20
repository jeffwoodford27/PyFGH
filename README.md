# PyFGH
A Python implementation of the Fourier Grid Hamiltonian (FGH) method, applied to molecular vibrations.

This program solves the vibrational Schrodinger Equation for a nonlinear triatomic molecule.
To describe the vibrations of a nonlinear triatomic moleucle, three vibrational coordinates are required: q1, q2, q3.
In this program, q1 and q2 represent stretching modes, while q3 represents the bending mode.

In the FGH method, each vibrational coordinate is discretized on N points of length L.  The grid spacing is dq = L/N.  In the FGH method, N must be odd.
The grid is symmetric about the equilibrium geometry, and each grid point qi is given by qi = (i-N//2)×dq.  (N//2 means divide N by two and truncate to the nearest integer.)

Instructions:
1. Run main.py.  A GUI window will pop up.
2. Enter the parameters for the grid length for each of the three vibrational coordinates.   N must be odd.  For L1 and L2 (stretching coordinates), the units are in bohr.  For L3 (bending coordinate), the units are in radians.
3. Select the number of cores desired for the calculation.  The computation of both the T matrix and the V matrix is able to be run in parallel.  The default is 1 (no parallelism).
4. Select whether the computation will be run remotely via SSH.  The default is "No".
5. Click "Read Structures and Energies from File".  Two dialog boxes will pop up.
6. In the FIRST dialog box, upload a CSV with the equilibrium geometry of the molecule.  The molecule is assumed to be in the x-y plane.  The CSV must be encoded "UTF-8".  It should have three lines, one per atom, and each line must be in the following format:

Symbol,A,x,y

where:
Symbol is the one- or two-letter atomic symbol for the atom.
A is the mass number (an integer!) for the atom.
x is the x-coordinate of the atom (in bohr)
y is the y-coordinate of the atom (in bohr)

7. In the SECOND dialog box, upload a CSV with the potential energy file.  This CSV must also be encoded "UTF-8" and must have the following format:

q1,q2,q3,x1,y1,x2,y2,x3,y3,energy

q1,q2,q3 = the values of the vibrational coordinates.  q1,q2 are stretching coordinates and should be in bohr.  q3 is the bending coordinate and should be in radians.

x1,y1,x2,y2,x3,y3 = the x,y coordinates of the three atoms.  Must be in bohr.

energy = the energy of the structure relative to the equilibrium geometry.  Must be in hartrees.

There must be N1×N2×N3 points total, and they must be arranged in order of increasing q3, THEN increasing q2, THEN increasing q1.  For example, if N1 = N2 = N3 = 7  and L1 = L2 = L3 = 0.7, then the lines in the potential energy file must be in this order:

-0.3, -0.3, -0.3, ...

-0.3, -0.3, -0.2, ...

...

-0.3, -0.3, +0.3, ...

-0.3, -0.2, -0.3, ...

-0.3, -0.2, -0.2, ...

...

-0.3, -0.2, +0.3, ...

...

-0.3, +0.3, +0.3, ...

-0.2, -0.3, -0.3, ...

-0.2, -0.3, -0.2, ...

Examples of these two files are provided in the "testing files" folder.

8. Click the "Calculate" button.

The program will then compute the kinetic energy (T) matrix, the potential energy (V) matrix, find the eigenvalues and eigenfunctions, and print the first 10 eigenvalues (in cm-1) to the screen.  The program will also save the eigenvalues and first 20 eigenvectors as CSV files in the "output files" folder. The eigenvector CSVs are arranged in the order: q1, q2, q3, value.

Validation

There are two example files in the "testing files" folder.
The first is "water-equil.csv", which represents the equilibrium coordinates (in bohr) for water computed at the RHF/6-31G(d) level.
The second is "water-potential.csv", which represents a potential energy file for water also computed at RHF/6-31G(d) level.  The parameters for this file are:

N1 = N2 = N3 = 11

L1 = L2 = 1.10 (bohr)

L3 = 1.65 (rad)

Using these files, the first six eigenvalues (relative to the lowest energy eigenvalue) should be:

1763.5 -- fundamental vibrational frequency for q3, bending  mode

3484.0 -- first overtone for q3

3912.3 -- fundamental vibrational frequency for q2, symmetric stretch

3998.2 -- fundamental vibrational frequency for q1, antisymmetric stretch

5168.9 -- second overtone for q3

5663.2 -- combination of q3 + q2

System Requirements:
* Python interpreter (we used v3.8)
* Numpy (we used v1.21.1)
* Scipy (we used v1.7.0)
* Tkinter (we used v???)
* Paramiko (we used v2.10.3) - for SSH

We recommend using the PyCharm Development Environment (https://www.jetbrains.com/pycharm/) for running this code.