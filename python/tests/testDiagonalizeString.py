from math import sqrt,pi,floor
import numpy as np
from scipy.sparse import lil_matrix,hstack,vstack,identity
from scipy.linalg import eig
from scipy.sparse.linalg import eigs,eigsh

# global parameters
f0 = 101
b1=.858236
b2=.000530
inharmCoef=0.00001
SR = 44100;

# derived parameters
k = 1./SR
gamma = 2.*f0; kappa = gamma*sqrt(inharmCoef)/pi

# stability condition
h = sqrt(0.5*(gamma**2*k**2+4*b2*k+sqrt((gamma*k**2+4*b2*k)**2+16*kappa**2*k**2)))
N = int(floor(1/h)); h = 1./N
mu = kappa*k/h**2; _lambda = gamma*k/h; zeta = 2*b2*k/h**2; den = 1 + b1*k

# construct update matrix
B = lil_matrix((N+1,N+1))
B.setdiag((N + 1)*[2 - 6*mu**2 - 2*_lambda**2 - 2*zeta])
B.setdiag(N*[4*mu**2 + _lambda**2 + zeta],1); B.setdiag(N*[4*mu**2 + _lambda**2 + zeta],-1)
B.setdiag((N - 1)*[-mu**2],2); B.setdiag((N - 1)*[-mu**2],-2)
B /= den

C = lil_matrix((N+1,N+1))
C.setdiag((N + 1)*[1 - b1*k - 2*zeta])
C.setdiag(N*[zeta],1); C.setdiag(N*[zeta],-1)
C /= -den

# construct final block matrix
P = hstack((B,C)); Q = hstack((identity(N+1),lil_matrix((N+1,N+1))))
P = vstack((P,Q))

w,v = eigs(P,k=N)
#w,v = eig(M.todense())

print SR*np.angle(w)/(2*pi)
