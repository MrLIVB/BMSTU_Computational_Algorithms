from math import exp, sin, cos, pi, fabs
from gauss_quadrature import roots_legendre
import matplotlib.pyplot as plt


def f(fi, teta, tau):
    lr = (2 * cos(teta) / (1 - sin(teta) ** 2 - cos(fi) ** 2))
    return (1 - exp(-tau * lr)) * cos(teta) * sin(teta)

def F(fi, tau, m, h_y):
    res = 0
    for i in range(int(m / 2 - 1)):
        res += f(fi, 2*i*h_y, tau) + 4 * f(fi, (2*i + 1) * h_y, tau) + f(fi, (2*i+2)*h_y, tau)
    return h_y / 3 * res


def matrix_normalize_rows(matrix, x_vars, cur):
    i = cur
    while i < x_vars:
        normalize = max(matrix[i])
        if fabs(normalize) < 1e-6:
            i+= 1
            continue
        j = cur
        while j < x_vars + 1:
            matrix[i][j] /= normalize
            j += 1
        i += 1

    i = cur + 1
    while i < x_vars + 1:
        if matrix[i][cur] < 1e-6:
            i += 1
            continue
        j = cur
        while j < x_vars + 1:
            matrix[i][j] -= matrix[cur][j]
            j += 1
        i += 1

def matrix_solve(matrix, x_vars):
    x = [0 for i in range(x_vars)]
    i = x_vars - 1
    while i >= x_vars - 1:
        sigma = 0
        j = x_vars - 1
        while j > i:
            sigma += matrix[i][j] * x[j]
            j -= 1
        if fabs(matrix[i][j]) <= 1e-6:
            x[i] = 0
        else:
            x[i] = (matrix[i][x_vars] - sigma) / matrix[i][i]
        i -= 1

    return x


tau = 0.5
n = int(input("Введите n: "))
m = int(input("Введите m: "))
b = pi/2
a = 0
h_y = (b - a) / n
t = []
y = []

roots = roots_legendre(n)
matrix = [[pow(roots[j], i) for j in range(n)] for i in range(n)]

for i in range(n):
    matrix[i].append((1 - pow(-1, i + 1)) / (i + 1))

for i in range(n):
    matrix_normalize_rows(matrix, n, i)

A = matrix_solve(matrix, n)

while tau <= 10:
    t.append(tau)
    res = 0
    for i in range(n):
        res += A[i] * F((b + a) / 2 + (b - a) / 2 * roots[i], tau, m, h_y)
    res *= (b - a) / 2
    res *= 4 / pi
    y.append(res)
    tau += 0.05

plt.plot(t, y)
plt.show()
