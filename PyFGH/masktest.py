import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from numpy import ma
from PyFGH import GUI_Classes as guc
import matplotlib.pyplot as plt
import csv
from PyFGH.util import pyfghutil

D = 3
N = np.array([11, 11, 11])
L = np.array([1.1, 1.1, 1.65])
dx = L/N
Npts = np.prod(N)
wfn = np.zeros(Npts,dtype=float)

wfnfile = "C:/Users/jwoodford/PycharmProjects/PyFGH/PyFGH/outputfiles/Eigenvector-0.csv"
with open(wfnfile, newline='') as csvfile:
    wfndata = csv.reader(csvfile, delimiter=',')
    i = 0
    for row in wfndata:
        wfn[i] = row[3]
        i = i + 1

def IndexToQ(D, N, L, idx):
    q = np.zeros(D,dtype=float)
    for d in range(D):
        q[d] = (idx[d]-(N[d]-1)//2)*(L[d]/N[d])
    return q

for i in range(Npts):
    idx = pyfghutil.PointToIndex(N,i)
    q = IndexToQ(D, N, L, idx)
#    print(i, idx, q, wfn[i])

q_indx = 0
q_indy = 1
q_mask = np.zeros(D, dtype=int)
q_mask[q_indx] = 1
q_mask[q_indy] = 1

nx = (N[q_indx] - 1) // 2
dx = L[q_indx] / N[q_indx]
x = np.array([(j - nx) * dx for j in range(N[q_indx])], dtype=float)

ny = (N[q_indy] - 1) // 2
dy = L[q_indy] / N[q_indy]
y = np.array([(j - ny) * dy for j in range(N[q_indy])], dtype=float)

q_idx = np.zeros(D, dtype=int)
i = 0
for d in range(D):
    if ((d != q_indx) and (d != q_indy)):
        q_idx[d] = 5
        i = i + 1
print(q_idx)

q_idx_mask = ma.array(q_idx, mask=q_mask)
print(q_idx_mask)
z = np.zeros((N[q_indx],N[q_indy]), dtype=float)

Npts = np.prod(N)
for pt in range(Npts):
    idx = np.array(pyfghutil.PointToIndex(N, pt), dtype=int)
    idx_mask = ma.array(idx, mask=q_mask)
    if (np.equal(q_idx_mask, idx_mask).all()):
        z[idx[q_indx],idx[q_indy]] = wfn[pt]
        print(pt, idx, wfn[pt])



