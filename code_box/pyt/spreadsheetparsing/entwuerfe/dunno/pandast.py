#!/usr/bin/python3

import os, csv, math, xlrd, re, sys, openpyxl, calendar, textwrap, itertools, pandas
from natsort import natsorted, ns
from xlwt import Formula
from xlutils import copy as xlcopy
from colorama import Fore as coly, Style as coln
from pandas import Series, DataFrame, ExcelWriter
import datetime
import matplotlib.pyplot as plt
import PyQt4
#from PyQt4 import QtGui

di= {'a': '1','b': '2','c': '3'}

fr = DataFrame.from_dict(sorted(di.items()))


for i in fr.values:
    print (i)

def myfunc(*, name, location ):
    print (name,location)
#    print frame
#    print month

myfunc(name=1,location=2)
