def agg():
    freq = {'a': 3, 'b': 5, 'c': 4}
    total = sum(freq.values())
    return float(total) / len(freq)
print('AVG: %.1f' % agg())
