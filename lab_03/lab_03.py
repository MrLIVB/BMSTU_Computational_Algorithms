def coeff(x, f):
    n = len(x)
    k = [0 for i in range(n + 1)]
    c = [0 for i in range(n + 1)]
    k[0] = 0
    c[0] = 0
    for i in range(1, n):
        j = i - 1
        m = j - 1
        a = x[i] - x[j]
        b = x[j] - x[m]
        r = 2 * (a + b) - b * c[j]
        c[i] = a / r
        k[i] = 3 * (((f[i] - f[j]) / a - (f[j] - f[m]) / b) - b * k[j]) / r
    c[n] = k[n]
    for i in range(n - 1, 1, -1):
        c[i] = k[i] - c[i] * c[i + 1]

    return c


def spl(x, f, c, x1):
    n = len(x)
    i = 0
    while x1 > x[i] and i < n:
        i += 1
    j = i - 1
    q = x[i] - x[j]
    r = x1 - x[j]
    b = (f[i] - f[i - 1]) / q - (c[i + 1] + 2 * c[i]) * q / 3
    d = (c[i + 1] - c[i]) / q * r

    p1 = b + r * (2 * c[i] + d)
    p2 = 2 * (c[i] + d)
    p = f[i - 1] + r * (b + r * (c[i] + d / 3))

    return p


def solve_tri_diag(matr, f, n):
    alpha = [0 for i in range(n - 1)]
    beta = [0 for i in range(n - 1)]
    b = [0 for i in range(n)]

    alpha[0] = - matr[2][0] / matr[1][0]
    beta[0] = f[0] / matr[1][0]

    for i in range(1, n - 1):
        alpha[i] = -matr[2][i] / matr[1][i] + matr[0][i] * alpha[i - 1]
        beta[i] = (f[i] - matr[0][i] * beta[i - 1]) / matr[1][i] + matr[0][i] * alpha[i - 1]

    b[n - 1] = (f[n - 1] - matr[0][n - 1] * beta[n - 2]) / \
                    (matr[1][n - 1] + matr[0][n - 1] + matr[0][n - 1] * alpha[n - 2])

    for i in range(n - 2, -1, -1):
        b[i] = b[i + 1] * alpha[i] + beta[i]

    return b

def build_spline(x, y, n):
    a = [0 for i in range(n - 1)]
    c  = [0 for i in range(n - 1)]
    d = [0 for i in range(n - 1)]
    delta = [0 for i in range(n - 1)]
    h = [0 for i in range(n - 1)]
    matr = [[0 for j in range(n)] for i in range(3)]

    f = [0 for i in range(n)]
    if n < 3:
        return -1

    x3 = x[2] - x[0]
    xn = x[n - 1] - x[n - 3]

    for i in range(n - 1):
        a[i] = y[i]
        h[i] = x[i + 1] - x[i]
        delta[i] = (y[i + 1] - y[i]) / h[i]
        matr[0][i] = h[i] if i else x3
        f[i] = 3 * (h[i] * delta[i - 1] + h[i - 1] * delta[i]) if i else 0

    matr[1][0] = h[0]
    matr[2][0] = h[0]

    for i in range(1, n - 1):
        matr[1][i] = 2 * (h[i] + h[i - 1])
        matr[2][i] = h[i]

    matr[1][n - 1] = h[n - 2]
    matr[2][n - 1] = xn
    matr[0][n - 1] = h[n - 2]

    f[0] = ((h[0] + 2 * x3) * h[1] * delta[0] + pow(h[0], 2) * delta[1]) / x3
    f[n - 1] = (pow(h[n - 2], 2) * delta[n - 3] + (2 * xn + h[n - 2]) * h[n - 3] * delta[n - 2]) / xn

    b = solve_tri_diag(matr, f, n)

    coef = [[0 for i in range(n - 1)] for j in range(4)]

    for j in range(n - 1):
        d[j] = (b[j + 1] + b[j] - 2 * delta[j]) / (h[j] * h[j])
        c[j] = 2 * (delta[j] - b[j]) / h[j] - (b[j + 1]) / h[j]

        coef[0][j] = a[j]
        coef[1][j] = b[j]
        coef[2][j] = c[j]
        coef[3][j] = d[j]

    return coef


def interpolate_spline(x, y, val):
    coef = build_spline(x, y, len(x))

    i = 0
    while x[i] < val:
        i += 1
    i -= 1

    return coef[0][i] + coef[1][i] * (val - x[i]) + coef[2][i] * pow(val - x[i], 2) + coef[3][i] * pow(val - x[i], 3)


def chose_configuration(table, x, n):
    xpos = -1
    for i in range(1, len(table[0])):  # поиск позиции x
        if table[0][i] > table[0][i - 1]:
            if table[0][i] >= x > table[0][i - 1]:
                xpos = i
                break
        if table[0][i] < table[0][i - 1]:
            if table[0][i] <= x < table[0][i - 1]:
                xpos = i
                break

    if xpos == -1:  # x вне таблицы
        return None, None

    left_border = xpos - (n // 2) - 1
    right_border = xpos + (n // 2 + n % 2)

    if left_border < 0:
        left_border = 0
        right_border = n + 1
    elif right_border > len(table[1]):
        left_border = len(table[1]) - n
        right_border = len(table[1])

    work_array_x = []

    poly_coefs = [[0 for j in range(n - i + 1)] for i in range(n + 1)]

    for i in range(left_border, right_border):
        work_array_x.append(table[0][i])
        poly_coefs[0][i - left_border] = table[1][i]

    return work_array_x, poly_coefs


def calculate_polynomial(work_array_x, poly_coefs, x, n):
    # готовим массивы для коеффициентов полинома, начиная с y из таблицы
    for i in range(1, n + 1):
        for j in range(n - i + 1):
            poly_coefs[i][j] = (poly_coefs[i - 1][j + 1] - poly_coefs[i - 1][j]) / (work_array_x[j + i] - work_array_x[j])

    res = poly_coefs[0][0]
    mult = 1
    for i in range(n):
        mult *= (x - work_array_x[i])
        res += mult * poly_coefs[i + 1][0]

    return res


def interpolate(table, x, n):
    work_array_x, poly_coefs = chose_configuration(table, x, n)
    if work_array_x is None:
        return None

    return calculate_polynomial(work_array_x, poly_coefs, x, n)


xarr = []
farr = []

i = 0
while i <= 5:
    xarr.append(round(i, 2))
    # farr.append(round(pow(round(i, 2), 3), 3))
    farr.append(round(pow(round(i, 2), 3), 3))
    i += 0.3

print(xarr)
print(farr)
carr = coeff(xarr, farr)
print('Кубический сплайн: %.3f' % spl(xarr, farr, carr, 2.4))
print('Кубический сплайн: %.3f' % interpolate_spline(xarr, farr, 2.4))
print('Полином Ньютона 3-ей степени: %.3f' % interpolate([xarr, farr], 2.4, 3))
