# CyGnusPlotter

&emsp; Although installing CyGnusPlotter is not difficult, you might have to do a few manipulation because for CyGnusPlotter depends on Python.  
&emsp; The way to install and uses are described here.

## Install Python 3

&emsp; You should install Python 3 if this is the first time using Python 3 on a machine you want to install CyGnusPlotter, except rare cases.

&emsp; [Download Python 3.x](https://www.python.org/)  
&emsp; [A Beginner's Python Tutorial/Installing Python](https://en.wikibooks.org/wiki/A_Beginner%27s_Python_Tutorial/Installing_Python)  

&emsp; The author recommends checking "Add Python 3.x to PATH" for Windows users. If not checking, a use of a command prompt below may not work.  
&emsp; NOTE: CyGnusPlotter does **NOT** work in Python 2.  

## Install CyGnusPlotter
&emsp; To install CyGnusPlotter, you should just download by clicking green top-right "Clone or download" button and unzip.  
&emsp; The name of the unzipped folder includes a branch name such as, "master", but you have not to mind it.  

## Open CyGnusPlotter's Graphical user interface

### For Windows users
&emsp; Windows users can open CyGnusPlotter's GUI in two ways described below.  
  
**Windows Explorer:**  
&emsp; Open "CyGnusPlotterGUI.py" with Python 3.x.  
  
**command prompt:**  
&emsp; The current directory is assumed CyGnusPlotter's parent path.
~~~
    > python ./CyGnusPlotterGUI.py
~~~
  

### For Mac, UNIX or Linux users
&emsp; UNIX like systems users can open CyGnusPlotter's GUI in two ways described below.  
  
**Mac OSX Finder or other file managers:**  
&emsp; Change "CyGnusPlotterGUI" to be executable, and click and run it in Terminal.  
&emsp; Older versions of Unix like systems may show different behavior.  


**Terminal:**  
&emsp; The current directory is assumed CyGnusPlotter's parent path.
~~~
    $ python3 ./CyGnusPlotterGUI.py
~~~
  

## Use CyGnusPlotter in Python's interactive mode
&emsp; The current directory is assumed CyGnusPlotter's parent path.
~~~
    >>> from cyglib import cyginput
~~~



# LICENSE
&emsp; Except for Bottle, CyGnusPlotter is distributed under  the Educational Community License, Version 2.0.
&emsp; The CyGnusPlotter distribution includes web framework Bottle, being written by Marcel Hellkamp and available under MIT license.