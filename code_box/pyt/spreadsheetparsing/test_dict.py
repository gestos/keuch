#!/usr/bin/python
import os
import csv
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
# define some colors for output later
grn = coly.GREEN
blu = coly.BLUE
cya = coly.CYAN
red = coly.RED
rst = coln.RESET_ALL

person = []
person = ["ralf", "klaus", "uwe", "micha", "paul"]
print(person)
pers_di = dict.fromkeys(person)
print(pers_di)
counter=0
for i in person:
    pers_di[i] = []
    counter += 1
    pers_di[i].append("test")
    pers_di[i].append("shoien")
print(pers_di)


