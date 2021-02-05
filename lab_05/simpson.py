def simpson(a, b, n, f):
    res = 0
    h = (b - a) / n

    x = a
    for i in range(n // 2):
        res += f(x) + 4*f(x + h) + f(x + 2*h)
        x += 2 * h

    return h / 3 * res

def f(x):
    return 4 * x**3
