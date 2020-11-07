
from math import sqrt

from scipy.sparse import identity

from .ResonatorBase import ResonatorBase
from .sparse_diff_matr_2d import (
    BOUNDARY_CONDITIONS_2D, laplacian_matrix_2d, biharmonic_matrix_2d)


class Resonator2D(ResonatorBase):
    valid_boundaries = BOUNDARY_CONDITIONS_2D

    def __init__(self, gamma=200, kappa=1, b1=0, b2=0,
                 boundary='SSSS', epsilon=1):
        super().__init__(gamma, kappa, b1, b2, boundary)
        self._epsilon = epsilon

    @property
    def epsilon(self):
        """Domain aspect ratio: epsilon = Lx / Ly."""
        return self._epsilon

    @epsilon.setter
    def epsilon(self, value):
        if value > 0:
            self._epsilon = value
        else:
            raise ValueError('argument epsilon has to be > 0')

    def constr_update_matrices(self):
        self._calc_grid_step()

        k = type(self).k
        _lambda = self.gamma * k / self.h
        mu = self.kappa * k / self.h ** 2

        zeta = 2. * self.b2 * k / self.h ** 2
        den = 1. + self.b1 * k
        Nx = self.Nx
        Ny = self.Ny
        self.Nm = Nm = (Nx - 1) * (Ny - 1)

        # create update matrices in sparse diagonal form
        Dlapl = laplacian_matrix_2d(Nx, Ny, self.boundary)
        I = identity(Nm)

        self.B = (
            (2. * I - mu ** 2 * biharmonic_matrix_2d(Nx, Ny, self.boundary) +
            (_lambda**2 + zeta) * Dlapl) / den)
        self.C = -((1. - self.b1 * k) * I + zeta * Dlapl) / den

    def constr_coupling_matrices(self):
        k = type(self).k
        h = self.h
        a = 2. * self.b2 * k / (h ** 2)
        Nx = self.Nx
        Ny = self.Ny
        Dlapl = laplacian_matrix_2d(Nx, Ny, self.boundary)
        self.C1 = (
            ((self.gamma * k / h) ** 2 + a) * Dlapl -
            (self.kappa * k / (h ** 2)) ** 2 *
            biharmonic_matrix_2d(Nx, Ny, self.boundary))
        self.C2 = -a * Dlapl

    def _calc_grid_step(self):
        k = type(self).k
        a = self.gamma ** 2 * k ** 2 + 4. * self.b2 * k
        self.h = sqrt(a + sqrt(a ** 2 + 16. * self.kappa ** 2 * k ** 2))
        self.Nx = int(sqrt(self.epsilon) / self.h)
        self.Ny = int(1. / (sqrt(self.epsilon) * self.h))
        self.h = sqrt(self.epsilon) / self.Nx
