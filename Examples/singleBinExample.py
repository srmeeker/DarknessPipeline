'''
Author: Seth Meeker        Date: August 3, 2016

Simple example script for opening a single DARKNESS bin file using parsePacketDump2
then plotting data for a selected pixel
'''

import sys, os
import numpy as np

import matplotlib, time, struct
import matplotlib.pyplot as plt

from PyQt4 import QtCore
from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from functools import partial

from Utils import binTools
from Utils.arrayPopup import plotArray
from parsePacketDump2 import parsePacketData

# Choose the row and column of the desired pixel. Quickest way to determine this is to use darkQuickViewer.py
selPixelRow = 9 #yCoord from darkQuickViewer
selPixelCol = 35 #xCoord from darkQuickViewer

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = 'photonDump.bin'

pathTstamp = os.path.splitext(os.path.basename(path))[0]
with open(path,'rb') as dumpFile:
    data = dumpFile.read()

nBytes = len(data)
nWords = nBytes/8 #64 bit words
#break into 64 bit words
words = np.array(struct.unpack('>{:d}Q'.format(nWords), data),dtype=object)

parseDict = parsePacketData(words,verbose=True)

timestamps = parseDict['photonTimestamps']
phasesDeg = parseDict['phasesDeg']
basesDeg = parseDict['basesDeg']
pixelIds = parseDict['pixelIds']
image = parseDict['image']
xCoords = parseDict['xCoords']
yCoords = parseDict['yCoords']

selPixelId = pixelIds[np.where((xCoords==selPixelCol) & (yCoords==selPixelRow))][0]
print selPixelId


print 'selected pixel',selPixelId
print len(np.where(pixelIds==selPixelId)[0]),'photons for selected pixel'

print 'timestamps', timestamps[0:10]
print 'phase',phasesDeg[0:10]
print 'base',basesDeg[0:10]
print 'IDs',pixelIds[0:10]
np.where(pixelIds==selPixelId)
fig,ax = plt.subplots(1,1)
ax.plot(phasesDeg[np.where(pixelIds==selPixelId)])
ax.plot(basesDeg[np.where(pixelIds==selPixelId)])
ax.set_title('phases (deg)')
#ax.plot(pixelIds)

nbins = 70

phaseHist, bins = np.histogram(phasesDeg[np.where(pixelIds==selPixelId)], nbins)
fig,ax = plt.subplots(1,1)
ax.plot(bins[:-1], phaseHist)
ax.set_title('phase histogram')

baseHist, bins = np.histogram(basesDeg[np.where(pixelIds==selPixelId)], nbins)
fig,ax = plt.subplots(1,1)
ax.plot(bins[:-1], baseHist)
ax.set_title('base histogram')

subHist, bins = np.histogram(phasesDeg[np.where(pixelIds==selPixelId)]-basesDeg[np.where(pixelIds==selPixelId)], nbins)
fig,ax = plt.subplots(1,1)
ax.plot(bins[:-1], subHist)
ax.set_title('phase-base histogram')
    
plotArray(image,origin='upper')

#np.savez('/mnt/data0/test2/{}.npz'.format(pathTstamp),**parseDict)

plt.show()
