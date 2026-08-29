from math import sqrt

def get_norm(values):
    if not values:
        return 0.0
    return round(sqrt(sum(x * x for x in values)), 3)
