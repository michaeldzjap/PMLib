
class ResonatorBase():
    SR = 44100
    k = 1 / SR

    def __init__(self, gamma=200, kappa=1, b1=0, b2=0, boundary=None):
        self.gamma = gamma
        self.kappa = kappa
        self.b1 = b1
        self.b2 = b2
        self.boundary = boundary

    @property
    def gamma(self):
        """Spatially scaled wave speed of the string."""
        return self._gamma

    @gamma.setter
    def gamma(self, value):
        sr2 = self.SR / 2
        if 0 <= value <= sr2:
            self._gamma = value
        else:
            raise ValueError(f'argument gamma out of the range 0 - {sr2}')

    @property
    def kappa(self):
        """Spatially scaled stiffness coefficient."""
        return self._kappa

    @kappa.setter
    def kappa(self, value):
        if value >= 0:
            self._kappa = value
        else:
            raise ValueError('argument kappa must be >= 0')

    @property
    def b1(self):
        """Frequency independent damping constant of the string."""
        return self._b1

    @b1.setter
    def b1(self, value):
        if value >= 0:
            self._b1 = value
        else:
            raise ValueError('argument b1 must be >= 0')

    @property
    def b2(self):
        """Frequency dependent damping constant of the string."""
        return self._b2

    @b2.setter
    def b2(self, value):
        if value >= 0:
            self._b2 = value
        else:
            raise ValueError('argument b2 must be >= 0')

    @property
    def boundary(self):
        """Boundary condition of the object."""
        return self._boundary

    @boundary.setter
    def boundary(self, value):
        if value in type(self).valid_boundaries:
            self._boundary = value
        else:
            raise ValueError(
                'argument boundary is not a valid boundary condition')
