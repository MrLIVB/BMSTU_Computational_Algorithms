import matplotlib.pyplot as plt
import numpy as np
from math import sin

# 3 массива x, y, p

class Table:
    x = []
    y = []
    p = []


def find_matr(x: list, y: list, p: list, n: int):
    res = [[0 for j in range(n + 2)] for i in range(n + 1)]

    for i in range(n + 1):
        for j in range(n + 1):
            sa = 0
            for k in range(len(x)):
                sa += p[k] * pow(x[k], i + j)
            res[i][j] = sa
        sb = 0
        for k in range(len(x)):
            sb += p[k] * y[k] * pow(x[k], i)
        res[i][n + 1] = sb
    return res

def gauss_direct(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    for i in range(rows):
        if matrix[i][i] == 0:
            return None

        temp = matrix[i][i]
        for j in range(i, cols):
            matrix[i][j] /= temp
        for j in range(i + 1, rows):
            temp = matrix[j][i]
            for k in range(0, cols):
                matrix[j][k] -= temp * matrix[i][k]
    return matrix


def gauss_reverse(matrix):
    rows = len(matrix)
    cols = len(matrix[0]) - 1
    res = [0 for i in range(rows)]
    for i in range(rows - 1, -1, -1):
        temp = matrix[i][cols]
        for j in range(cols - 1, i, -1):
            temp -= res[j] * matrix[i][j]
        res[i] = temp
    return res


def gauss(matrix):
    tm = gauss_direct(matrix)
    res = gauss_reverse(tm)
    return res


table = None

def input_table():
    table = Table
    n = int(input("Введите колличество элементов: "))
    for i in range(n):
        print(f'Введите {i} элемент')
        x = float(input("x = "))
        y = float(input("y = "))
        p = float(input("p = "))
        table.x.append(x)
        table.y.append(y)
        table.p.append(p)
    return table


def change_weight():
    global table
    n = int(input("Введите номер элемента: "))
    p = float(input("Введите вес: "))
    table.p[n - 1] = p

def set_weights(table, weights):
    for i in range(len(weights)):
        table.p[i] = weights[i]
    return table

def approximate(table):
    plt.scatter(table.x, table.y, color='red')
    n_arr = [6, 10, 20]

    for n in n_arr:
        matr = find_matr(table.x, table.y, table.p, n)
        res = gauss(matr)
        sx = table.x[0]
        fx = table.x[len(table.x) - 1]
        plotted_x = []
        plotted_y = []
        while sx <= fx:
            plotted_x.append(sx)
            tmp = 0
            for i in range(n + 1):
                tmp += pow(sx, i) * res[i]
            plotted_y.append(tmp)
            sx += 0.05

        plt.plot(plotted_x, plotted_y, label=f'n = {n}')
        plt.legend()
    plt.show()


def menu():
    print('1 - Ввести таблицу')
    print('2 - Изменить вес')
    print('3 - Аппроксимировать')
    print('4 - Выйти')
    choice = int(input("Ваш выбор: "))

    global table
    if choice == 1:
        table = input_table()
    elif choice == 2:
        change_weight()
    elif choice == 3:
        approximate(table)
    elif choice == 4:
        return 1
    return 0


while not menu():
    pass

