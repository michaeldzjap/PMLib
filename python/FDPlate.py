from FDObjectBase import FDObjectBase
from sparse_diff_matr_2d import laplacian_matrix_2d,biharm_matrix_2d
from math import sqrt
import numpy as np
from scipy.sparse import dia_matrix,identity

class FDPlate(FDObjectBase):
  validBoundaryConds = ('AllSidesClamped','LeftClampedRightClampedTopClampedBottomSimplySupported','LeftClampedRightClampedTopClampedBottomFree','LeftClampedRightClampedTopSimplySupportedBottomClamped','LeftClampedRightClampedTopSimplySupportedBottomSimplySupported','LeftClampedRightClampedTopSimplySupportedBottomFree','LeftClampedRightClampedTopFreeBottomClamped','LeftClampedRightClampedTopFreeBottomSimplySupported','LeftClampedRightClampedTopFreeBottomFree','LeftClampedRightSimplySupportedTopClampedBottomClamped','LeftClampedRightSimplySupportedTopClampedBottomSimplySupported','LeftClampedRightSimplySupportedTopClampedBottomFree','LeftClampedRightSimplySupportedTopSimplySupportedBottomClamped','LeftClampedRightSimplySupportedTopSimplySupportedBottomSimplySupported','LeftClampedRightSimplySupportedTopSimplySupportedBottomFree','LeftClampedRightSimplySupportedTopFreeBottomClamped','LeftClampedRightSimplySupportedTopFreeBottomSimplySupported','LeftClampedRightSimplySupportedTopFreeBottomFree','LeftClampedRightFreeTopClampedBottomClamped','LeftClampedRightFreeTopClampedBottomSimplySupported','LeftClampedRightFreeTopClampedBottomFree','LeftClampedRightFreeTopSimplySupportedBottomClamped','LeftClampedRightFreeTopSimplySupportedBottomSimplySupported','LeftClampedRightFreeTopSimplySupportedBottomFree','LeftClampedRightFreeTopFreeBottomClamped','LeftClampedRightFreeTopFreeBottomSimplySupported','LeftClampedRightFreeTopFreeBottomFree','LeftSimplySupportedRightClampedTopClampedBottomClamped','LeftSimplySupportedRightClampedTopClampedBottomSimplySupported','LeftSimplySupportedRightClampedTopClampedBottomFree','LeftSimplySupportedRightClampedTopSimplySupportedBottomClamped','LeftSimplySupportedRightClampedTopSimplySupportedBottomSimplySupported','LeftSimplySupportedRightClampedTopSimplySupportedBottomFree','LeftSimplySupportedRightClampedTopFreeBottomClamped','LeftSimplySupportedRightClampedTopFreeBottomSimplySupported','LeftSimplySupportedRightClampedTopFreeBottomFree','LeftSimplySupportedRightSimplySupportedTopClampedBottomClamped','LeftSimplySupportedRightSimplySupportedTopClampedBottomSimplySupported','LeftSimplySupportedRightSimplySupportedTopClampedBottomFree','LeftSimplySupportedRightSimplySupportedTopSimplySupportedBottomClamped','AllSidesSimplySupported','LeftSimplySupportedRightSimplySupportedTopSimplySupportedBottomFree','LeftSimplySupportedRightSimplySupportedTopFreeBottomClamped','LeftSimplySupportedRightSimplySupportedTopFreeBottomSimplySupported','LeftSimplySupportedRightSimplySupportedTopFreeBottomFree','LeftSimplySupportedRightFreeTopClampedBottomClamped','LeftSimplySupportedRightFreeTopClampedBottomSimplySupported','LeftSimplySupportedRightFreeTopClampedBottomFree','LeftSimplySupportedRightFreeTopSimplySupportedBottomClamped','LeftSimplySupportedRightFreeTopSimplySupportedBottomSimplySupported','LeftSimplySupportedRightFreeTopSimplySupportedBottomFree','LeftSimplySupportedRightFreeTopFreeBottomClamped','LeftSimplySupportedRightFreeTopFreeBottomSimplySupported','LeftSimplySupportedRightFreeTopFreeBottomFree','LeftFreeRightClampedTopClampedBottomClamped','LeftFreeRightClampedTopClampedBottomSimplySupported','LeftFreeRightClampedTopClampedBottomFree','LeftFreeRightClampedTopSimplySupportedBottomClamped','LeftFreeRightClampedTopSimplySupportedBottomSimplySupported','LeftFreeRightClampedTopSimplySupportedBottomFree','LeftFreeRightClampedTopFreeBottomClamped','LeftFreeRightClampedTopFreeBottomSimplySupported','LeftFreeRightClampedTopFreeBottomFree','LeftFreeRightSimplySupportedTopClampedBottomClamped','LeftFreeRightSimplySupportedTopClampedBottomSimplySupported','LeftFreeRightSimplySupportedTopClampedBottomFree','LeftFreeRightSimplySupportedTopSimplySupportedBottomClamped','LeftFreeRightSimplySupportedTopSimplySupportedBottomSimplySupported','LeftFreeRightSimplySupportedTopSimplySupportedBottomFree','LeftFreeRightSimplySupportedTopFreeBottomClamped','LeftFreeRightSimplySupportedTopFreeBottomSimplySupported','LeftFreeRightSimplySupportedTopFreeBottomFree','LeftFreeRightFreeTopClampedBottomClamped','LeftFreeRightFreeTopClampedBottomSimplySupported','LeftFreeRightFreeTopClampedBottomFree','LeftFreeRightFreeTopSimplySupportedBottomClamped','LeftFreeRightFreeTopSimplySupportedBottomSimplySupported','LeftFreeRightFreeTopSimplySupportedBottomFree','LeftFreeRightFreeTopFreeBottomClamped','LeftFreeRightFreeTopFreeBottomSimplySupported','AllSidesFree')

  """@classmethod
  def __generateBoundaryConds(cls):
    conds = ['Clamped','SimplySupported','Free']; cls.validBoundaryConds = 81*[None]; i=0
    for cond0 in conds:
      for cond1 in conds:
        for cond2 in conds:
          for cond3 in conds:
            if cond0 == cond1 == cond2 == cond3:
              cls.validBoundaryConds[i] = 'AllSides' + cond0
            else:
              cls.validBoundaryConds[i] = 'Left' + cond0 + 'Right' + cond1 + 'Top' + cond2 + 'Bottom' + cond3
            i+=1"""

  def __init__(self,gamma=200,kappa=1,b1=0,b2=0,boundaryCond='AllSidesSimplySupported',epsilon=1,nu=0.3):
    FDObjectBase.__init__(self,gamma,kappa,b1,b2,boundaryCond)
    #self.__generateBoundaryConds()
    self._epsilon = epsilon
    self._nu = nu

  @property
  def epsilon(self):
    """domain aspect ratio: epsilon=Lx/Ly"""
    return self._epsilon

  @property
  def nu(self):
    """boundary condition parameter: for steel approx 0.3"""
    return self._nu

  @epsilon.setter
  def epsilon(self,newEpsilon):
    if newEpsilon > 0:
      self._epsilon = newEpsilon
    else:
      raise ValueError('argument epsilon has to be a real number greater than 0')

  @nu.setter
  def nu(self,newNu):
    """not sure what allowed range of nu is supposed to be, check later"""
    self._nu = newNu

  # public methods
  def constrUpdateMatrices(self):
    self.__calcGridStep()       # calculate grid step
    k = self.__class__.k; _lambda = self.gamma*k/self.h; mu = self.kappa*k/self.h**2
    zeta = 2*self.b2*k/self.h**2; den = 1 + self.b1*k; Nx = self.Nx; Ny = self.Ny

    # create update matrices in sparse diagonal form
    Dlapl = laplacian_matrix_2d(Nx,Ny,self.boundaryCond)
    I = identity(self.Nm)
    self.B = (2*I - mu**2*biharm_matrix_2d(Nx,Ny,self.boundaryCond) + (_lambda**2 + zeta)*Dlapl)/den
    self.C = -((1 - self.b1*k)*I + zeta*Dlapl)/den

  def constrCouplingMatrices(self):
    k = self.__class__.k; den = 1 + self.b1*k
    self.C1 = self.B.copy()*den; self.C2 = self.C.copy()*den
    self.C1.setdiag(-1*(self.C1.diagonal() - 2)); self.C2.setdiag(-1*(self.C2.diagonal() + (1 - self.b1*k)))

  # private methods
  def __calcGridStep(self):
    k = self.__class__.k; a = self.gamma**2*k**2 + 4*self.b2*k
    self.h = sqrt(a + sqrt(a**2 + 16*self.kappa**2*k**2))
    self.Nx = int(sqrt(self.epsilon)/self.h)
    self.Ny = int(1/(sqrt(self.epsilon)*self.h))
    self.Nm = (self.Nx - 1)*(self.Ny - 1)
    self.N = (self.Nx,self.Ny,self.epsilon)
    self.h = sqrt(self.epsilon)/self.Nx
