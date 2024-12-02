# stripchart
Python Library to Plot Time Series Data Points in Real Time using Tkinter  

An attempt to simplify plotting a time series in Python. This repository's only dependancy is the Python native Tkinter library. 

To use on a headless Raspberry Pi Zero with an OS Lite install:
 * ``ssh -X pi@mypi.local``
 * ``apt install python3-tk``
 * ``git clone https://github.com/coburnw/stripchart``
 * ``python src/stripchart/chart.py``

The -X option of ssh is the magic that allows a Lite install to delegate Tk's graphics rendering to the clients display manager.

To install for your own use:
 * ``python -m venv --prompt prompt_name venv``
 * ``source venv/bin/activate``
 * ``git clone http://github.com/coburnw/stripchart.git``
 * ``cd stripchart``
 * ``pip install --editable .``
 
Todo:
 * ticks are somewhat erratic
 * x axis scale is in decades rather than a time series
 * more factoring needed to make class interaction by the developer more intuitive 
 * raise and catch dedicated overrange events, in both x and y
 * fix the many omissions

Credit:
 * Tk Best Practices [https://tkdocs.com/index.html](https://tkdocs.com/index.html)
 * Enrico's [tkintr](https://github.com/enrico-dibacco/tkinter) repository for the first example that clicked
 
Still very rough. Virtually untested.
