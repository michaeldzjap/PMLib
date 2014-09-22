from FDObjectBase import FDObjectBase
from math import sqrt
from numpy import array
from scipy.sparse import lil_matrix
#from sparse_add import sptoeplitz

class FDString(FDObjectBase):
  validBoundaryConds = ('BothClamped','LeftClampedRightSimplySupported','LeftSimplySupportedRightClamped',\
  'BothSimplySupported','LeftClampedRightFree','LeftFreeRightClamped','LeftSimplySupportedRightFree',\
  'LeftFreeRightSimplySupported','BothFree')

  def __init__(self,gamma=200,kappa=1,b1=0,b2=0,boundaryCond='BothSimplySupported'):
    FDObjectBase.__init__(self,gamma,kappa,b1,b2,boundaryCond)

  # public methods
  def constrUpdateMatrices(self):
    self.__calcGridStep()       # calculate grid step
    k = self.__class__.k; _lambda2 = (self.gamma*k/self.h)**2; mu2 = (self.kappa*k/self.h**2)**2
    zeta = 2*self.b2*k/self.h**2; den = 1 + self.b1*k; N = self.N; Nm = self.Nm

    # create update matrices in sparse diagonal form
    self.B = lil_matrix((Nm,Nm))
    self.B.setdiag(Nm*[2 - 6*mu2 - 2*_lambda2 - 2*zeta])
    self.B.setdiag((Nm - 1)*[4*mu2 + _lambda2 + zeta],1); self.B.setdiag((Nm - 1)*[4*mu2 + _lambda2 + zeta],-1)
    self.B.setdiag((Nm - 2)*[-mu2],2); self.B.setdiag((Nm - 2)*[-mu2],-2)
    self.B /= den
    # self.B = sptoeplitz([2 - 6*mu**2 - 2*_lambda**2 - 2*zeta,4*mu**2 + _lambda**2 + zeta,-mu**2] + (N - 2)*[0])/den

    self.C = lil_matrix((Nm,Nm))
    self.C.setdiag(Nm*[1 - self.b1*k - 2*zeta])
    self.C.setdiag((Nm - 1)*[zeta],1); self.C.setdiag((Nm - 1)*[zeta],-1)
    self.C /= -den
    # self.C = -sptoeplitz([1 - self.b1*k - 2*zeta,zeta] + (self.N - 1)*[0])/den

    # adjust matrix entrees due to specified boundary conditions
    if self.boundaryCond == 'LeftClampedRightSimplySupported':
      self.B[-1,-1] += mu2/den
    elif self.boundaryCond == 'LeftSimplySupportedRightClamped':
      self.B[0,0] += mu2/den
    elif self.boundaryCond == 'BothSimplySupported':
      self.B[0,0] += mu2/den; self.B[-1,-1] += mu2/den
    elif self.boundaryCond == 'LeftClampedRightFree':
      a = (self.gamma*self.h/self.kappa)**2; b = 2*self.b2*self.h**2/(self.kappa**2*k)
      self.B[-1,-3:] = array([-mu2,mu2*(2 + a + b),2 - mu2*(1 + a + b)])/den
      self.B[-2,-2:] = map(sum,zip(self.B[-2,-2:].todense().tolist()[0],mu2*array([1,-2])/den))
      #self.B[-2,-2:] = [_a + _b for _a,_b in zip(self.B[-2,-2:].todense().tolist()[0],[mu**2,-2*mu**2]/den)]
      self.C[-1,-2:] = array([-mu2*b,-1 + self.b1*k + mu2*b])/den
    elif self.boundaryCond == 'LeftFreeRightClamped':
      a = (self.gamma*self.h/self.kappa)**2; b = 2*self.b2*self.h**2/(self.kappa**2*k)
      self.B[0,:3] = array([2 - mu2*(1 + a + b),mu2*(2 + a + b),-mu2])/den
      self.B[1,:2] = map(sum,zip(self.B[1,:2].todense().tolist()[0],mu2*array([-2,1])/den))
      self.C[0,:2] = array([-1 + self.b1*k + mu2*b,-mu2*b])/den
    elif self.boundaryCond == 'BothFree':
      a = (self.gamma*self.h/self.kappa)**2; b = 2*self.b2*self.h**2/(self.kappa**2*k)
      self.B[0,:3] = array([2 - mu2*(1 + a + b),mu2*(2 + a + b),-mu2])/den
      self.B[1,:2] = map(sum,zip(self.B[1,:2].todense().tolist()[0],mu2*array([-2,1])/den))
      self.C[0,:2] = array([-1 + self.b1*k + mu2*b,-mu2*b])/den
      self.B[-1,-3:] = array([-mu2,mu2*(2 + a + b),2 - mu2*(1 + a + b)])/den
      self.B[-2,-2:] = map(sum,zip(self.B[-2,-2:].todense().tolist()[0],mu2*array([1,-2])/den))
      self.C[-1,-2:] = array([-mu2*b,-1 + self.b1*k + mu2*b])/den
    elif self.boundaryCond == 'LeftFreeRightSimplySupported':
      self.B[-1,-1] += mu2/den
      a = (self.gamma*self.h/self.kappa)**2; b = 2*self.b2*self.h**2/(self.kappa**2*k)
      self.B[0,:3] = array([2 - mu2*(1 + a + b),mu2*(2 + a + b),-mu2])/den
      self.B[1,:2] = map(sum,zip(self.B[1,:2].todense().tolist()[0],mu2*array([-2,1])/den))
      self.C[0,:2] = array([-1 + self.b1*k + mu2*b,-mu2*b])/den
    elif self.boundaryCond == 'LeftSimplySupportedRightFree':
      self.B[0,0] += mu2/den
      a = (self.gamma*self.h/self.kappa)**2; b = 2*self.b2*self.h**2/(self.kappa**2*k)
      self.B[-1,-3:] = array([-mu2,mu2*(2 + a + b),2 - mu2*(1 + a + b)])/den
      self.B[-2,-2:] = map(sum,zip(self.B[-2,-2:].todense().tolist()[0],mu2*array([1,-2])/den))
      self.C[-1,-2:] = array([-mu2*b,-1 + self.b1*k + mu2*b])/den

    self.B = self.B.tocsc(); self.C = self.C.tocsc()

  def constrCouplingMatrices(self):
    k = self.__class__.k; den = 1 + self.b1*k

    # construnct first two coupling matrices in sparse diagonal form
    self.C1 = self.B.copy()*den; self.C2 = self.C.copy()*den
    self.C1.setdiag(-1*(self.C1.diagonal() - 2)); self.C2.setdiag(-1*(self.C2.diagonal() + (1 - self.b1*k)))

  # private methods
  def __calcGridStep(self):
    k = self.__class__.k; a = self.gamma**2*k**2 + 4*self.b2*k
    self.h = sqrt(0.5*(a + sqrt(a**2 + 16*self.kappa**2*k**2)))
    self.N = int(1/self.h)
    if self.boundaryCond == 'BothFree':
      self.Nm = self.N + 1
    elif self.boundaryCond in ('LeftClampedRightFree','LeftSimplySupportedRightFree','LeftFreeRightClamped','LeftFreeRightSimplySupported'):
      self.Nm = self.N
    else:
      self.Nm = self.N - 1
    self.h = 1./self.N
