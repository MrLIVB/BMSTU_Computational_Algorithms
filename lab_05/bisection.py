def bisection(a, b, eps, f):

    if abs(f(a)) < eps:
        return a
    if abs(f(b)) < eps:
        return b

    c = (a + b) / 2
    eps = abs(a - b) * 0.000001
    while abs(f(c)) >= eps:
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
        c = (a + b) / 2
    return c

def f(x):
    return x + 1


if __name__ == "__main__":
    print(bisection(-2, 2, 0.0001, f))