
from math import sqrt

from scipy.sparse import identity

from .ResonatorBase import ResonatorBase
from .sparse_diff_matr_1d import (
    BOUNDARY_CONDITIONS_1D, second_difference_matrix, fourth_difference_matrix)


class Resonator1D(ResonatorBase):
    valid_boundaries = BOUNDARY_CONDITIONS_1D

    def __init__(self, gamma=200, kappa=1, b1=0, b2=0, boundary='SS', sr=44100):
        super().__init__(gamma, kappa, b1, b2, boundary, sr)

    def constr_update_matrices(self):
        self._calc_grid_step()

        k = self.k
        _lambda2 = (self.gamma * k / self.h) ** 2
        mu2 = (self.kappa * k / self.h ** 2) ** 2
        zeta = 2. * self.b2 * k / self.h ** 2
        den = 1. + self.b1 * k
        N = self.N

        Dxx = second_difference_matrix(N, self.boundary)
        self.Nm = Dxx.shape[0]
        I = identity(self.Nm)

        if 'F' not in self.boundary:
            self.B = (
                (2. * I + (_lambda2 + zeta) * Dxx -
                mu2 * fourth_difference_matrix(N, self.boundary)) / den)
            self.C = -((1. - self.b1 * k) * I + zeta * Dxx) / den
        else:
            Dxxxx = fourth_difference_matrix(
                N, self.boundary, {'a0': 1. + _lambda2 + zeta,
                'a1': -(2 + _lambda2 + zeta), 'a2': -zeta})
            self.B = (2. * I + (_lambda2 + zeta) * Dxx - mu2*Dxxxx[0]) / den
            self.C = (
                -((1. - self.b1 * k) * I + zeta * Dxx - mu2 * Dxxxx[1]) / den)

    def constr_coupling_matrices(self):
        k = self.k
        h = self.h
        N = self.N
        a = 2. * self.b2 * k / h ** 2

        _lambda2 = (self.gamma * k / self.h) ** 2
        zeta = 2. * self.b2 * k / self.h ** 2
        mu2 = (self.kappa * k / h ** 2) ** 2

        Dxx = second_difference_matrix(N, self.boundary)

        if 'F' not in self.boundary:
            self.C1 = (
                (_lambda2 + zeta) * Dxx -
                mu2 * fourth_difference_matrix(N, self.boundary))
            self.C2 = -zeta * Dxx
        else:
            Dxxxx = fourth_difference_matrix(
                N, self.boundary, {'a0': 1. + _lambda2 + zeta,
                'a1': -2. - _lambda2 - zeta,'a2': -zeta})
            self.C1 = (_lambda2 + zeta) * Dxx - mu2 * Dxxxx[0]
            self.C2 = -zeta * Dxx - mu2 * Dxxxx[1]

    def _calc_grid_step(self):
        k = self.k
        a = self.gamma ** 2 * k ** 2 + 4. * self.b2 * k
        self.h = sqrt(0.5 * (a + sqrt(a ** 2 + 16. * self.kappa ** 2 * k ** 2)))
        self.N = int(1. / self.h)
        self.h = 1. / self.N
