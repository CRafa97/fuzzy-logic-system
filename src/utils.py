def join(bounds):
    return min (b[0] for b in bounds), max(b[1] for b in bounds)

def simpson(f, a, b, prec=3):
    area = ((b - a) / 6) * (f(a) + 4*f((a + b)/2) + f(b))
    return round(area, prec)