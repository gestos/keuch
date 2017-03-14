#!/usr/bin/python
import os, csv, math, xlrd, re, sys, xlwt, calendar, textwrap, pandas
from natsort import natsorted, ns
from xlwt import Formula
from xlutils import copy as xlcopy
from colorama import Fore as coly, Style as coln
import datetime
import matplotlib.pyplot as plt

i="B Gesing Carexpert 995887"

teile = re.compile(r'(^\D)\s(.*)(\b\d[\d\s]*$)')
try:
    standort = teile.match(i).group(1).strip()
    kuerzel = teile.match(i).group(2).strip()
    id_num = int(teile.match(i).group(3).strip())
    print standort
    print kuerzel
    print id_num
except:
        print("sth wrong with " + str(i))
 
