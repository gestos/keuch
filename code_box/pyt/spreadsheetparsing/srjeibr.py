#!/usr/bin/python
import os
import csv
from xlrd import open_workbook
import xlwt
from xlutils import copy as xlcopy
import re
import sys
from natsort import natsorted, ns

if sys.argv[1]:
    print "there's a command line argument"
    target_xls = os.path.abspath(sys.argv[1])
else:
    target_xls = os.path.abspath('target.xls')
print (target_xls)








zieldatei_ro = open_workbook(target_xls)
zieldatei_rw = xlcopy.copy(zieldatei_ro)

print dir(zieldatei_rw)

sheet_rw = zieldatei_rw.get_sheet('Sheet1')
zelle00 = sheet_rw.write(1,2, 'automatically too / two')
zieldatei_rw.save(target_xls)
