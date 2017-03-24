#!/usr/bin/python
import os, csv, math, xlrd, re, sys, openpyxl, calendar, textwrap, itertools, pandas
from natsort import natsorted, ns
from xlwt import Formula
from xlutils import copy as xlcopy
from colorama import Fore as coly, Style as coln
from pandas import Series, DataFrame, ExcelWriter
import datetime

di= {'a': '1','b': '2','c': '3'}

fr = DataFrame.from_dict(sorted(di.items()))


for i in fr.values:
    print i
