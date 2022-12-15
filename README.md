# stripchart
Python Library to Plot Time Series Data Points in Real Time using Tkinter  

An attempt to simplify plotting a time series in Python. This repository's only dependancy is the Python native Tkinter library. 

To use on a headless raspberry pi zero with an OS Lite install:
 * ``ssh -X pi@mypi.local``
 * ``apt install python3-tk``
 * ``git clone https://github.com/coburnw/stripchart``
 * ``python stripchart.py``
 
The -X option to ssh is the magic that allows a Lite install to delegate Tk's graphics rendering to the clients display manager.

Todo:
 * ticks are somewhat erratic
 * x axis is in decades rather than a standard time series
 * more factoring needed to make class interaction more intuitive 
 * raise and catch a dedicated overrange event, in both x and y
  
Still very rough. Virtually untested.
