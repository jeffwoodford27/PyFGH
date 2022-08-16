# Testing file for matplotlib plotting capabilities for the eigenvectors.

from matplotlib import pyplot as plt
import matplotlib.tri as mtri
import numpy as np
import csv
from scipy.spatial import Delaunay
from scipy.interpolate import griddata

def PointToIndex(N,pt):
    return list(np.unravel_index(pt,tuple(N)))

evfile = "output files/Eigenvector-6.csv"
D = 3
N = np.zeros(D,dtype=int)
N[0] = N[1] = N[2] = 11
Npts = np.prod(N)
L = np.zeros(D,dtype=float)
L[0] = L[1] = 1.1
L[2] = 1.65

x = np.zeros(Npts,dtype=float)
y = np.zeros(Npts,dtype=float)
z = np.zeros(Npts,dtype=float)

c = np.zeros(Npts,dtype=float)
with open(evfile, newline='') as csvfile:
    ev = csv.reader(csvfile)
    pt = 0
    for row in ev:
        x[pt] = float(row[0])
        y[pt] = float(row[1])
        z[pt] = float(row[2])
        c[pt] = float(row[3])
        pt = pt + 1

sum = 0
for i in range(Npts):
    sum += c[i]*c[i]
#print(sum)

for i in range(Npts):
    val = (c[i]*c[i])/sum
#    c[i] = val
    c[i] = c[i]*c[i]


points = np.zeros([Npts,D],dtype=float)
for pt in range(Npts):
    idx = PointToIndex(N,pt)
    points[pt,0] = idx[0]
    points[pt,1] = idx[1]
    points[pt,2] = idx[2]

grid_x,grid_y,grid_z = np.mgrid[0:11:33j,0:11:33j,0:11:33j]
griddata = griddata(points, c, (grid_x, grid_y, grid_z), method='linear')
#print(griddata.shape)

#print(grid_x[0])
#print(grid_y[0])
#print(grid_z[0])

def plot4d(x,y,z,c,N,L):
    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(projection="3d")
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    mask = c > 0.001
#    idx = np.arange(int(np.prod(data.shape)))
#    x, y, z = np.unravel_index(idx, data.shape)
#    print(x[5],y[5],z[5])
#    print(data.flatten().shape)
#    print(x.shape,y.shape,z.shape)
#    pt = PointToIndex(N,[5,5,5])
#    print(x[pt],y[pt],z[pt],data.flatten()[pt])
    x = (x+1/2)*L[2]/N[2] - L[2]/2
    y = (y+1/2)*L[1]/N[1] - L[1]/2
    z = (z+1/2)*L[0]/N[0] - L[0]/2
    ax.set_xlabel("q1")
    ax.set_ylabel("q2")
    ax.set_zlabel("q3")
    ax.scatter(z, y, x, c=c, s=10.0 * mask, edgecolor="face", alpha=None, marker="o", linewidth=0)
#    ax.scatter(x, y, z, c=data.flatten(), edgecolor="face", alpha=None, marker="o", cmap="magma", linewidth=0)
    plt.tight_layout()
    plt.show()
    return

plot4d(grid_x,grid_y,grid_z,griddata,N,L)

def plot4dorig(data):
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(projection="3d")
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    mask = data > 0.01
    idx = np.arange(int(np.prod(data.shape)))
    x, y, z = np.unravel_index(idx, data.shape)
    ax.scatter(x, y, z, c=data.flatten(), s=10.0 * mask, edgecolor="face", alpha=0.2, marker="o", cmap="magma", linewidth=0)
    plt.tight_layout()
    plt.show()
    plt.close(fig)

'''
if __name__ == "__main__":
    X = np.arange(-10, 10, 0.5)
    Y = np.arange(-10, 10, 0.5)
    Z = np.arange(-10, 10, 0.5)
    X, Y, Z = np.meshgrid(X, Y, Z, indexing="ij")
    density_matrix = np.sin(np.sqrt(X**2 + Y**2 + Z**2))
    print(density_matrix.shape)
    plot4d(density_matrix)



point_coords= np.array([[ 0.05497894, -0.11160859,  0.37084371],
                        [-0.00817349, -0.14016391,  0.39896593],
                        [-0.04405962, -0.13445015,  0.41198156],
                        [-0.02392213, -0.1297217,   0.39447151],
                        [-0.00622379, -0.12973436,  0.39639086],
                        [ 0.01604251, -0.12920773,  0.40366026],
                        [ 0.06505235, -0.13291964,  0.40368367],
                        [ 0.07263324, -0.13199505,  0.40244909],
                        [ 0.03655646, -0.13674183,  0.40442567],
                        [ 0.00245951, -0.13406454,  0.40627548]])

snowh=[992634.25,
       22319520.0,
       23621576.0,
       22518240.0,
       19963640.0,
       20256056.0,
       33873776.0,
       19216264.0,
       17755528.0,
       4434950.0]

x = point_coords[:, 0]
y = point_coords[:, 1]
z = point_coords[:, 2]
points2D = np.vstack([x,y]).T
tri = Delaunay(points2D) #triangulate the 2d points
I, J, K = (tri.simplices).T
print("simplices:", "\n", tri.simplices)
fig=go.Figure(go.Mesh3d(x=x, y=y, z=z,
                        i=I, j=J, k=K,
                       intensity=snowh, colorscale="ice" )) #these two last attributes, intensity and colorscale, assign a color according to snow height
fig.show()


index_x = 0; index_y = 1; index_z = 2; index_c = 3
list_name_variables = ['x', 'y', 'z', 'c']
name_color_map = 'seismic'
triangles = mtri.Triangulation(x, y).triangles
choice_calcuation_colors = 1
if choice_calcuation_colors == 1: # Mean of the "c" values of the 3 pt of the triangle
    colors = np.mean( [c[triangles[:,0]], c[triangles[:,1]], c[triangles[:,2]]], axis = 0);
elif choice_calcuation_colors == 2: # Mediane of the "c" values of the 3 pt of the triangle
    colors = np.median( [c[triangles[:,0]], c[triangles[:,1]], c[triangles[:,2]]], axis = 0);
elif choice_calcuation_colors == 3: # Max of the "c" values of the 3 pt of the triangle
    colors = np.max( [c[triangles[:,0]], c[triangles[:,1]], c[triangles[:,2]]], axis = 0);
#end
#----------
# Displays the 4D graphic.
fig = plt.figure()
ax = fig.gca(projection='3d')
triang = mtri.Triangulation(x, y, triangles)
surf = ax.plot_trisurf(triang, z, cmap = name_color_map, shade=False, linewidth=0.2)
surf.set_array(colors); surf.autoscale()

#Add a color bar with a title to explain which variable is represented by the color.
cbar = fig.colorbar(surf, shrink=0.5, aspect=5)
cbar.ax.get_yaxis().labelpad = 15; cbar.ax.set_ylabel(list_name_variables[index_c], rotation = 270)

# Add titles to the axes and a title in the figure.
ax.set_xlabel(list_name_variables[index_x]); ax.set_ylabel(list_name_variables[index_y])
ax.set_zlabel(list_name_variables[index_z])
plt.title('%s in function of %s, %s and %s' % (list_name_variables[index_c], list_name_variables[index_x], list_name_variables[index_y], list_name_variables[index_z]) )

plt.show()
'''