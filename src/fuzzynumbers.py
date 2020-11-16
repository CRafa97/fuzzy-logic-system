from fuzzyset import FuzzySet
from math import exp

class TriangularFuzzyNumber(FuzzySet):
    def __init__(self, inf, mid, sup):
        super().__init__(self._triangular_membership, (inf, sup))
        self.inf = inf
        self.mid = mid
        self.sup = sup

    def _triangular_membership(self, x):
        return (self.inf <= x < self.mid) * (x - self.inf) / (self.mid - self.inf) + \
               (self.mid <= x <= self.sup) * (self.sup - x ) / (self.sup - self.mid)

class TrapezoidalFuzzyNumber(FuzzySet):
    def __init__(self, inf, mid1, mid2, sup):
        super().__init__(self._trapezoidal_membership, (inf, sup))
        self.inf = inf
        self.mid1 = mid1
        self.mid2 = mid2
        self.sup = sup

    def _trapezoidal_membership(self, x):
        return (self.inf <= x < self.mid1) * (x - self.inf) / (self.mid1 - self.inf) + \
               (self.mid1 <= x < self.mid2) + \
               (self.mid2 <= x <= self.sup) * (self.sup - x) / (self.sup - self.mid2)

class GaussianFuzzyNumber(FuzzySet):
    def __init__(self, k, m, domain=(-20,20)): # predefined domain
        super().__init__(self._gaussian_membership, domain)
        self.k = k
        self.m = m

    def _gaussian_membership(self, x):
        return exp(-self.k * (x - self.m)**2)

class SigmoidalFuzzyNumber(FuzzySet):
    def __init__(self, inf, sup):
        super().__init__(self._sigmoidal_membership, domain=(inf, sup))
        self.inf = inf
        self.sup = sup
        self.m = (inf + sup) / 2

    def _sigmoidal_membership(self, x):
        return (x <= self.inf) + \
               (self.inf < x <= self.m) * (2 * ((x - self.inf) / (self.sup - self.inf))**2 ) + \
               (self.m < x < self.sup) * (1 - (2 * ( (x - self.sup) / (self.sup - self.inf) )**2 ) ) + \
               (x >= self.sup)

# Negation Operation

class FuzzyNegation(FuzzySet):
    def __init__(self, fs):
        super().__init__(self._neg_membership, domain=fs.domain)
        self.fs = fs

    def _neg_membership(self, x):
        return 1 - self.fs.membership(x)

# Modifiers

class FuzzyVery(FuzzySet):
    def __init__(self, fs):
        super().__init__(self._very_membership, domain=fs.domain)
        self.fs = fs

    def _very_membership(self, x):
        return self.fs.membership(x)**2

class FuzzyFairly(FuzzySet):
    def __init__(self, fs):
        super().__init__(self._fairly_membership, domain=fs.domain)
        self.fs = fs

    def _fairly_membership(self, x):
        return self.fs.membership(x)**(1/2)