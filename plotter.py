import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

xPositionCenter, yPositionCenter, zPositionCenter = 25., 25., 25.

dataDetON = '/Users/akanellako/Documents/B0mapping/24-10-21 50X50X50 1MM 2AVE DWELL 50 detectors on.csv'
dataDetOFF = '/Users/akanellako/Documents/B0mapping/24-10-21 50X50X50 1MM 2AVE DWELL 50.csv'

minValuesDetOffList = []
maxValuesDetOffList = []
minValuesDetOnList = []
maxValuesDetOnList = []

detOnDF = pd.read_csv(dataDetON, skiprows=1)
detOffDF = pd.read_csv(dataDetOFF, skiprows=1)

detOnDF['Xset'] = detOnDF['Xset'] - xPositionCenter
detOnDF['Yset'] = detOnDF['Yset'] - yPositionCenter
detOnDF['Zset'] = detOnDF['Zset'] - zPositionCenter

detOffDF['Xset'] = detOffDF['Xset'] - xPositionCenter
detOffDF['Yset'] = detOffDF['Yset'] - yPositionCenter
detOffDF['Zset'] = detOffDF['Zset'] - zPositionCenter

geometricalCenterField = detOffDF[(detOffDF['Xset'] == 0) & (detOffDF['Yset'] == 0) & (detOffDF['Zset'] == 0)]['Bm'].values[0]

detOffDF['Difference'] = detOffDF['Bm'] - geometricalCenterField
detOnDF['Difference'] = detOnDF['Bm'] - geometricalCenterField

filteredDetOffDF = detOffDF[(detOffDF['Xset'] == 0) & (detOffDF['Yset'] == 0)]
filteredDetOnDF = detOnDF[(detOnDF['Xset'] == 0) & (detOnDF['Yset'] == 0)]

zPositions = np.arange(detOffDF['Zset'].min(), detOffDF['Zset'].max()+1, 1)

for zPos in zPositions:
	aDetOffDF = detOffDF[(detOffDF['Zset'] == zPos)]
	aDetOnDF = detOnDF[(detOnDF['Zset'] == zPos)]

	minValuesDetOffList.append(aDetOffDF[aDetOffDF['Difference'].abs() < 1]['Difference'].min())
	maxValuesDetOffList.append(aDetOffDF[aDetOffDF['Difference'].abs() < 1]['Difference'].max())
	minValuesDetOnList.append(aDetOnDF[aDetOnDF['Difference'].abs() < 1]['Difference'].min())
	maxValuesDetOnList.append(aDetOnDF[aDetOnDF['Difference'].abs() < 1]['Difference'].max())

CMdetOffDF = detOffDF[(detOffDF['Zset'] == 0)]
CMdetOffDF = CMdetOffDF.pivot('Yset', 'Xset', 'Bm')

CMdetOnDF = detOnDF[(detOffDF['Zset'] == 0)]
CMdetOnDF = CMdetOnDF.pivot('Yset', 'Xset', 'Bm')

plt.figure(dpi = 200)
plt.errorbar(filteredDetOffDF.Zset.values, filteredDetOffDF.Difference.values, yerr=0., label = 'w/o detectors', fmt='.', zorder=5)
plt.errorbar(filteredDetOnDF.Zset.values, filteredDetOnDF.Difference.values, yerr=0., label = 'w/ detectors', fmt='.', zorder=5)
plt.axvline(x=0, color='k', linestyle='--', label='geometrical center')
plt.axhline(y=0, color='k', linewidth='0.75')
plt.legend(loc='upper right')
plt.xlabel('Motor set z-position [mm]')
plt.ylabel('Difference [mT]')
plt.savefig('graph1.png')

plt.figure(dpi = 200)
plt.errorbar(filteredDetOffDF.Zset.values, minValuesDetOffList, yerr=0., label = 'min w/o detectors', fmt='1', color='tab:blue', zorder=5)
plt.errorbar(filteredDetOffDF.Zset.values, maxValuesDetOffList, yerr=0., label = 'max w/o detectors', fmt='2', color='tab:blue', zorder=3)
plt.errorbar(filteredDetOffDF.Zset.values, minValuesDetOnList, yerr=0., label = 'min w/ detectors', fmt='1', color='tab:orange', zorder=5)
plt.errorbar(filteredDetOffDF.Zset.values, maxValuesDetOnList, yerr=0., label = 'max w/ detectors', fmt='2', color='tab:orange', zorder=3)
plt.axvline(x=0, color='k', linestyle='--', label='geometrical center')
plt.axhline(y=0, color='k', linewidth='0.75')
plt.legend(loc='upper right')
plt.xlabel('Motor set z-position [mm]')
plt.ylabel('Difference [mT]')
plt.savefig('graph2.png')

xTicks = np.arange(0, len(CMdetOffDF.columns), 5)
yTicks = np.arange(0, len(CMdetOffDF.index), 5)

plt.figure(dpi = 200)
plt.imshow(CMdetOffDF, aspect='auto', origin='lower', cmap='rainbow', vmin='48.88', vmax='48.95')
plt.xticks(ticks=xTicks, labels=[int(label) for label in CMdetOffDF.columns[xTicks]])
plt.yticks(ticks=yTicks, labels=[int(label) for label in CMdetOffDF.index[yTicks]])
plt.xlabel('Motor set $x$ position [mm]')
plt.ylabel('Motor set $y$ position [mm]')
plt.colorbar(label='Magnetic field $Β_0$ [mT]')
# plt.title('Field mapping at the middle of the magnet w/o detectors')
plt.savefig('graph3a.png')


plt.figure(dpi = 200)
plt.imshow(CMdetOnDF, aspect='auto', origin='lower', cmap='rainbow', vmin='48.88', vmax='48.95')
plt.xticks(ticks=xTicks, labels=[int(label) for label in CMdetOffDF.columns[xTicks]])
plt.yticks(ticks=yTicks, labels=[int(label) for label in CMdetOffDF.index[yTicks]])
plt.xlabel('Motor set $x$ position [mm]')
plt.ylabel('Motor set $y$ position [mm]')
plt.colorbar(label='Magnetic field $Β_0$ [mT]')
# plt.title('Field mapping at the middle of the magnet w/ detectors')
plt.savefig('graph3b.png')

# plt.show()
# sns.heatmap(CMdetOffDF, annot=False, cmap='rainbow')


