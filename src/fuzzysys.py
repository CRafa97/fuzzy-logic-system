from fuzzyset import *
from fuzzynumbers import *
from utils import *

class FuzzyInferenceSystem:
    def __init__(self, rules):
        self.rules = rules
        self.antc = [ r[:-1] for r in rules ]
        self.precs = [ r[-1] for r in rules ]

    # aggregation methods

    def aggregation_method(self, inputs, method="mamdani", input_type="singleton"):
        operator = FuzzyInferenceSystem.__dict__[method]
        dgs_operator = FuzzyInferenceSystem.__dict__[f"{input_type}_degrees"]
        dgs = dgs_operator(self, inputs)
        miuc = lambda z: max( operator(self, degree, prec, z) for degree, prec in zip(dgs, self.precs) )
        domain = join([prec.domain for prec in self.precs])
        return FuzzySet(membership=miuc, domain=domain)

    def mamdani(self, degree, prec, z):
        return min (degree, prec.membership(z))

    def larsen(self, degree, prec, z):
        return degree * prec.membership(z)

    def singleton_degrees(self, inputs):
        dgs = []
        for antc in self.antc:
            dgs.append( min (s.membership(i) for s, i in zip(antc, inputs)) )
        return dgs

    def fuzzy_degrees(self, inputs):

        def _common(f, s):
            import numpy as np
            inf, sup = join([f.domain, s.domain])
            return max( min(f.membership(x), s.membership(x)) for x in np.arange(inf, sup + 1, 0.1) )

        dgs = []
        for antc in self.antc:
            maxs = []
            for f, i in zip(antc, inputs):
                maxs.append(_common(f, i))
            dgs.append(min(maxs))
        return dgs

    # defuzzification methods

    def MOM(self, fs):
        vals = []
        vmax = 0
        inf, sup = fs.domain
        for zj in range(inf, sup + 1):
            v = fs.membership(zj)
            if vmax < v:
                vmax = v
                vals = [zj]
            elif vmax == v:
                vals.append(zj)
            else:
                pass

        return sum(vals) / len(vals)

    def COA(self, fs):
        inf, sup = fs.domain
        n ,d = 0, 0
        for zj in range(inf, sup + 1):
            val = fs.membership(zj)
            n += zj * val
            d += val

        return n / d

    def BOA(self, fs):
        alpha, beta = fs.domain
        z0 = (alpha + beta) / 2

        while True:
            lf = simpson(fs.membership, alpha, z0)
            rg = simpson(fs.membership, z0, beta)

            if lf == rg:
                return z0
            elif lf > rg:
                beta = z0
            else:
                alpha = z0
            
            z0 = (alpha + beta) / 2

if __name__ == "__main__":
    A = TriangularFuzzyNumber(0, 2, 4)
    B = TriangularFuzzyNumber(3, 4, 5)
    C = TriangularFuzzyNumber(0, 1, 2)
    D = TriangularFuzzyNumber(2, 3, 4)
    E = TriangularFuzzyNumber(2, 4, 6)

    rules = [(A, B)]
    system = FuzzyInferenceSystem(rules)
    res = system.aggregation_method((C,), method="larsen", input_type="fuzzy")
    des = system.MOM(res)
    print(des)