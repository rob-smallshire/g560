from numpy import arange
from scipy.stats import rv_discrete


def zipf(n, a):
    x = arange(1, n+1)
    weights = x ** (-a)
    weights /= weights.sum()
    return rv_discrete(name='bounded_zipf', values=(x - 1, weights))
