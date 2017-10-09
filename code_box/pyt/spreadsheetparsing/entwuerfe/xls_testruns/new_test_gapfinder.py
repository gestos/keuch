#!/usr/bin/python3
import os, csv, math, xlrd, re, sys, xlwt, calendar, textwrap, itertools, pandas
from natsort import natsorted, ns
from xlwt import Formula
from xlutils import copy as xlcopy
from colorama import Fore as coly, Style as coln
from datetime import date, timedelta
import numpy as np
from itertools import tee#, izip

days=pandas.read_pickle('./testpickle.pkl')
print(type(days))
datelist=days[0].tolist()

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b)
    return zip(a, b)

def missing_dates(dates):
    print(type(dates))
    input('keypress')
    print(sorted(dates))
    input('keypress')
    for prev, curr in pairwise(sorted(dates)):
        i = prev
        while i + timedelta(1) < curr:
            i += timedelta(1)
            yield i

dates=datelist
del dates[-3]

dates2 = [ date(2010, 1, 8),
        date(2010,1,2),
        date(2010,1,5),
        date(2010,1,1),
        date(2010,1,7) ]


for missing in missing_dates(dates):
    print('missing days:')
    print (missing)

print (dates[-8:])
