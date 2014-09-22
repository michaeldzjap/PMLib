import numpy as np
from scipy.sparse import dia_matrix
from sparse_add import setdiag_range

Nx = 4; Ny = 4
diag = 6*[None]
diag[0] = 20 + np.zeros((Nx + 1)*(Ny + 1))
diag[1] = np.zeros((Nx + 1)*(Ny + 1))
for i in xrange(0,Nx + 1): diag[1][i*(Ny + 1):i*(Ny + 1) + Ny] = -8
diag[2] = np.zeros((Nx + 1)*(Ny + 1))
for i in xrange(0,Nx + 1): diag[2][i*(Ny + 1):i*(Ny + 1) + Ny - 1] = 1
diag[3] = -8 + np.zeros((Nx + 1)*(Ny + 1))
diag[4] = np.zeros((Nx + 1)*(Ny + 1))
for i in xrange(0,Nx + 1): diag[4][i*(Ny + 1):i*(Ny + 1) + Ny] = 2
diag[5] = 1 + np.zeros((Nx + 1)*(Ny + 1))
B = dia_matrix(([diag[0],np.roll(diag[1],1),diag[1],np.roll(diag[2],2),diag[2],diag[3],diag[3],\
    np.roll(diag[4],1),diag[4],diag[4],np.roll(diag[4],1),diag[5],diag[5]],\
    [0,1,-1,2,-2,Ny + 1,-Ny - 1,Ny + 2,-Ny - 2,Ny,-Ny,2*(Ny + 1),-2*(Ny + 1)]),\
    shape=((Nx + 1)*(Ny + 1),(Nx + 1)*(Ny + 1)))
B = B.tolil()
B.setdiag([18] + (Ny - 1)*[19] + [18])
setdiag_range(B,[18] + (Ny - 1)*[19] + [18],(Nx*(Ny + 1),(Nx + 1)*(Ny + 1 )))
for i in xrange(1,Nx): B[i*(Nx + 1),i*(Ny + 1)] = 19; B[(i + 1)*(Nx + 1) - 1,(i + 1)*(Ny + 1) - 1] = 19
print B.todense()
