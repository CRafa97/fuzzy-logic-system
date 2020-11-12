from fuzzyset import FuzzySet

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