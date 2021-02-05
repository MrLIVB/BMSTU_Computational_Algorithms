class Table:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Fy:
    def __init__(self, x: [], y: []):
        self.arg = x
        self.val = y


def read(filename):
    file = open(filename, "r")

    y = []
    z = []
    x = list(map(float, file.readline()[1:].split()))

    while 1:
        line = file.readline()
        if line == '':
            break

        nums = line.split()
        y.append(float(nums[0]))
        z_line = []
        for i in range(1, len(nums)):
            z_line.append(float(nums[i]))
        z.append(z_line)

    file.close()
    return x, y, z


def get_borders(args, val, power):
    pos = -1
    for i in range(1, len(args)):
        if args[i] > args[i - 1]:
            if args[i] >= val > args[i - 1]:
                pos = i
                break
        if args[i] < args[i - 1]:
            if args[i] <= val < args[i - 1]:
                pos = i
                break

    if pos == -1:
        return None, None

    left_border = pos - (power // 2) - 1
    right_border = pos + (power // 2 + power % 2)

    if left_border < 0:
        left_border = 0
        right_border = power + 1
    elif right_border > len(args):
        left_border = len(args) - power
        right_border = len(args)

    return left_border, right_border


def chose_configuration(xy: Fy, val, power, shift):
    left_border, right_border = get_borders(xy.arg, val, power)

    if left_border is None:
        return None, None

    work_array_x = []
    poly_coefs = [[0 for j in range(power - i + 1)] for i in range(power + 1)]

    for i in range(left_border, right_border):
        work_array_x.append(xy.arg[i])
        poly_coefs[0][i - left_border] = xy.val[i - shift]

    return work_array_x, poly_coefs


def get_poly_coefs(args, poly_coefs, power):
    for i in range(1, power + 1):
        for j in range(power - i + 1):
            poly_coefs[i][j] = (poly_coefs[i - 1][j + 1] - poly_coefs[i - 1][j]) / (args[j + i] - args[j])
    return poly_coefs


def calculate_val(args, poly_coefs, arg, power):
    res = poly_coefs[0][0]
    mult = 1
    for i in range(power):
        mult *= (arg - args[i])
        res += mult * poly_coefs[i + 1][0]

    return res


def interpolate(xy: Fy, arg, power, shift):
    work_array_x, poly_coefs = chose_configuration(xy, arg, power, shift)
    if work_array_x is None:
        return None

    poly_coefs = get_poly_coefs(xy.arg, poly_coefs, power)

    return calculate_val(xy.arg, poly_coefs, arg, power)


def interpolate_3d(wt: Table, x, y, nx, ny):
    left_border, right_border = get_borders(wt.y, y, ny)
    if left_border is None:
        return
    temp_res = []
    for i in range(left_border, right_border):
        tr = interpolate(Fy(wt.x, wt.z[i]), x, nx, 0)
        if tr is None:
            return
        temp_res.append(tr)
    return interpolate(Fy(wt.y, temp_res), y, ny, left_border)


def f(x, y):
    return x * x + y * y


def form_new_table_f():
    name = input("Введите имя файла, в который будет сохранена таблица: ")
    file = open(name, "w")
    arg_min = float(input("Введите минимальное значение аргумента: "))
    arg_max = float(input("Введите максимальное значение аргумента: "))
    step = float(input("Введите шаг: "))

    file.write('x')
    i = arg_min
    while i < arg_max:
        file.write(" %.3f" % i)
        i += step
    file.write('\n')

    i = arg_min
    while i < arg_max:
        file.write("%.3f" % i)
        j = arg_min
        while j < arg_max:
            file.write(' %.3f' % f(i, j))
            j += step
        file.write("\n")
        i += step

    file.close()


cur_table = Table(None, None, None)
file_name = 'two_sqr'

while 1:
    print("\n\nМеню: ")
    print("1. Интерполяция")
    print("2. Выбрать файл")
    print("3. Сформировать файл по заданной функции")
    print("4. Выход")
    ch = int(input("\nВаш выбор: "))

    if ch < 0 or ch > 5:
        pass
    elif ch == 1:
        if len(file_name) == 0:
            print("Файл не выбран")
            continue
        if cur_table.x is None or len(cur_table.x) == 0:
            table = read(file_name)
        x = float(input("Введите X для интерполяции: "))
        y = float(input("Введите Y для интерполяции: "))
        nx = int(input("Введите степень полинома по Х: "))
        ny = int(input("Введите степень полинома по Y: "))
        res = interpolate_3d(cur_table, x, y, nx, ny)
        if res is None:
            print("Экстраполяция запрещена")
            continue
        print("Результат интерполяции: %.3f" % res)
    elif ch == 2:
        file_name = input("Введите название файла: ")
        x, y, z = read(file_name)
        cur_table = Table(x, y, z)
    elif ch == 3:
        form_new_table_f()
    elif ch == 4:
        break
