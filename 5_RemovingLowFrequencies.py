"""Удаление высокочастотных компонент для стабильного нулевого уровня. Построение графика до/после удаления.
Т.к. преобразование фурье является интегралом, его можно разбить на отдельные
 фрагменты интегрирования, поэтому для ускорения ФТ берется для каждого фрагмента."""
import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy.fftpack import fft, ifft, fftfreq
from functions import DateStart, DateEnd, seriesreducer
import pandas as pd
import sys
from tqdm import tqdm

Sensor_Frequency = 8
Times = 10  # Насколько разредить запись, количество точек уменьшается в (2**Times)
TMax = 20  # Минимальная длительность волн, которые останутся после преобразования (в минутах)
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
istransformed = open('Data/istransformed.txt').readlines()[0].strip()

while DateStart <= DateEnd:
    filename = DateStart.strftime('%Y.%m.%d')
    Error = False
    for i in range(1, sys.maxsize):
        try:
            arr = np.load('Data/' + filename + ' reading ' + str(i) + '.npy')
            if istransformed == 'Not transformed' and len(arr) != 0:
                Fl = True
                s = fft(arr)
                x = fftfreq(len(arr), (1 / 8) / (2 * np.pi))
                for freq in range(len(x)):
                    if abs(x[freq]) < np.pi / (TMax * 30):  # Удаление гармоник длительностью > TMax минут
                        s[freq] = 0 + 0j
                arr = ifft(s).real
                np.save('Data/' + filename + ' reading ' + str(i) + '.npy', arr)
            y = np.append(y, seriesreducer(arr, Times))
        except FileNotFoundError:
            Error = True
        if Error:
            break
    ticks = np.append(ticks, c + round((len(y) - c) / 2))
    c = len(y)
    pbar.update(1)
    DateStart += Deltadate

if Fl:
    with open('Data/istransformed.txt', 'w') as file:
        file.write('Transformed')

fig = plt.figure()
ax = fig.add_subplot(111)
ax.tick_params(labelsize=20)
ax.plot(np.arange(len(np.load('Data/ConvertedPlot.npy'))),
        np.load('Data/ConvertedPlot.npy'), linewidth=2, color='#760461', label='Before Fourier transform', alpha=.4)
ax.plot(np.arange(len(y)), y, linewidth=2, color='#046176', label='After Fourier transform')
ax.set_xlabel('Days', fontsize=20)
ax.set_ylabel('η(t), [m]', fontsize=20)
ax.set_xticks(ticks[::3])
ax.set_xticklabels(dates[::3], rotation=30)
ax.axhline(y=0, color='black', linewidth=1)
ax.grid(axis="y")
plt.legend(fontsize=16)
plt.show()
