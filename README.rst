Extract data from postscript plots
===================================

What does it do?
-----------------
* Writes out data file with points of plot.
* Recreates the plot

Caveats: 
---------
* not generally applicable, YMMV. Postscript is a programming language, not everything can be supported.
* works on at least some IDL ps2eps plots, specifically fig7b.eps fig8b.eps from http://arxiv.org/format/1206.2642v1

Technical details:
-------------------
* Uses 'C' (color) lines to identify data sets and their color.
* Uses   'a b l x y M' lines to identify data points
* Uses   'a b l x y M' lines to identify plot area (surrounding rectangle)

Author: Johannes Buchner (c) 2014

