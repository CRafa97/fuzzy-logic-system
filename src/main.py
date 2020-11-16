from fuzzynumbers import *
from fuzzysys import FuzzyInferenceSystem

# Fuzzification

# Linguistic: Distance
far = SigmoidalFuzzyNumber(20, 30)
normal = GaussianFuzzyNumber(k=0.05, m=15, domain=(0, 30))
near = FuzzyNegation(SigmoidalFuzzyNumber(0, 5))

# Linguistic: Object Speed
move = SigmoidalFuzzyNumber(10, 20)
move_slow = FuzzyFairly(move)
move_fast = FuzzyVery(move)
keep = TrapezoidalFuzzyNumber(-1, 0, 9, 20)

# Linguistic: Car Speed 
slow = FuzzyNegation(SigmoidalFuzzyNumber(10, 30))
constant = GaussianFuzzyNumber(k=0.05, m=45, domain=(10, 90))
fast = SigmoidalFuzzyNumber(60, 90)

# Linguistic: Brake Degree (0-60)
nothing = FuzzySet(lambda x: x == 0, domain=(0,60))
small = TriangularFuzzyNumber(1, 10, 20)
medium = TriangularFuzzyNumber(21, 30, 40)
big = TriangularFuzzyNumber(41, 50, 59)
complete = FuzzySet(lambda x: x == 60, domain=(0,60))

# System Rules
# (Distance, Car Speed, Object Speed) -> Brake Degree

rules = [
    (far, slow, keep, nothing),
    (normal, slow, keep, small),
    (normal, constant, keep, medium),
    (near, constant, keep, big),
    (near, fast, keep, complete),

    (near, fast, move_slow, big),
    (normal, constant, move_slow, medium),
    (far, constant, move_slow, small),
    (near, constant, move_fast, small),
    (normal, slow, move_fast, nothing),
]

def main():
    fsys = FuzzyInferenceSystem(rules=rules)

    test = (10, 40, 1,)

    # Test1 (mamdani - COA): 10, 40, 1 - ?
    print("--- Test Mamdani - COA --- ")
    res1 = fsys.aggregation_method(test, method="mamdani", input_type="singleton")
    desf1 = fsys.COA(res1)
    print(f"Grado: {desf1}\n")

    # Test2 (mamdani - MOM): 10, 40, 1 - ?
    print("--- Test Mamdani - MOM --- ")
    res2 = fsys.aggregation_method(test, method="mamdani", input_type="singleton")
    desf2 = fsys.MOM(res2)
    print(f"Grado: {desf2}\n")

    # Test3 (mamdani - BOA): 10, 40, 1 - ?
    print("--- Test Mamdani - BOA --- ")
    res3 = fsys.aggregation_method(test, method="mamdani", input_type="singleton")
    desf3 = fsys.BOA(res3)
    print(f"Grado: {desf3}\n")

    # Test4 (larsen - COA): 10, 40, 1 - ?
    print("--- Test Larsen - COA --- ")
    res4 = fsys.aggregation_method(test, method="larsen", input_type="singleton")
    desf4 = fsys.COA(res4)
    print(f"Grado: {desf4}\n")

    # Test5 (larsen - MOM): 10, 40, 1 - ?
    print("--- Test Larsen - MOM --- ")
    res5 = fsys.aggregation_method(test, method="larsen", input_type="singleton")
    desf5 = fsys.MOM(res5)
    print(f"Grado: {desf5}\n")

    # Test6 (larsen - BOA): 10, 40, 1 - ?
    print("--- Test Larsen - BOA --- ")
    res6 = fsys.aggregation_method(test, method="larsen", input_type="singleton")
    desf6 = fsys.BOA(res6)
    print(f"Grado: {desf6}\n")

if __name__ == "__main__":
    main()