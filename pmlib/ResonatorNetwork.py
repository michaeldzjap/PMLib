
from math import pi
from numbers import Number
import os
import json
import sys

from scipy.sparse import lil_matrix, identity, hstack, vstack, csc_matrix
from scipy.linalg import solve
from scipy.linalg import eig

import numpy as np

from .ResonatorBase import ResonatorBase
from .Resonator1D import Resonator1D
from .Resonator2D import Resonator2D
from .sparse_add import spdistr1D, spdistr2D


class ResonatorNetwork():
    def __init__(self, objs=None, connPointMatrix=None, massMatrix=None,
                 excPointMatrix=None, readoutPointMatrix=None, sr=44100):
        self.sr = sr
        self.k = 1 / sr
        self.objs = objs or [Resonator1D(), Resonator1D(101)]
        self.connPointMatrix = connPointMatrix or [[0.5], [0.5]]
        self.massMatrix = massMatrix or [[1.], [1.]]
        self.excPointMatrix = excPointMatrix or [[0.5], [0.]]
        self.readoutPointMatrix = readoutPointMatrix or [[0.4], [0.]]

    @property
    def objs(self):
        return self._objs

    @objs.setter
    def objs(self, value):
        t = (ResonatorBase, ResonatorNetwork)
        if all(isinstance(o, t) for o in value):
            self._objs = value[:]
        else:
            raise TypeError('objs value contains an invalid object')

    # FIXME: Checks here for each property and later with _check_dimensions.

    @property
    def connPointMatrix(self):
        return self._connPointMatrix

    @connPointMatrix.setter
    def connPointMatrix(self, value):
        if len(value) != 2:
            raise ValueError(
                'connPointMatrix value must be a 2D indexable object')
        else:
            self._check_array_range(value, 'connPointMatrix')
            self._check_array_column(value, 'connPointMatrix')
            self._connPointMatrix = value

    @property
    def massMatrix(self):
        return self._massMatrix

    @massMatrix.setter
    def massMatrix(self, value):
        if len(value) != 2:
            raise ValueError('massMatrix value must be a 2D indexable object')
        else:
            self._check_array_column(value, 'massMatrix')
            self._massMatrix = value

    @property
    def excPointMatrix(self):
        return self._excPointMatrix

    @excPointMatrix.setter
    def excPointMatrix(self, value):
        if len(value) != 2:
            raise ValueError(
                'excPointMatrix value must be a 2D indexable object')
        else:
            self._check_array_range(value, 'excPointMatrix')
            self._excPointMatrix = value

    @property
    def readoutPointMatrix(self):
        return self._readoutPointMatrix

    @readoutPointMatrix.setter
    def readoutPointMatrix(self, value):
        if len(value) != 2:
            raise ValueError(
                'readoutPointMatrix value must be a 2D indexable object')
        else:
            self._check_array_range(value, 'readoutPointMatrix')
            self._readoutPointMatrix = value

    def calc_modes(self, min_freq, max_freq, min_T60=0.01):
        self._check_dimensions()
        for m in self.objs:
            m.constr_update_matrices()
            m.constr_coupling_matrices()
        self.Nt = [m.Nm for m in self.objs]  # cumulative is dimension of final block
        A = self._constr_state_transition_matrix()
        _lambda, v = eig(A.todense())  # find eigenvalues and eigenvectors
        lambda_abs = np.abs(_lambda)

        # construct input and output matrices and compute diagonalised versions
        self._B = solve(v, self._constr_input_matrix().todense())
        self._S = self._constr_output_matrix() * v

        # filter modes
        wmax = 2. * pi * max_freq / self.sr
        wmin = 2. * pi * min_freq / self.sr
        rmin = 1. - 6.91 / (min_T60 * self.sr)
        lambda_arg = np.arccos(_lambda.real / lambda_abs)
        idx = (
            (_lambda.imag >= 0.) & (lambda_abs < 1.) & (lambda_arg >= wmin) &
            (lambda_arg <= wmax) & (lambda_abs >= rmin))
        _lambda = _lambda[idx]
        lambda_abs = lambda_abs[idx]
        lambda_arg = lambda_arg[idx]
        v = v[:,idx]
        self._B = self._B[idx,:]
        self._S = self._S[:,idx]

        # sort from largest to smallest eigenvalue
        idx = _lambda.argsort()[::-1]
        self.eigenvalues = _lambda[idx]
        self.angle = lambda_arg[idx]
        self.radius = lambda_abs[idx]
        self.eigenvectors = v[idx,:]
        self._B = self._B[idx,:]
        self._S = self._S[:,idx]

    def calc_biquad_coefs(self, gain=1):
        try:
            lambda_real = self.eigenvalues.real
            lambda_imag = self.eigenvalues.imag
            Sr = self._S.real
            Si = self._S.imag
            Br = self._B.real
            Bi = self._B.imag
            a1 = gain * -2. * (
                np.einsum('in,nj->ijn', -Sr, Br) +
                np.einsum('in,nj->ijn', Si, Bi))
            a2 = gain * -2. * (
                np.einsum('in,nj,n->ijn', Sr, Br, lambda_real) -
                np.einsum('in,nj,n->ijn', Si, Bi, lambda_real) +
                np.einsum('in,nj,n->ijn', Sr, Bi, lambda_imag) +
                np.einsum('in,nj,n->ijn', Si, Br, lambda_imag))
            b1 = -2. * lambda_real
            b2 = self.radius ** 2
            self.biquadCoefs = {'a1': a1, 'a2': a2, 'b1': b1, 'b2': b2}
        except AttributeError:
            raise Exception(
                'eigenvalues are not calculated, '
                'please execute calc_modes first') from None  # NOTE: Computers don't know 'please'.

    def save_json(self, path=None, include='yyyy'):
        try:
            path = path or os.path.dirname(os.path.realpath(__file__)) + '/modalData.json'
            if not path.endswith('.json'):
                path += '.json'

            data = dict()
            for i, char in enumerate(include):
                if char == 'y':
                    if i == 0:
                        coefs = dict()
                        for key in self.biquadCoefs:
                            coefs[key] = self.biquadCoefs[key].tolist()
                        data['biquadCoefs'] = coefs
                    elif i == 1:
                        data['eigenvaluesPolar'] = {
                            'radius': self.radius.tolist(),
                            'angle': self.angle.tolist()}
                    elif i == 2:
                        data['eigenvaluesRect'] = {
                            'real': self.eigenvalues.real.tolist(),
                            'imag': self.eigenvalues.imag.tolist()}
                    elif i == 3:
                        data['eigenvectors'] = {
                            'real': self.eigenvectors.real.tolist(),
                            'imag': self.eigenvectors.imag.tolist()}

            with open(path, 'w') as outfile:
                json.dump(data, outfile)
            return True
        except:
            print(sys.exc_info())
            return False

    def _check_array_range(self, mat, arg_name):
        for row in mat:
            for elm in row:
                if isinstance(elm, Number):
                    if elm > 1:
                        raise ValueError(
                            f'argument {arg_name} may only '
                            'contain elements between 0 - 1')
                else:
                    if elm[0] > 1 or elm[1] > 1:
                        raise ValueError(
                            f'argument {arg_name} may only '
                            'contain elements between 0 - 1')

    def _check_array_column(self, mat, arg_name):
        # if np.any(np.sum(mat > 0, axis=0) > 2):
        if any(sum(mat[p][q] > 0 for p in range(len(mat))) for q in range(len(mat[0]))) > 2:  # BUG: any returns True/False
            raise ValueError(
                f'argument {arg_name} may only contain '
                '2 nonzero elements per column')

    def _check_colls_dim(self, coll1, coll2, err_str):
        # FIXME: It could be better to only allow one type
        # or make a cast when values are first entered
        # instead of having to check all combinations.
        if isinstance(coll1, np.ndarray) and isinstance(coll2, np.ndarray):
            if coll1.shape[0] != coll2.shape[0]: raise Exception(err_str)
        elif (isinstance(coll1, list) or isinstance(coll1, tuple)) and isinstance(coll2, np.ndarray):
            if len(coll1) != coll2.shape[0]: raise Exception(err_str)
        elif isinstance(coll1, np.ndarray) and (isinstance(coll2, list) or isinstance(coll2, tuple)):
            if coll1.shape[0] != len(coll2): raise Exception(err_str)
        elif (isinstance(coll1, list) or isinstance(coll1, tuple)) and (isinstance(coll2, list) or isinstance(coll2, tuple)):
            if len(coll1) != len(coll2): raise Exception(err_str)

    def _check_dimensions(self):
        self._check_colls_dim(self.connPointMatrix,self.excPointMatrix,\
        'arguments connPointMatrix and excPointMatrix must contain an equal nr. of rows')
        self._check_colls_dim(self.connPointMatrix,self.objs,\
        'the nr. of rows of argument connPointMatrix must be equal to the nr. of elements in objs')
        self._check_colls_dim(self.excPointMatrix,self.objs,\
        'the nr. of rows of argument excPointMatrix must be equal to the nr. of elements in objs')
        self._check_colls_dim(self.readoutPointMatrix,self.objs,\
        'the nr. of rows of argument readoutPointMatrix must be equal to the nr. of elements in objs')

    # def _iscoll(self,arr):
    #     if isinstance(arr, (list, tuple)):
    #         return True
    #     else:
    #         return False

    # # maybe not necessary
    # def _checkCoordinatesForPlate(self, mat, arg_name):
    #     if any([[not(point == 0 or isinstance(point,list)) for point in mat[i][:]] for obj,i\
    #     in zip(self.objs,range(len(self.objs))) if isinstance(obj,Resonator2D)][0]):
    #         raise Exception(arg_name + ' contains one or more invalid coordinates for a plate object')

    def _constr_state_transition_matrix(self):
        k = self.k
        A = None  # state transtion block matrix

        # Loop over all rows (i.e. individual objs) and
        # find all connections with other objs.
        for row, i, obj in zip(self.massMatrix, range(len(self.objs)), self.objs):
            fac = 1. / (1. + obj.b1 * k)
            fac /= obj.h ** 2 if isinstance(obj, Resonator2D) else obj.h
            C1_total = csc_matrix((obj.Nm, obj.Nm))
            C2_total = csc_matrix((obj.Nm,obj.Nm))
            C3_total = dict()
            C4_total = dict()
            A_row = None
            colInds = np.nonzero(row)[0]

            # For every connection between obj q and r other
            # objects, construct inter-connection matrices.
            for j in colInds:
                cpoint_q = self.connPointMatrix[i][j]
                if isinstance(obj, Resonator2D):
                    e_q = spdistr2D(
                        1., cpoint_q[0], cpoint_q[1],
                        obj.Nx - 1,
                        obj.Ny - 1,
                        flatten=True)
                else:
                    e_q = spdistr1D(1., cpoint_q, obj.Nm, 'lin')

                # Return the row indices of the nonzero entrees
                # in the current col we are looking in.
                row_r = [
                    ind for ind, item in enumerate([self.massMatrix[q][j]
                    for q in range(len(self.massMatrix))]) if item > 0]

                # Remove row index of current object and since list must
                # now be of size 1, simply return row index.
                row_r.remove(i)
                row_r = row_r[0]
                M = float(self.massMatrix[i][j]) / self.massMatrix[row_r][j]  # mass ratio: Mq/Mr
                cpoint_r = self.connPointMatrix[row_r][j]

                if isinstance(self.objs[row_r], Resonator2D):
                    e_r = spdistr2D(
                        1., cpoint_r[0], cpoint_r[1],
                        self.objs[row_r].Nx - 1,
                        self.objs[row_r].Ny - 1,
                        flatten=True)
                else:
                    e_r = spdistr1D(
                        1., cpoint_r, self.objs[row_r].B.shape[0], 'lin')

                c1 = fac / (e_q.T.dot(e_q)[0,0] + M * e_r.T.dot(e_r)[0,0])
                e_qCre_q = e_q*e_q.T
                e_qCre_r = e_q*e_r.T
                C1_total = C1_total + c1 * e_qCre_q * obj.C1
                C2_total = C2_total + c1 * e_qCre_q * obj.C2

                if row_r in C3_total:
                    # Save to assert that when C3[row_r]
                    # is empty, C4[row_r] is also empty.
                    C3_total[row_r] = (
                        C3_total[row_r] - c1 * e_qCre_r * self.objs[row_r].C1)
                    C4_total[row_r] = (
                        C4_total[row_r] - c1 * e_qCre_r * self.objs[row_r].C2)
                else:
                    C3_total[row_r] = -c1*e_qCre_r*self.objs[row_r].C1
                    C4_total[row_r] = -c1*e_qCre_r*self.objs[row_r].C2

            # Construct row of A for u[n].
            for j in range(0,len(self.objs)):
                if i == j:
                    # We're on the diagonal.
                    if A_row == None:
                        A_row = hstack(
                            (obj.B + C1_total, obj.C + C2_total), format="lil")
                    else:
                        A_row = hstack(
                            (A_row, obj.B + C1_total, obj.C + C2_total),
                            format="lil")
                elif j in C3_total:
                    if A_row == None:
                        A_row = hstack(
                            (C3_total[j], C4_total[j]), format="lil")
                    else:
                        A_row = hstack(
                            (A_row, C3_total[j], C4_total[j]), format="lil")
                else:
                    Nm2 = self.objs[j].Nm * 2
                    if A_row is None:
                        A_row = lil_matrix((obj.Nm, Nm2))
                    else:
                        A_row = hstack((A_row, lil_matrix((obj.Nm, Nm2))))

            # Construct row of A for u[n - 1]
            if i == 0:
                # First object, so identity matrix is first in row.
                I = hstack(
                    (identity(obj.Nm, format="lil"),
                    lil_matrix((obj.Nm, A_row.shape[1] - obj.Nm))))
            elif i == len(self.objs) - 1:
                # Last object, so identity matrix is penultimate to last col.
                I = hstack(
                    (lil_matrix((obj.Nm, A_row.shape[1] - 2 * self.objs[-1].Nm)),
                    identity(obj.Nm,format="lil"),lil_matrix((obj.Nm,obj.Nm))))
            else:
                # If any other object, calc pos of identity
                # matrix based on grid size N of each obj.
                I = hstack(
                    (lil_matrix((obj.Nm, 2 * np.sum(self.Nt[:i]))),
                    identity(obj.Nm),
                    lil_matrix((obj.Nm, obj.Nm + 2 * np.sum(self.Nt[-(len(self.Nt) - 1 - i):])))))
            # Append row to block state transition matrix A.
            A = vstack((A_row, I)) if A is None else vstack((A, A_row, I))

        return A.tocsc()

    def _constr_input_matrix(self):
        B = None
        k = self.k

        for row, obj in zip(self.excPointMatrix, self.objs):
            E = lil_matrix((obj.Nm * 2, len(self.excPointMatrix[0])))
            for i, ep in enumerate(row):
                if ep > 0.0:
                    if isinstance(obj, Resonator2D):
                        E[:obj.Nm,i] = spdistr2D(
                            k ** 2 / ((1. + obj.b1 * k) * obj.h ** 2),
                            ep[0], ep[1],
                            obj.Nx - 1, obj.Ny - 1,
                            flatten=True)
                    else:
                        E[:obj.Nm,i] = spdistr1D(
                            k ** 2 / ((1. + obj.b1 * k) * obj.h),
                            ep, obj.Nm, 'lin')
            B = E if B is None else vstack((B, E))

        return B.tocsc()

    def _constr_output_matrix(self):
        S = None
        k = self.k

        for col in [list(x) for x in zip(*self.readoutPointMatrix)]:  # transpose self.readoutPointMatrix
            E = None
            for rp, obj in zip(col, self.objs):
                if rp > 0.0:
                    if isinstance(obj, Resonator2D):
                        e = spdistr2D(
                            1. / k, rp[0], rp[1],
                            obj.Nx - 1,obj.Ny - 1,
                            flatten=True).T
                    else:
                        e = spdistr1D(1. / k, rp, obj.Nm, 'lin').T
                    E = hstack((e,-e)) if E is None else hstack((E,e,-e))
                else:
                    e = lil_matrix((1, obj.Nm * 2))
                    E = e if E is None else hstack((E, e))
            S = E if S is None else vstack((S, E))

        return S.tocsc()
