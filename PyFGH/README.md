# PyFGH
A Python implementation of the Fourier Grid Hamiltonian (FGH) method, applied to molecular vibrations.

By: Nelson Maxey, Weston Henning, Tyler Law, Josiah Randleman, and Prof. Jeff Woodford
(jwoodford@missouriwestern.edu)

This program solves the vibrational Schrodinger Equation in internal coordinates.  In principle it may be used for molecules of any size, but it has only been most thoroughly tested for diatomic and triatomic molecules.  Currently this program is only tested for nonlinear molecules beyond diatomics.


To describe the vibrations of a molecule, a set of vibrational coordinates are required.  If the molecule has Nat number of atoms, then for a nonlinear molecule, there are 3Nat-6 vibrations, and hence 3Nat-6 vibrational coordinates needed to describe that vibration.  For a symmetric (C2v) nonlinear triatomic molecule, the most convenient choices are the symmetric stretch, asymmetric stretch, and symmetric bend.  These vibrational coordinates are collectively represented as {q}.

In the FGH method, each vibrational coordinate is discretized on N points of length L.  The grid spacing is dq = L/N.  In the FGH method, N must be odd.
The grid is symmetric about the equilibrium geometry, and each grid point qi is given by qi = (i-N//2)×dq.  (N//2 means divide N by two and truncate to the nearest integer.)

Instructions:
1. Run main.py.  A GUI window will pop up.
2. Enter the number of dimensions (D), corresponding to the number of vibrations to be considered in the problem.
3. Click on "Get N,L Values".  In the input box, enter the N and L values for each dimension.  These must be given in the same order as specified in the potential energy file (see below).  For coordinates describing stretches, the unit of L is bohr.  For coordinates describing angles, the unit of L is radians.
4. Select the number of cores desired for the calculation.  If a value greater than 1 is selected, construction of the kinetic and potential energy matrices is performed in parallel using process-based multiprocessing.
5. Click "Get Equilibrium Coordinates".  Select the filename of the equilibrium coordinate file (described below).
6. Select the number of desired eigenvalues to be returned.  The eigenvalue corresponds to the energy of a vibrational state.  Selecting the minimum allowable value (2) means to only select the ground and first excited state.
7. Select the eigenvalue calculation method, either "Sparse Matrix" or "Full Matrix".  If "Full Matrix" is selected, then the complete Hamiltonian matrix is diagonalized.  If "Sparse Matrix" is selected, then sparse matrix techniques are used to find only the number of eigenvalues requested above.  If the size of your problem is very large, Sparse Matrix should be selected.
8. Click "Choose Potential Energy Method", and then choose either "Read From File" or "Calculate With Psi4".
    8a. If you choose "Read From File", select the potential energy file (described below).
    8b. If you choose "Calculate With Psi4", select the model chemistry you wish for Psi4 to use.
9. Click "CALCULATE!" to kick off the calculation.

The Equilibrium Structure File

The first line should contain:
Charge,Multiplicity

where the charge is the molecular charge and the multiplicity is the electronic multiplicity (2S+1) for the electronic state in question.

For every line thereafter, it should contain:
Symbol,A,x,y,z

where:
* Symbol is the one- or two-letter atomic symbol for the atom.
* A is the mass number (an integer!) for the atom.
* x is the x-coordinate of the atom (in bohr).
* y is the y-coordinate of the atom (in bohr).
* z is the z-coordinate of the atom (in bohr).

The Potential Energy File

The structure of the potential energy file is as follows:
Each line should have the following format:

q1,q2,...,qD,x1,y1,z1,x2,y2,z2,...,x(Nat),y(Nat),z(Nat),energy

q1,q2, ..., qD = the values of the M vibrational coordinates.  Units must be in bohr.
x1,y1,z1,...,x(Nat),y(Nat),z(Nat) = the x,y,z coordinates of each of the Nat atoms at that particular grid point.  Must be in bohr.
energy = the energy of the structure relative to the equilibrium geometry.  Must be in hartrees.

There must be N1×N2×...*ND points total, and they must be arranged in order of increasing q1, THEN increasing q2, THEN increasing q3.  For example, if D = 3 and N1 = N2 = N3 = 7  and L1 = L2 = L3 = 0.7, then the lines in the potential energy file must be in this order:

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

Sample Input Data

There are two example files in the "testing files" folder.
The first is "water-equil.csv", which represents the equilibrium coordinates (in bohr) for water computed at the RHF/6-31G(d) level.
The second is "water-potential.csv", which represents a potential energy file for water also computed at RHF/6-31G(d) level.  The parameters for this file are:

N1 = N2 = N3 = 11
L1 = L2 = 1.10
L3 = 1.65

Using these files, the first six eigenvalues (relative to the lowest energy eigenvalue) should be:

1758.1 -- fundamental vibrational frequency for q3, bending mode

3472.3 -- first overtone for q3

3912.5 -- fundamental vibrational frequency for q2, symmetric stretch

4000.1 -- fundamental vibrational frequency for q1, antisymmetric stretch

5150.6 -- second overtone for q3

5658.9 -- combination of q3 + q2

System Requirements:
* Python interpreter (we used v3.8)
* Numpy (we used v1.21.1)
* Scipy (we used v1.7.0)
* Tkinter (as a part of the standard library)
* If the Psi4 option is selected, then Psi4 must be correctly installed on your system and the relevant Python libraries must be discoverable by PyFGH.

We recommend using the PyCharm Development Environment (https://www.jetbrains.com/pycharm/) for running this code.

Acknowledgements

The theoretical method behind this work is based on the following paper:
Stare, J., and Balint-Kurti, G. G., "Fourier Grid Hamiltonian Method for Solving the Vibrational Schrodinger Equation in Internal Coordinates: Theory and Test Applications", J. Phys. Chem. A 2003, 107, 7204-7214

This software is licensed under LGPL-3.0.

