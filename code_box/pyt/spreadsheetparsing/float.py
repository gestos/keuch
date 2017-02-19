#!/usr/bin/python
import os
import csv
import math
import xlrd
import re
import sys
from natsort import natsorted, ns
import xlwt
from xlwt import Formula
from xlutils import copy as xlcopy
from colorama import Fore as coly, Style as coln
from datetime import datetime
from datetime import date
from collections import defaultdict

flo=13.78
print(type(flo))
a,b = math.modf(flo)
print a
print b
c= round(((a*60)/100),2)
print c
print b+c
print dir(datetime.strptime)
date_objt = datetime.strptime(str(b+c), "%M.%S").time() # this is a python datetime.date object
print(date_objt)
