x_table = [    1,     2,     3,    4,      5,     6]
y_table = [0.571, 0.889, 1.091, 1.231, 1.333, 1.412]

def left_side_diff(y, h):
    return [None if i == 0
            else (y[i] - y[i - 1]) / h for i in range(len(y))]

def right_side_diff(y, h):
    return [None if i == (len(y) - 1)
            else (y[i + 1] - y[i]) / h for i in range(len(y))]

def center_diff(y, h):
    return [None if i == (len(y) - 1) or i == 0
            else (y[i + 1] - y[i - 1]) / (h * 2) for i in range(len(y))]


def runge_left(y, h):
    n = len(y)
    p = 1

    yh = left_side_diff(y, h)
    y2h = [0 if i < 2 else (y[i] - y[i - 2]) / (2*h) for i in range(n)]

    return [None if i < 2 else (yh[i] + (yh[i] - y2h[i]) / (2**p - 1)) for i in range(n)]

def eta(y):
    return 1 / y

def ksi(x):
    return 1 / x

def align(x, y):
    n = len(x)
    eta_a = [eta(x[i]) for i in range(n)]
    ksi_a = [ksi(y[i]) for i in range(n)]

    return [None if i == len(x) - 1
            else ((eta_a[i + 1] - eta_a[i]) / (ksi_a[i + 1] - ksi_a[i])) * y[i] / x[i]
            for i in range(len(x))]

def second_diff(y, h):
    return [None if i == (len(y) - 1) or i == 0
            else (y[i - 1] - 2 * y[i] + y[i + 1]) / h**2
            for i in range(len(y))]

# ─│┌┐└┘├┤┬┴┼

def output_table(x, y, diffs):
    print("┌───┬─────────┬────────┬────────┬────────┬────────┬────────┐")
    print("│ x │    y    │", end='')
    for i in range(len(diffs)):
        print("    %d   │" % (i + 1), end='')

    for r in range(len(x)):
        print("\n├───┼─────────┼────────┼────────┼────────┼────────┼────────┤")
        print("│ %d │  %.3f  │" % (x[r], y[r]), end='')
        for d in range(len(diffs)):
            if diffs[d][r] is not None:
                print(" %-6.3f │" % diffs[d][r], end='')
            else:
                print("  None  │", end='')
    print("\n└───┴─────────┴────────┴────────┴────────┴────────┴────────┘")


lsd = left_side_diff(y_table, 1)
rsd = right_side_diff(y_table, 1)
cnt = center_diff(y_table, 1)
run = runge_left(y_table, 1)
ali = align(x_table, y_table)
sec = second_diff(y_table, 1)

output_table(x_table, y_table, [lsd, cnt, run, ali, sec])