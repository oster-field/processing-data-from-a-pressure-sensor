"""Построение графика колебаний давления по дням. Число точек, входящее в построение заметно сокращается.
Красным выделяются области, соответствующие погружению датчика."""
import numpy as np
import matplotlib.pyplot as plt
import datetime
import sys
import pandas as pd
from functions import seriesreducer, divedetector, DateStart, DateEnd

Times = 10  # Насколько разредить запись, количество точек уменьшается в (2**Times)
Deltadate = datetime.timedelta(days=1)
dates = pd.date_range(DateStart, DateEnd).strftime('%d.%m').tolist()

y = np.arange(0)
ticks = np.arange(0)
c = 0
while DateStart <= DateEnd:
    filename = DateStart.strftime('%Y.%m.%d')
    Error = False
    for i in range(1, sys.maxsize):
        try:
            arr = seriesreducer(np.load('Data/' + filename + ' reading ' + str(i) + '.npy'), Times)
            y = np.append(y, arr)
        except FileNotFoundError:
            Error = True
        if Error:
            break
    ticks = np.append(ticks, c+round((len(y)-c)/2))
    c = len(y)
    DateStart += Deltadate

fig = plt.figure()
ax = fig.add_subplot(111)
ax.tick_params(labelsize=20)
ax.plot(np.arange(len(y)), y, linewidth=2, color='#2D9B27', label='Pressure fluctuations')
ax.set_xlabel('Days', fontsize=20)
ax.set_ylabel('Pressure, [MPa]', fontsize=20)
ax.set_xticks(ticks[::3])
ax.set_xticklabels(dates[::3], rotation=30)
ax.axhline(y=0, color='black', linewidth=1)
ax.grid(axis="y")
xbegin, ybegin, xend, yend = divedetector(y)
ax.plot(xbegin, ybegin, linewidth=2.3, color='#BE2F33', label='Sensor immersion')
ax.plot(xend, yend, linewidth=2.3, color='#BE2F33')
plt.legend(fontsize=16)
plt.show()
