def read(filename):
    file = open(filename, "r")

    x = []
    y = []

    while 1:
        line = file.readline()
        if line == '':
            break

        nums = line.split()
        x.append(float(nums[0]))
        y.append(float(nums[1]))

    file.close()
    return x, y


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


def find_root_interpolate(table, n):
    t_x = [table[1][i] for i in range(len(table[0]))]
    t_y = [table[0][i] for i in range(len(table[0]))]
    work_array_x, poly_coefs = chose_configuration([t_x, t_y], 0, n)

    if work_array_x is None:
        for i in range(len(table[0])):
            table[0][i] = table[1][i]
            table[1][i] = t[i]
        return None

    res = calculate_polynomial(work_array_x, poly_coefs, 0, 4)
    return res


def bisection(table):
    r_x = -1
    r_b_n = -1
    for i in range(len(table[0]) - 1):
        for j in range(i + 1, len(table[0])):
            if table[1][i] * table[1][j] < 0:
                r_b_n = j
                break
        if table[1][r_b_n] * table[1][i] < 0:
            r_x = table[0][r_b_n]
            break

    if r_b_n == -1:
        return None
    l_x = table[0][r_b_n - 1]
    c = (r_x + l_x) / 2
    n = 6
    work_array_x, poly_coefs = chose_configuration(table, 0, n)
    t = calculate_polynomial(work_array_x, poly_coefs, c, n)
    t1 = calculate_polynomial(work_array_x, poly_coefs, r_x, n)
    t2 = calculate_polynomial(work_array_x, poly_coefs, l_x, n)

    if t1 == 0:
        return r_x
    if t2 == 0:
        return l_x

    prev_c = c
    rep = 0
    eps = abs(t1 - t2) * 0.000001
    while abs(t) >= eps:
        if abs(t1) < eps:
            return r_x
        if abs(t2) < eps:
            return l_x
        if t1 * t < 0:
            l_x = c
        elif t2 * t < 0:
            r_x = c

        c = (r_x + l_x) / 2

        t = calculate_polynomial(work_array_x, poly_coefs, c, n)
        t1 = calculate_polynomial(work_array_x, poly_coefs, r_x, n)
        t2 = calculate_polynomial(work_array_x, poly_coefs, l_x, n)

        if c == prev_c:
            rep += 1
        else:
            prev_c = c
            rep = 0

        if rep >= 20:
            return None

    return c


def form_new_table():
    name = input("Введите имя файла, в который будет сохранена таблица: ")
    file = open(name, "w")
    n = int(input("Введите количество значений: "))
    print("Введите построчно таблицу в формате x y:")
    for i in range(n):
        file.write(input())
    file.close()


def f(x):
    return x * x


def form_new_table_f():
    name = input("Введите имя файла, в который будет сохранена таблица: ")
    file = open(name, "w")
    i = float(input("Введите минимальный x: "))
    x_max = float(input("Введите максимальный x: "))
    step = float(input("Введите шаг: "))

    while i < x_max:
        file.write('%.3f' % (i) + ' ' + '%.3f'%(f(i)) + '\n')
        i += step

    file.close()


file = ''
table = []

while 1:
    print("\n\nМеню: ")
    print("1. Интерполяция")
    print("2. Найти корень, используя метод половинного деления")
    print("3. Найти корень, используя обратную интерполяцию")
    print("4. Выбрать файл")
    print("5. Сформировать новый файл вручную")
    print("6. Сформировать файл по заданной функции")
    print("7. Выход")
    ch = int(input("\nВаш выбор: "))

    if ch < 0 or ch > 7:
        pass
    elif ch == 1:
        if len(file) == 0:
            print("Файл не выбран")
            continue
        if len(table) == 0:
            table = read(file)
        x = float(input("Введите X для интерполяции: "))
        n = int(input("Введите степень полинома: "))
        res = interpolate(table, x, n)
        if res is None:
            print("Экстраполяция запрещена")
            continue
        print("Результат интерполяции: %.3f" % res)
    elif ch == 2:
        if file is '':
            print("Файл не выбран")
            continue
        if len(table) == 0:
            table = read(file)
        res = bisection(table)
        if res is None:
            print("Корней нет, либо их не удалось найти")
            continue
        print("Корень: %.3f" % res)
    elif ch == 3:
        if file is '':
            print("Файл не выбран")
            continue
        if len(table) == 0:
            table = read(file)
        n = int(input("Введите степень полинома: "))
        res = find_root_interpolate(table, n)
        if res is None:
            print("Корней нет, либо их не удалось найти")
            continue
        print("Корень: %.3f" % res)
    elif ch == 4:
        file = input("Введите название файла: ")
        table = read(file)
    elif ch == 5:
        form_new_table()
    elif ch == 6:
        form_new_table_f()
    elif ch == 7:
        break
