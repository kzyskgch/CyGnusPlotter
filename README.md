# CyGnusPlotter

&emsp; Installing CyGnusPlotter is not difficult, however, you might have to do a few manipulation because CyGnusPlotter depends on Python.  
&emsp; The way to install and uses are described here.

## Install Python 3

&emsp; If this is the first time using Python 3 on a machine you want to install CyGnusPlotter, you should install the Python 3 except rare cases. 

&emsp; [Download Python 3.x](https://www.python.org/)  
&emsp; [A Beginner's Python Tutorial/Installing Python](https://en.wikibooks.org/wiki/A_Beginner%27s_Python_Tutorial/Installing_Python)  

&emsp; NOTE: CyGnusPlotter does **NOT** work in Python 2.  
&emsp; NOTE: For  Windows users, checking "Add Python 3.x to PATH" is recommended when installing. If not checking, a use of a command prompt below may not work.  

## Install CyGnusPlotter
&emsp; Download by clicking green top-right "Clone or download" button and unzip.  
&emsp; The name of the unzipped folder includes a branch name such as "master" but you have not to mind it.  

## Open CyGnusPlotter's graphical user interface

### For Windows users
&emsp; Windows users can open CyGnusPlotter's GUI in two ways described below.  
  
**Explorer (i.e. on the window):**  
&emsp; Open "CyGnusPlotterGUI.py" with Python 3.x.  
  
**Command prompt:**  
&emsp; Make sure that the current directory is the parent path of CyGnusPlotter and execute the next line.
~~~
    > python ./CyGnusPlotterGUI.py
~~~
  

### For Mac, UNIX or Linux users
&emsp; UNIX like systems users can open CyGnusPlotter's GUI in two ways described below.  
  
**Mac OSX Finder or other file managers (i.e. on the window):**  
&emsp;  Change "CyGnusPlotterGUI.py" to be executable, click and run it in Terminal.  
&emsp; Older versions of Unix like systems may show different behavior.  


**Terminal:**  
&emsp; Make sure that the current directory is the parent path of CyGnusPlotter and execute the next line.
~~~
    $ python3 ./CyGnusPlotterGUI.py
~~~
  

## Use CyGnusPlotter in Python's interactive mode
&emsp; Make sure that the current directory is the parent path of CyGnusPlotter and import cyglib as the next line.
~~~
    >>> from cyglib import cyginput
~~~



# LICENSE
&emsp; Except for Bottle, CyGnusPlotter is distributed under  the Educational Community License, Version 2.0.   
&emsp; The CyGnusPlotter distribution includes web framework Bottle, being written by Marcel Hellkamp and available under MIT license. 