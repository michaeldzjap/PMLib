from FDObjectBase import FDObjectBase
from FDString import FDString
from FDPlate import FDPlate
from sparse_add import spdistr1D,spdistr2D
from scipy.sparse import lil_matrix,coo_matrix,identity,hstack,vstack,csc_matrix
from scipy.linalg import solve
from scipy.linalg import eig
from math import pi
import scipy as sp
import numpy as np
import time
from numbers import Number

class FDObjNetwork(FDObjectBase):

  def __init__(self,objs=None,connPointMatrix=None,massMatrix=None,excPointMatrix=None,readoutPointMatrix=None):
    if objs == None:
      self._objs = [FDString(),FDString(101)]
    else:
      self._objs = objs
    if connPointMatrix == None:
      self._connPointMatrix = np.array([[0.5],[0.5]])
    else:
      self._connPointMatrix = connPointMatrix
    if massMatrix == None:
      self._massMatrix = np.array([[1.],[1.]])
    else:
      self._massMatrix = massMatrix
    if excPointMatrix == None:
      self._excPointMatrix = np.array([[0.5],[0.]])
    else:
      self._excPointMatrix = excPointMatrix
    if readoutPointMatrix == None:
      self.readoutPointMatrix = np.array([0.4,0.])
    else:
      self.readoutPointMatrix = readoutPointMatrix

  @property
  def objs(self):
    return self._objs

  @property
  def connPointMatrix(self):
    return self._connPointMatrix

  @property
  def massMatrix(self):
    return self._massMatrix

  @property
  def excPointMatrix(self):
    return self._excPointMatrix

  @property
  def readoutPointMatrix(self):
    return self._readoutPointMatrix

  @objs.setter
  def objs(self,newObjs):
    try:
      [obj.k for obj in newObjs]
    except AttributeError:
      raise AttributeError('argument objs contains an invalid object')
    else:
      self._objs = newObjs[:]

  @connPointMatrix.setter
  def connPointMatrix(self,newConnPointMatrix):
    try:
      len(newConnPointMatrix)
    except TypeError:
      raise TypeError('argument connPointMatrix must be a 2D indexable object')
    else:
      if isinstance(newConnPointMatrix,list) or isinstance(newConnPointMatrix,tuple):
        newConnPointMatrix = np.array(newConnPointMatrix)
      self.__checkRangeOfArray(newConnPointMatrix,'connPointMatrix')
      self.__checkNrOfElmsInColOfArray(newConnPointMatrix,'connPointMatrix')
      self._connPointMatrix = np.asarray(newConnPointMatrix).copy()

  @massMatrix.setter
  def massMatrix(self,newmassMatrix):
    try:
      len(massMatrix)
    except TypeError:
      raise TypeError('argument massMatrix must be a 2D indexable object')
    else:
      if isinstance(newmassMatrix,list) or isinstance(newmassMatrix,tuple):
        newmassMatrix = np.array(newmassMatrix)
      self.__checkNrOfElmsInColOfArray(newmassMatrix,'massMatrix')
      self._massMatrix = np.asarray(newmassMatrix).copy()

  @excPointMatrix.setter
  def excPointMatrix(self,newExcPointMatrix):
    try:
      len(newExcPointMatrix)
    except TypeError:
      raise TypeError('argument excPointMatrix must be a 2D indexable object')
    else:
      if isinstance(newExcPointMatrix,list) or isinstance(newExcPointMatrix,tuple):
        newExcPointMatrix = np.array(newExcPointMatrix)
      self.__checkRangeOfArray(newExcPointMatrix,'excPointMatrix')
      self.__checkNrOfElmsInColOfArray(newExcPointMatrix,'excPointMatrix')
      self._excPointMatrix = np.asarray(newExcPointMatrix).copy()

  @readoutPointMatrix.setter
  def readoutPointMatrix(self,newReadoutPointMatrix):
    try:
      len(newReadoutPointMatrix)
    except TypeError:
      raise TypeError('argument readoutPointMatrix must be a 2D indexable object')
    else:
      if isinstance(newReadoutPointMatrix,list) or isinstance(newReadoutPointMatrix,tuple):
        newReadoutPointMatrix = np.array(newReadoutPointMatrix)
      self.__checkRangeOfArray(newReadoutPointMatrix,'readoutPointMatrix')
      self._readoutPointMatrix = np.asarray(newReadoutPointMatrix).copy()

  # public methods
  def calcModes(self):
    stT = time.time()
    self.__checkDimensions()
    for m in self.objs:
      m.constrUpdateMatrices(); m.constrCouplingMatrices()
    self.Nt = [m.Nm for m in self.objs]          # cumulative is dimension of final block
    A = self.__constrStateTransitionMatrix()
    self._w,v = eig(A.todense())    # find eigenvalues and eigenvectors
    w_abs = np.abs(self._w)

    # construct input and output matrices and compute diagonalised versions
    self._B = solve(v,self.__constrInputMatrix().todense())
    self._S = self.__constrOutputMatrix()*v

    # discard eigenvalues and eigenvectors which are either purely real or purely imaginary
    # also discard any eigenvalues and eigenvectors if abs(w) >= 1
    i = 0
    while i < len(self._w):
      if abs(self._w[i].real) < 1e-09 or abs(self._w[i].imag) < 1e-09 or w_abs[i] >= 1.0:
        self._w = np.delete(self._w,i)
        w_abs = np.delete(w_abs,i)
        v = sp.delete(v,i,1)
        self._B = sp.delete(self._B,i,0)
        self._S = sp.delete(self._S,i,1)
      else:
        i += 1

    # sort from largest to smallest eigenvalue
    idx = self._w.argsort()[::-1]
    self._w = self._w[idx]; w_abs = w_abs[idx]
    v = v[idx,:]; self._B[idx,:]; self._S[:,idx]

    self._idx = np.r_[:len(self._w)/2]*2    # even indices for positive freqs only
    w_abs = w_abs[self._idx]
    beta = {'freq':self.__class__.SR*np.arccos(np.real(self._w[self._idx])/w_abs)/(2*pi),\
    't60':6.91*self.__class__.k/(1 - w_abs)}

    #for a,b,wa,w in zip(beta['freq'],beta['t60'],w_abs,self._w): print a,b,wa,w

    endT = time.time(); self.calcTime = endT - stT

    return beta

  def calcBiquadCoefs(self,gain=1):
    B = self._B; S = self._S; w = np.array(self._w)
    a1 = np.empty((S.shape[0],B.shape[1],len(w)/2)); a2 = np.empty((S.shape[0],B.shape[1],len(w)/2))
    # row index corresponds to output channel n, column index corresponds to input channel m,
    # e.g. a1_n,m are the real valued numerator coefficients corresponding to the combination of the
    # eigenvalues with the complex (after diagonalization) distributions of input channel m and output
    # channel n
    idx = self._idx
    for row,i in zip(S,xrange(0,S.shape[0])):
      for col,j in zip(B.T,xrange(0,B.shape[1])):
        for n,m in zip(idx,xrange(0,len(w)/2)):   # combine 2 1st order sections to make 1 2nd order section
          srbr = row[n].real*col[n].real; sibi = abs(row[n].imag)*abs(col[n].imag)
          a1[i,j,m] = gain*-2*(-srbr + sibi)
          a2[i,j,m] = gain*-2*((srbr - sibi)*w[n].real + \
          (row[n].real*abs(col[n].imag) + abs(row[n].imag)*col[n].real)*abs(w[n].imag))
    b1 = -2*w[idx].real; b2 = w[idx].real**2 + w[idx].imag**2

    return {'a1':a1,'a2':a2,'b1':b1,'b2':b2}

  # private methods
  def __checkRangeOfArray(self,mat,arg_name):
    for row in mat:
      for elm in row:
        if isinstance(elm,Number):
          if elm > 1:
            raise Exception('argument ' + arg_name + ' may only contain elements between 0 - 1')
        else:
          if elm[0] > 1 or elm[1] > 1:
            raise Exception('argument ' + arg_name + ' may only contain elements between 0 - 1')

  def __checkNrOfElmsInColOfArray(self,mat,arg_name):
    if np.any(np.sum(mat > 0,axis=0) > 2):
      raise Exception('argument ' + arg_name + ' may only contain 2 nonzero elements per column')

  def __checkDimOfColls(self,coll1,coll2,err_str):
    if isinstance(coll1,np.ndarray) and isinstance(coll2,np.ndarray):
      if coll1.shape[0] != coll2.shape[0]: raise Exception(err_str)
    elif (isinstance(coll1,list) or isinstance(coll1,tuple)) and isinstance(coll2,np.ndarray):
      if len(coll1) != coll2.shape[0]: raise Exception(err_str)
    elif isinstance(coll1,np.ndarray) and (isinstance(coll2,list) or isinstance(coll2,tuple)):
      if coll1.shape[0] != len(coll2): raise Exception(err_str)
    elif (isinstance(coll1,list) or isinstance(coll1,tuple)) and (isinstance(coll2,list) or isinstance(coll2,tuple)):
      if len(coll1) != len(coll2): raise Exception(err_str)

  def __checkDimensions(self):
    self.__checkDimOfColls(self.connPointMatrix,self.excPointMatrix,\
    'arguments connPointMatrix and excPointMatrix must contain an equal nr. of rows')
    self.__checkDimOfColls(self.connPointMatrix,self.objs,\
    'the nr. of rows of argument connPointMatrix must be equal to the nr. of elements in objs')
    self.__checkDimOfColls(self.excPointMatrix,self.objs,\
    'the nr. of rows of argument excPointMatrix must be equal to the nr. of elements in objs')
    self.__checkDimOfColls(self.readoutPointMatrix,self.objs,\
    'the nr. of rows of argument readoutPointMatrix must be equal to the nr. of elements in objs')

  def __iscoll(self,arr):
    if isinstance(arr,list) or isinstance(arr,tuple):
      return True
    else:
      return False

  # maybe not necessary
  def __checkCoordinatesForPlate(self,mat,arg_name):
    if any([[not(point == 0 or isinstance(point,list)) for point in mat[i][:]] for obj,i\
    in zip(self.objs,xrange(len(self.objs))) if isinstance(obj,FDPlate)][0]):
      raise Exception(arg_name + ' contains one or more invalid coordinates for a plate object')

  def __constrStateTransitionMatrix(self):
    k = self.__class__.k
    A = None    # state transtion block matrix
    # loop over all rows (i.e. individual objs) and find all connections with other objs
    for row,i,obj in zip(self.massMatrix,xrange(len(self.objs)),self.objs):
      fac = 1./(obj.h + obj.b1*k*obj.h)
      C1_total = csc_matrix((obj.Nm,obj.Nm)); C2_total = csc_matrix((obj.Nm,obj.Nm))
      C3_total = {}; C4_total = {}; A_row = None
      colInds = np.nonzero(row)[0]
      # for every connection between obj q and r other objects, construct inter-connection matrices
      for j in colInds:
        cpoint_q = self.connPointMatrix[i,j]
        e_q = spdistr2D(1,cpoint_q[0],cpoint_q[1],obj.Nx - 1,obj.Ny - 1,flatten=True)\
        if isinstance(obj,FDPlate) else spdistr1D(1,cpoint_q,obj.Nm,'lin')
        # return the row indices of the nonzero entrees in the current col we are looking in
        row_r = np.nonzero(self.massMatrix[:,j].copy())[0].tolist()
        # remove row index of current object and since list must now be of size 1, simply return row index
        row_r.remove(i); row_r = row_r[0]
        M = float(self.massMatrix[i,j])/self.massMatrix[row_r,j]    # mass ratio: Mq/Mr
        cpoint_r = self.connPointMatrix[row_r,j]
        e_r = spdistr2D(1,cpoint_r[0],cpoint_r[1],self.objs[row_r].Nx - 1,self.objs[row_r].Ny - 1,flatten=True) \
        if isinstance(self.objs[row_r],FDPlate) \
        else spdistr1D(1,cpoint_r,self.objs[row_r].Nm,'lin')
        c1 = fac/(e_q.T.dot(e_q)[0,0] + M*e_r.T.dot(e_r)[0,0])
        e_qCre_q = e_q*e_q.T; e_qCre_r = e_q*e_r.T
        C1_total = C1_total + c1*e_qCre_q*obj.C1
        C2_total = C2_total + c1*e_qCre_q*obj.C2
        if row_r in C3_total:   # save to assert that when C3[row_r] is empty, C4[row_r] is empty also
          C3_total[row_r] = C3_total[row_r] - c1*e_qCre_r*self.objs[row_r].C1
          C4_total[row_r] = C4_total[row_r] - c1*e_qCre_r*self.objs[row_r].C2
        else:
          C3_total[row_r] = -c1*e_qCre_r*self.objs[row_r].C1
          C4_total[row_r] = -c1*e_qCre_r*self.objs[row_r].C2

      # construct row of A for u[n]
      for j in xrange(0,len(self.objs)):
        if i == j:       # we're on the diagonal
          A_row = hstack((obj.B + C1_total,obj.C + C2_total),format="lil") if A_row == None else \
          hstack((A_row,obj.B + C1_total,obj.C + C2_total),format="lil")
        elif j in C3_total:
          A_row = hstack((C3_total[j],C4_total[j]),format="lil") if A_row == None else \
          hstack((A_row,C3_total[j],C4_total[j]),format="lil")
        else:
          A_row = lil_matrix((obj.Nm,self.objs[j].Nm*2)) if A_row == None else \
          hstack((A_row,lil_matrix((obj.Nm,self.objs[j].Nm*2))))

      # construct row of A for u[n - 1]
      if i == 0:   # first object, so identity matrix is first in row
        I = hstack((identity(obj.Nm,format="lil"),lil_matrix((obj.Nm,A_row.shape[1] - obj.Nm))))
      elif i == len(self.objs) - 1:   # last object, so identity matrix is penultimate to last col
        I = hstack((lil_matrix((obj.Nm,A_row.shape[1] - 2*self.objs[-1].Nm)),\
        identity(obj.Nm,format="lil"),lil_matrix((obj.Nm,obj.Nm))))
      else:   # if any other object, calc pos of identity matrix based on grid size N of each obj
        I = hstack((lil_matrix((obj.Nm,2*np.sum(self.Nt[:i]))),identity(obj.Nm),\
        lil_matrix((obj.Nm,obj.Nm + 2*np.sum(self.Nt[-(len(self.Nt) - 1 - i):])))))
      # append row to block state transition matrix A
      A = vstack((A_row,I)) if A == None else vstack((A,A_row,I))

    return A.tocsc()

  def __constrInputMatrix(self):
    B = None; k = self.__class__.k
    for row,obj in zip(self.excPointMatrix,self.objs):
      E = lil_matrix((obj.Nm*2,self.excPointMatrix.shape[1]))
      for ep,i in zip(row,xrange(0,len(row))):
        if ep > 0.0:
          E[:obj.Nm,i] = spdistr2D(k**2/((1 + obj.b1*k)*obj.h**2),ep[0],ep[1],obj.Nx - 1,obj.Ny - 1,flatten=True)\
          if isinstance(obj,FDPlate) else spdistr1D(k**2/((1 + obj.b1*k)*obj.h),ep,obj.Nm,'lin')
      B = E if B == None else vstack((B,E))

    return B.tocsc()

  def __constrOutputMatrix(self):
    S = None; k = self.__class__.k
    for col in self.readoutPointMatrix.T:
      E = None
      for rp,obj in zip(col,self.objs):
        if rp > 0.0:
          e = spdistr2D(1/(k*obj.h**2),rp[0],rp[1],obj.Nx - 1,obj.Ny - 1,flatten=True).T\
          if isinstance(obj,FDPlate) else spdistr1D(1/(k*obj.h),rp,obj.Nm,'lin').T
          E = hstack((e,-e)) if E == None else hstack((E,e,-e))
        else:
          e = lil_matrix((1,obj.Nm*2))
          E = e if E == None else hstack((E,e))
      S = E if S == None else vstack((S,E))

    return S.tocsc()
