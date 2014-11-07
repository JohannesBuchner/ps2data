"""
Extract data from postscript plots

What does it do?
	Writes out data file with points of plot.
	Recreates the plot

Caveats: 
	not generally applicable, YMMV. Postscript is a programming language,
	not everything can be supported.
	works on at least some IDL ps2eps plots,
	specifically fig7b.eps fig8b.eps from http://arxiv.org/format/1206.2642v1

Uses 'C' (color) lines to identify data sets and their color.
Uses   'a b l x y M' lines to identify data points
Uses   'a b l x y M' lines to identify plot area (surrounding rectangle)

(C) Johannes Buchner, 2014

"""

import matplotlib.pyplot as plt
import sys
from math import log10
import json

if len(sys.argv) != 7:
	print 'SYNAPSIS: %s <filename.ps> xmin xmax [linear|log] ymin ymax [linear|log]' % sys.argv[0]
	print
	print 'filename.ps: EPS or PS file'
	print 'xmin, xmax: lower and upper value of plot range on x-axis'
	print 'ymin, ymax: lower and upper value of plot range on y-axis'
	print
	print 'Johannes Buchner (C) 2014'
	sys.exit(1)
filename = sys.argv[1]
f = open(filename)
lines = f.readlines()

realxmin, realxmax, xscale, realymin, realymax, yscale = sys.argv[2:]
realxmin, realxmax, realymin, realymax = float(realxmin), float(realxmax), float(realymin), float(realymax)

drawrect = [None, None, None, None]

def convertpoints(x, y):
	xlo, ylo, xhi, yhi = drawrect
	xx = (x - xlo) * 1. / (xhi - xlo)
	yy = (y - ylo) * 1. / (yhi - ylo)
	
	if xscale == 'log':
		xxx = 10**(xx * (log10(realxmax) - log10(realxmin)) + log10(realxmin))
	else:
		xxx = xx * (realxmax - realxmin) + realxmin
	if yscale == 'log':
		yyy = 10**(yy * (log10(realymax) - log10(realymin)) + log10(realymin))
	else:
		yyy = yy * (realymax - realymin) + realymin
	return xxx, yyy

currentcolor = None
datasets = []
currentdataset = []

for l in lines:
	parts = l.rstrip().split()
	args = tuple(parts[:-1])
	cmd = parts[-1]
	if cmd in commands:
		cmd = commands[cmd]
	if cmd == 'C':
		newcurrentcolor = int(args[0]) / 255., int(args[1]) / 255., int(args[2]) / 255.
		if currentcolor != newcurrentcolor:
			print 'new color:', newcurrentcolor
			if currentdataset: datasets.append(dict(color=currentcolor, data=currentdataset))
			currentdataset = []
			pass
		currentcolor = int(args[0]) / 255., int(args[1]) / 255., int(args[2]) / 255.
	if len(args) == 5 and cmd[0] == 'l' and args[2] == 'M':
		xstart = int(args[0])
		ystart = int(args[1])
		xlen = int(args[3])
		ylen = int(args[4])
		if xlen >= 0 and ylen >= 0:
			if drawrect[0] is None or drawrect[0] > xstart:
				drawrect[0] = xstart
			if drawrect[1] is None or drawrect[1] > ystart:
				drawrect[1] = ystart
			if drawrect[2] is None or drawrect[2] < xstart + xlen:
				drawrect[2] = xstart + xlen
			if drawrect[3] is None or drawrect[3] < ystart + ylen:
				drawrect[3] = xstart + xlen
	#if cmd == 'B' and args[2].lower() == 'm':
	if len(args) == 5 and cmd == 'L' and args[2] == 'm':
		x = int(args[3])
		y = int(args[4])
		xx, yy = convertpoints(x, y) #args[2] == 'm')
		#print xx, yy, x, y
		#plt.plot(xx, yy, 'o', color=currentcolor)
		currentdataset.append([xx, yy])
		# 139 18 m B

if currentdataset: datasets.append(dict(color=currentcolor, data=currentdataset))

for d in datasets:
	color = d['color']
	c = d['data']
	#print (color, len(c)) ]
	xx, yy = [x for x, y in c], [y for x, y in c]
	if len(c) == 1:
		plt.plot(xx, yy, '*', color=color)
	elif len(c) < 10:
		plt.plot(xx, yy, 's-', color=color)
	else:
		plt.plot(xx, yy, 'o', color=color)
plt.xlim(realxmin, realxmax)
plt.gca().set_xscale(xscale)
plt.ylim(realymin, realymax)
plt.gca().set_yscale(yscale)
json.dump(datasets, open(filename + ".json", 'w'), indent=4)
plt.savefig(filename + ".pdf", bbox_inches='tight')
print 'draw rectangle:', drawrect


