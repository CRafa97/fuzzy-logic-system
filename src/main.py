from fuzzynumbers import *
from fuzzysys import FuzzyInferenceSystem

# Fuzzification

# Linguistic: Distance
far = SigmoidalFuzzyNumber(20, 30)
normal = GaussianFuzzyNumber(k=0.05, m=15, domain=(0, 30))
near = FuzzyNegation(SigmoidalFuzzyNumber(0, 10))

# Linguistic: Object Speed
move = SigmoidalFuzzyNumber(10, 20)
move_slow = FuzzyFairly(move)
move_fast = FuzzyVery(move)
keep = TrapezoidalFuzzyNumber(-1, 0, 10, 20)

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
    (far, slow, keep, nothing), #1
    (normal, slow, keep, small), #2
    (normal, constant, keep, medium), #3
    (near, constant, keep, big), #4
    (near, fast, keep, complete), #5

    (near, fast, move_slow, big), #6
    (normal, constant, move_slow, medium), #7
    (far, constant, move_slow, small), #8
    (near, constant, move_fast, small), #9
    (normal, slow, move_fast, nothing), #10
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

    # More Tests

    ntest1 = (30, 15, 15,) # no pisar nada el freno
    print("--- Using Mamdani - COA --- ")
    nres1 = fsys.aggregation_method(ntest1, method="mamdani", input_type="singleton")
    ndesf1 = fsys.COA(nres1)
    print(f"Grado: {ndesf1}\n")

    ntest2 = (6, 64, 7,)
    print("--- Using Larsen - MOM --- ") # pisar bastante el freno
    nres2 = fsys.aggregation_method(ntest2, method="larsen", input_type="singleton")
    ndesf2 = fsys.MOM(nres2)
    print(f"Grado: {ndesf2}\n")

    ntest3 = (12, 67, 10,)
    print("--- Using Mamdani - BOA --- ") # pisar mas o menos el freno
    nres3 = fsys.aggregation_method(ntest3, method="larsen", input_type="singleton")
    ndesf3 = fsys.BOA(nres3)
    print(f"Grado: {ndesf3}\n")

    # FuzzySet Input
    print("  Fuzzy Sets as Input  ")

    dist = TriangularFuzzyNumber(5, 11, 18)
    speedx = FuzzySet(lambda x: x == 65, domain=(0,90))
    obj_speed = TrapezoidalFuzzyNumber(-1, 0, 5, 15)

    inputx = (dist, speedx, obj_speed)
    print("--- Using Mamdani - COA --- ")
    ans = fsys.aggregation_method(inputx, method="mamdani", input_type="fuzzy")
    des = fsys.COA(ans)
    print(f"Grado: {des}\n")

if __name__ == "__main__":
    main()