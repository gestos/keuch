#!/usr/bin/python3
import os, csv, math, xlrd, re, sys, xlwt, calendar, textwrap, itertools, pandas
from natsort import natsorted, ns
from xlwt import Formula
from xlutils import copy as xlcopy
from colorama import Fore as coly, Style as coln
import datetime
import numpy as np

days=pandas.read_pickle('./testpickle.pkl')
print(type(days))
print(days.ix)
print(list(days))


