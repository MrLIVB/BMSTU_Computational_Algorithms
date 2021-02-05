from legendre import legendre
import seidel
import matrix
import numpy as np
from math import sqrt, pi, e


def quadrature(k):
    if k % 2:
        return 0
    else:
        return 2 / (k + 1)

def integrate(a, b, n, f):
    l = legendre(n)

    A = np.zeros((n, n))
    B = np.zeros((n, 1))
    for k in range(n):
        row = []
        for i in range(n):
            A[k, i] = l[i] ** k
        B[k] = quadrature(k)

    """D = np.linalg.inv(A)
    D = np.matrix(D)
    C = D * B
    C = C.transpose()
    Ai = np.array(C.ravel())
    Ai = nparray_to_list(Ai)[0]"""
    D = matrix.inv(A)
    Ai = matrix.multi(D, B)

    return (b - a) / 2 * sum(Ai[i] * f((b-a)/2 * l[i] + (a + b) / 2) for i in range(n))



def nparray_to_list(a):
    a = list(a)
    for i in range(len(a)):
        a[i] = list(a[i])
    return a