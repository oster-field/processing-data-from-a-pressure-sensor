"""1) Функция удаляет каждую n-ю точку "times" раз, она нужна для построения
графиков в больших масштабах (дни, месяцы) для ускорения работы
2)Функция среднего значения между соседними точками
3)Маркировка точек ряда, соответствующих погружению датчика
4)Поиск записей, содержащих момент погружения
5)Получение номера записи."""
import numpy as np
import matplotlib.pyplot as plt
import sys
import datetime

DateStart = datetime.datetime.strptime((open('DataTXT/INFO.dat').readlines()[5].strip()),
                                       '%Y.%m.%d %H:%M:%S.%f').date()
DateEnd = datetime.datetime.strptime((open('DataTXT/INFO.dat').readlines()[7].strip()),
                                     '%Y.%m.%d %H:%M:%S.%f').date()


def seriesreducer(arr, times, n=2):
    for i in range(0, times):
        arr = arr[::n]
    return arr


def meanvalueplot(series):
    if len(series) % 2 != 0:
        series = np.delete(series, 0)
    a = series[::2]
    b = series[1::2]
    mean = a / b
    xmean = 2 * np.arange(0, len(mean))
    return xmean, mean


def divedetector(series):
    x, seriessplit = meanvalueplot(series)
    a, b = np.split(seriessplit, 2)
    a = np.flip(a)
    for i in a:
        if 0.5 < i < 1.5:
            a = np.delete(a, [0])
        else:
            break
    for i in b:
        if 0.5 < i < 1.5:
            b = np.delete(b, [0])
        else:
            break
    xbegin = np.arange(0, len(series[0:2 * len(a)]))
    ybegin = series[0:2 * len(a)]
    xend = np.arange(len(series) - len(series[0:2 * len(b)]), len(series))
    yend = np.flip(np.flip(series)[0:2 * len(b)])
    return xbegin, ybegin, xend, yend


def lowmean():
    ds = datetime.datetime.strptime((open('DataTXT/INFO.dat').readlines()[5].strip()),
                                    '%Y.%m.%d %H:%M:%S.%f').date()
    de = datetime.datetime.strptime((open('DataTXT/INFO.dat').readlines()[7].strip()),
                                    '%Y.%m.%d %H:%M:%S.%f').date()
    dt = datetime.timedelta(days=1)
    mean = np.arange(0)
    readings = []
    while ds <= de:
        filename = ds.strftime('%Y.%m.%d')
        Error = False
        for i in range(1, sys.maxsize):
            try:
                arr = seriesreducer(np.load('Data/' + filename + ' reading ' + str(i) + '.npy'), 5)
                mean = np.append(mean, np.mean(arr))
                readings.append('Data/' + filename + ' reading ' + str(i) + '.npy')
            except FileNotFoundError:
                Error = True
            if Error:
                break
        ds += dt
    res = []
    for i in range(len(readings)-1):
        if mean[i] < np.sum(mean) / len(readings) < mean[i + 1] or mean[i+1] < np.sum(mean) / len(readings) < mean[i]:
            res.append(readings[i])
            res.append(readings[i+1])
    return res


def extractlastnumber(string):
    last_space_index = string.rfind(" ")
    if last_space_index != -1:
        substring = string[last_space_index + 1:]
        numbers = "".join([c for c in substring if c.isdigit()])
        if numbers:
            return int(numbers)
    return None

