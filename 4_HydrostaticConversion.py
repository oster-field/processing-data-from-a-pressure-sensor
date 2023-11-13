"""Применение формулы гидростатического пересчета и разбиение на 20-минутные записи, построение графика смещений.
Нужно вручную ввести глубину погружения. График можно строить несколько раз, пересчет будет только при первом
запуске программы. Удаленные дни на оси абсцисс пересчитываются."""
import numpy as np
import matplotlib.pyplot as plt
import datetime
from functions import DateStart, DateEnd, seriesreducer
import pandas as pd
import sys
from tqdm import tqdm

Times = 10  # Насколько разредить запись, количество точек уменьшается в (2**Times)
h = 1 - 0.136  # Глубина погружения
dates = pd.date_range(DateStart, DateEnd).strftime('%d.%m').tolist()
deleteddates = []
for i in range(1, 3):
    for line in open('Data/log' + str(i) + '.txt').readlines():
        day = line.strip()[8::]
        month = line.strip()[5:7]
        deleteddates.append(day + '.' + month)
dates = [date for date in dates if date not in deleteddates]
Deltadate = datetime.timedelta(days=1)
DateStart += Deltadate * len(open('Data/log1.txt').readlines())  # Даты начала и конца записи волнения (без погружений)
DateEnd -= Deltadate * len(open('Data/log2.txt').readlines())
pbar = tqdm(total=len(dates), desc="Progress: ", colour='green')
y = np.arange(0)
ticks = np.arange(0)
c = 0
Fl = False
isconverted = open('Data/isconverted.txt').readlines()[0].strip()
while DateStart <= DateEnd:
    filename = DateStart.strftime('%Y.%m.%d')
    Error = False
    for i in range(1, sys.maxsize):
        try:
            arr = np.load('Data/' + filename + ' reading ' + str(i) + '.npy')
            if isconverted == 'Not converted':
                Fl = True
                arr = np.delete(arr, np.where(arr == 0))
                arr *= 10e3  # Из МПа в Па
                arr -= 101000  # Вычитается атмосферное давление
                arr -= 1026 * 9.8 * h  # Вычитается давление на глубине погружения
                arr /= 1026 * 9.8  # Смещение водной поверхности
                np.save('Data/' + filename + ' reading ' + str(i) + '.npy', arr)
            y = np.append(y, seriesreducer(arr, Times))
        except FileNotFoundError:
            Error = True
        if Error:
            break
    ticks = np.append(ticks, c+round((len(y)-c)/2))
    c = len(y)
    pbar.update(1)
    DateStart += Deltadate

if Fl:
    with open('Data/isconverted.txt', 'w') as file:
        file.write('Converted')
np.save('Data/ConvertedPlot', y)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.tick_params(labelsize=20)
ax.plot(np.arange(len(y)), y, linewidth=2, color='#046176', label='Water surface displacement')
ax.set_xlabel('Days', fontsize=20)
ax.set_ylabel('η(t), [m]', fontsize=20)
ax.set_xticks(ticks[::3])
ax.set_xticklabels(dates[::3], rotation=30)
ax.axhline(y=0, color='black', linewidth=1)
ax.grid(axis="y")
plt.legend(fontsize=16)
plt.show()
