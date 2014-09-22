import numpy as np
from scipy.sparse import dia_matrix,lil_matrix
import time

stT = time.time()
Nx = 3; Ny = 5

# this seems to be fastest
"""diag_0 = np.zeros((Nx + 1)*(Ny + 1)) + 20
diag_1 = np.zeros((Nx + 1)*(Ny + 1))
for i in xrange(0,Nx + 1): diag_1[i*(Ny + 1):i*(Ny + 1) + Ny] = -8
diag_2 = np.zeros((Nx + 1)*(Ny + 1))
for i in xrange(0,Nx + 1): diag_2[i*(Ny + 1):i*(Ny + 1) + Ny - 1] = 1
diag_3 = np.zeros((Nx + 1)*(Ny + 1)) - 8
diag_4 = np.zeros((Nx + 1)*(Ny + 1))
for i in xrange(0,Nx + 1): diag_4[i*(Ny + 1):i*(Ny + 1) + Ny] = 2
diag_5 = np.ones((Nx + 1)*(Ny + 1))

mtr = dia_matrix(([diag_0,np.roll(diag_1,1),diag_1,np.roll(diag_2,2),diag_2,diag_3,diag_3,np.roll(diag_4,1),diag_4,\
                   diag_4,np.roll(diag_4,1),diag_5,diag_5],\
                  [0,1,-1,2,-2,Ny + 1,-Ny - 1,Ny + 2,-Ny - 2,Ny,-Ny,2*(Ny + 1),-2*(Ny + 1)]),\
    shape=((Nx + 1)*(Ny + 1),(Nx + 1)*(Ny + 1)))"""

"""mtr = lil_matrix(((Nx + 1)*(Ny + 1),(Nx + 1)*(Ny + 1)))
mtr.setdiag((Nx + 1)*(Ny + 1)*[20])
mtr.setdiag(((Nx + 1)*(Ny + 1) - 1)*[-8],1); mtr.setdiag(((Nx + 1)*(Ny + 1) - 1)*[-8],-1)
mtr.setdiag(((Nx + 1)*(Ny + 1) - 2)*[1],2); mtr.setdiag(((Nx + 1)*(Ny + 1) - 2)*[1],-2)
mtr.setdiag(((Nx + 1)*(Ny + 1) - Ny)*[2],Ny); mtr.setdiag(((Nx + 1)*(Ny + 1) - Ny)*[2],-Ny)
mtr.setdiag(((Nx + 1)*(Ny + 1) - Ny - 1)*[-8],Ny + 1); mtr.setdiag(((Nx + 1)*(Ny + 1) - Ny - 1)*[-8],-Ny - 1)
mtr.setdiag(((Nx + 1)*(Ny + 1) - Ny - 2)*[2],Ny + 2); mtr.setdiag(((Nx + 1)*(Ny + 1) - Ny - 2)*[2],-Ny - 2)
mtr.setdiag(((Nx + 1)*(Ny + 1) - 2*(Ny + 1))*[1],2*(Ny + 1)); mtr.setdiag(((Nx + 1)*(Ny + 1) - 2*(Ny + 1))*[1],-2*(Ny + 1))"""

"""mtr = lil_matrix(((Nx + 1)*(Ny + 1),(Nx + 1)*(Ny + 1)))
mtr.setdiag(np.zeros((Nx + 1)*(Ny + 1)) + 20)
mtr.setdiag(np.zeros((Nx + 1)*(Ny + 1) - 1) - 8,1); mtr.setdiag(np.zeros((Nx + 1)*(Ny + 1) - 1) -8,-1)
mtr.setdiag(np.ones((Nx + 1)*(Ny + 1) - 2),2); mtr.setdiag(np.ones((Nx + 1)*(Ny + 1) - 2),-2)
mtr.setdiag(np.zeros((Nx + 1)*(Ny + 1) - Ny) + 2,Ny); mtr.setdiag(np.zeros((Nx + 1)*(Ny + 1) - Ny) + 2,-Ny)
mtr.setdiag(np.zeros((Nx + 1)*(Ny + 1) - Ny - 1) - 8,Ny + 1); mtr.setdiag(np.zeros((Nx + 1)*(Ny + 1) - Ny - 1) - 8,-Ny - 1)
mtr.setdiag(np.zeros((Nx + 1)*(Ny + 1) - Ny - 2) + 2,Ny + 2); mtr.setdiag(np.zeros((Nx + 1)*(Ny + 1) - Ny - 2) + 2,-Ny - 2)
mtr.setdiag(np.ones((Nx + 1)*(Ny + 1) - 2*(Ny + 1)),2*(Ny + 1)); mtr.setdiag(np.ones((Nx + 1)*(Ny + 1) - 2*(Ny + 1)),-2*(Ny + 1))"""

diag_0 = np.zeros((Nx + 1)*(Ny + 1)) - 4
diag_1 = np.zeros((Nx + 1)*(Ny + 1))
for i in xrange(0,Nx + 1): diag_1[i*(Ny + 1):i*(Ny + 1) + Ny] = 1
diag_2 = np.ones((Nx + 1)*(Ny + 1))

mtr = dia_matrix(([diag_0,np.roll(diag_1,1),diag_1,diag_2,diag_2],[0,1,-1,Ny + 1,-Ny - 1]),shape=((Nx + 1)*(Ny + 1),(Nx + 1)*(Ny + 1)))

print mtr.todense()
print time.time() - stT
