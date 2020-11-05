class TriangularFuzzyNumber:
    def __init__(self, inf, pk, sup):
        self.inf = inf
        self.pk = pk
        self.sup = sup

    def __call__(self, x):
        "Membership function"
        return (self.inf <= x < self.pk) * (x - self.inf) / (self.pk - self.inf) + \
               (self.pk <= x <= self.sup) * (self.sup - x ) / (self.sup - self.pk)

    # define operations

class TrapezoidalFuzzyNumber:
    def __init__(self, inf, pk1, pk2, sup):
        self.inf = inf
        self.pk1 = pk1
        self.pk2 = pk2
        self.sup = sup

    def __call__(self, x):
        "Membership function"
        return (self.inf <= x < self.pk1) * (x - self.inf) / (self.pk1 - self.inf) + \
               (self.pk1 <= x < self.pk2) + \
               (self.pk2 <= x <= self.sup) * (self.sup - x) / (self.sup - self.pk2)