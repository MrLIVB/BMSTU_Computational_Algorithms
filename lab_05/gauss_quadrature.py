import copy
import numpy as np
from math import sqrt, pi, e

from bisection import bisection

class LegendrePolynomial:
    def __init__(self, n):
        self.degree = n
        self.coef = [1]
        while n and len(self.coef) < n + 1:
            self.coef.append(0)

    def get(self, x):
        res = 0
        for i in range(self.degree + 1):
            res += self.coef[i] * x ** (self.degree - i)
        return res

    def __imul__(self, other):
        for i in range(len(self.coef)):
            self.coef[i] *= other
        return self

    def __isub__(self, other):
        i = other.degree
        j = self.degree
        while i != -1:
            self.coef[j] -= other.coef[i]
            i -= 1
            j -= 1
        return self

    def promote(self):
        self.degree += 1
        self.coef.append(0)
        return self

def form_legendre(n):
    if n == 0:
        return LegendrePolynomial(0)
    if n == 1:
        return LegendrePolynomial(1)

    zero = LegendrePolynomial(0)
    one = LegendrePolynomial(1)

    for i in range(1, n):
        m = i + 1
        buf_one = copy.deepcopy(one)

        one.promote()
        one *= ((2 * m - 1) / m)
        zero *= ((m - 1) / m)
        one -= zero

        zero = buf_one

    return one


def roots_legendre(n):
    roots = []
    roots_inter = []
    h = 2 / n
    a = -1
    b = a + h
    legendre = form_legendre(n)

    while len(roots_inter) != n:
        roots_inter = []

        while b <= 1:
            if legendre.get(a) * legendre.get(b) < 0:
                roots_inter.append([a, b])
            a = b
            b += h

        h /= 2
        a = -1
        b = a + h

    for i in roots_inter:
        roots.append(bisection(i[0], i[1], 0.000001, legendre.get))
    return roots


def quadrature(k):
    if k % 2:
        return 0
    else:
        return 2 / (k + 1)

def integrate(a, b, n, f, tau, m, h_y):
    t = roots_legendre(n)

    A = np.zeros((n, n))
    B = np.zeros((n, 1))

    for k in range(n):
        for i in range(n):
            A[k, i] = t[i] ** k
        B[k] = quadrature(k)

    D = np.linalg.inv(A)
    C = D * B

    Ai = np.array(C.ravel())
    res = 0
    for i in range(n):
        print(f((b + a) / 2 + (b - a) / 2 * t[i], tau, m, h_y))
        res += Ai[i] * f((b + a) / 2 + (b - a) / 2 * t[i], tau, m, h_y)
    res *= (b - a) / 2
    return res


def nparray_to_list(a):
    a = list(a)
    for i in range(len(a)):
        a[i] = list(a[i])
    return a
