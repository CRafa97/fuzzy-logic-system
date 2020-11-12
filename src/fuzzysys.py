from fuzzyset import *
from fuzzynumbers import *
from utils import *

class FuzzyInferenceSystem:
    def __init__(self, rules):
        self.rules = rules
        self.antc = [ r[:-1] for r in rules ]
        self.precs = [ r[-1] for r in rules ]

    # aggregation methods

    def aggregation_method(self, inputs, method="mamdani"):
        dgs = self.degrees(inputs)
        operator = FuzzyInferenceSystem.__dict__[method]
        miuc = lambda z: max( operator(self, degree, prec, z) for degree, prec in zip(dgs, self.precs) )
        domain = join([prec.domain for prec in self.precs])
        return FuzzySet(membership=miuc, domain=domain)

    def mamdani(self, degree, prec, z):
        return min (degree, prec.membership(z))

    def larsen(self, degree, prec, z):
        return degree * prec.membership(z)

    def degrees(self, inputs):
        dgs = []
        for antc in self.antc:
            dgs.append( min (s.membership(i) for s, i in zip(antc, inputs)) )
        return dgs

    # defuzzification methods

    def MOM(self, fs):
        d = {}
        inf, sup = fs.domain
        for zj in range(inf, sup + 1):
            val = fs.membership(zj)
            try:
                d[val].append(zj)
            except:
                d[val] = [zj]

        vmax = max(d.keys())
        return sum(d[vmax]) / len(d[vmax])

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
    C = TriangularFuzzyNumber(3, 4, 5)

    rules = [(A, B, C)]
    system = FuzzyInferenceSystem(rules)
    res = system.aggregation_method((3, 4), method="larsen")
    des = system.MOM(res)
    print(des)