
from itertools import product

from scipy.sparse import dia_matrix
import numpy as np


# String vector: 'LRTB'
# so 'C' -> Clamped, 'S' -> Simply supported, 'F' -> Free
# then 'CCCS' -> L-Clamped, R-Clamped, T-Clamped, B-Simply.
BOUNDARY_CONDITIONS_2D = tuple("".join(x) for x in product(*(['CSF'] * 4)))


def checkInputArgs(Nx, Ny, bc):
    if not isinstance(Nx,int):
        raise TypeError('argument Nx must be of type int')
    elif Nx < 0:
        raise ValueError('argument Nx cannot be negative')
    if not isinstance(Ny,int):
        raise TypeError('argument Ny must be of type int')
    elif Ny < 0:
        raise ValueError('argument Ny cannot be negative')
    if not bc in BOUNDARY_CONDITIONS_2D:
        raise ValueError('argument bc does not represent a valid boundary condition')


def laplacian_matrix_2d(Nx=3, Ny=3, bc='CCCC'):
    """
    generates the discrete laplacian operator in matrix form operating over a 2D grid of size (Nx - 1)*(Ny - 1)
    """
    checkInputArgs(Nx,Ny,bc)

    #np.set_printoptions(threshold=np.nan,linewidth=230,precision=2,suppress=True)

    if not 'F' in bc:
        diag = 3*[None]
        diag[0] = -4 + np.zeros((Nx - 1)*(Ny - 1))
        diag[1] = np.ones((Nx - 1)*(Ny - 1))
        for i in range(1,Nx): diag[1][i*(Ny - 1) - 1] = 0
        diag[2] = np.ones((Nx - 1)*(Ny - 1))

        mat = dia_matrix(([diag[0],np.roll(diag[1],1),diag[1],diag[2],diag[2]],\
        [0,1,-1,Ny - 1,-Ny + 1]),shape=((Nx - 1)*(Ny - 1),(Nx - 1)*(Ny - 1)))
    else:
        raise NotImplementedError('free boundary conditions are not implemented yet')

    return mat


def biharmonic_matrix_2d(Nx=3, Ny=3, bc='CCCC'):
    """
    generates the discrete biharmonic operator in matrix form
    """
    checkInputArgs(Nx,Ny,bc)

    #np.set_printoptions(threshold=np.nan,linewidth=230,precision=2,suppress=True)

    diag = 6*[None]

    if bc == 'CCCC':
        diag[0] = 20 + np.zeros((Nx - 1)*(Ny - 1))
    elif bc == 'SSSS':
        diag[0] = np.array([18] + (Ny - 3)*[19] + [18] + sum([[19] + (Ny - 3)*[20] + [19]]*(Nx - 3),[]) + [18] + (Ny - 3)*[19] + [18])
    elif bc == 'CCCS':
        diag[0] = np.array(sum([[19] + [20]*(Ny - 2)]*(Nx - 1),[]))
    elif bc == 'CCSC':
        diag[0] = np.array(sum([[20]*(Ny - 2) + [19]]*(Nx - 1),[]))
    elif bc == 'CCSS':
        diag[0] = np.array(sum([[19] + [20]*(Ny - 3) + [19]]*(Nx - 1),[]))
    elif bc == 'CSCC':
        diag[0] = [20]*(Ny - 1)*Nx + [19]*(Ny - 1)
    elif bc == 'CSCS':
        diag[0] = sum([[19] + [20]*(Ny - 2)]*(Nx - 2),[]) + [18] + [19]*(Ny - 2)
    elif bc == 'CSSC':
        diag[0] = sum([[20]*(Ny - 2) + [19]]*(Nx - 2),[]) + [19]*(Ny - 2) + [18]
    elif bc == 'CSSS':
        diag[0] = sum([[19] + [20]*(Ny - 3) + [19]]*(Nx - 2),[]) + [18] + [19]*(Ny - 3) + [18]
    elif bc == 'SCCC':
        diag[0] = [19]*(Ny - 1) + [20]*(Ny - 1)*(Nx - 2)
    elif bc == 'SCCS':
        diag[0] = [18] + [19]*(Ny - 2) + sum([[19] + [20]*(Ny - 2)]*(Nx - 2),[])
    elif bc == 'SCSC':
        diag[0] = [19]*(Ny - 2) + [18] + sum([[20]*(Ny - 2) + [19]]*(Nx - 2),[])
    elif bc == 'SCSS':
        diag[0] = [18] + [19]*(Ny - 3) + [18] + sum([[19] + [20]*(Ny - 3) + [19]]*(Nx - 2),[])
    elif bc == 'SSCC':
        diag[0] = [19]*(Ny - 1) + [20]*(Ny - 1)*(Nx - 3) + [19]*(Ny - 1)
    elif bc == 'SSCS':
        diag[0] = [18] + [19]*(Ny - 2) + sum([[19] + [20]*(Ny - 2)]*(Nx - 3),[]) + [18] + [19]*(Ny - 2)
    elif bc == 'SSSC':
        diag[0] = [19]*(Ny - 2) + [18] + sum([[20]*(Ny - 2) + [19]]*(Nx - 3),[]) + [19]*(Ny - 2) + [18]
    else:
        raise NotImplementedError('free boundary conditions are not implemented yet')

    diag[1] = -8 + np.zeros((Nx - 1)*(Ny - 1))
    for i in range(1,Nx): diag[1][i*(Ny - 1) - 1] = 0
    diag[2] = np.ones((Nx - 1)*(Ny - 1))
    for i in range(1,Nx): diag[2][i*(Ny - 1) - 1] = 0; diag[2][i*(Ny - 1) - 2] = 0
    diag[3] = -8 + np.zeros((Nx - 1)*(Ny - 1))
    diag[4] = 2 + np.zeros((Nx - 1)*(Ny - 1))
    for i in range(1,Nx): diag[4][i*(Ny - 1) - 1] = 0
    diag[5] = np.ones((Nx - 1)*(Ny - 1))

    mat = dia_matrix(([diag[0],np.roll(diag[1],1),diag[1],np.roll(diag[2],2),diag[2],diag[3],diag[3],\
    np.roll(diag[4],1),np.roll(diag[4],Ny - 1),np.roll(diag[4],-Ny + 2),diag[4],diag[5],diag[5]],\
    [0,1,-1,2,-2,Ny - 1,-Ny + 1,Ny,Ny - 2,-Ny + 2,-Ny,2*(Ny - 1),2*(-Ny + 1)]),\
    shape=((Nx - 1)*(Ny - 1),(Nx - 1)*(Ny - 1)))

    return mat
