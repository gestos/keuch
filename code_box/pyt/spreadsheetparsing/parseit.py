#!/usr/bin/python
import os
import csv
import xlrd
import re
import sys
from natsort import natsorted, ns
import xlwt
from xlutils import copy as xlcopy

print len(sys.argv)

if len(sys.argv) > 1:
#    print "there's a command line argument"
    daily_report_dir_path = os.path.abspath(sys.argv[1])
else:
    daily_report_dir_path = '/home/keuch/gits/wiki_carex/stats/Hotlineber1458Gesing_taegl_217_HOURLY/'
    
print (daily_report_dir_path)

liste_aller_gelesenen_files = list()

for tabelle in natsorted(os.listdir(daily_report_dir_path), alg=ns.IGNORECASE, reverse=True):
    if tabelle.endswith(".xls"):
        tabelle_fullpath = os.path.join(daily_report_dir_path, tabelle)
        ganze_tabelle = xlrd.open_workbook(tabelle_fullpath)
        erstes_sheet = ganze_tabelle.sheet_by_index(0)
        zeilen = erstes_sheet.nrows
        Datum_B2 = erstes_sheet.cell(1,1).value
        Datum_korrekt = re.sub(r' ', '.', Datum_B2[:10]) 
        Date_usable = Datum_korrekt.encode("utf-8")
        datensatz_fuer_dieses_sheet = list()

#        print(zeilen)
#        print (tabelle_fullpath)
#        print (Datum_korrekt)

        datensatz_fuer_dieses_sheet.append(Date_usable)

        wanted_cols = [2,3,4,5,12] # this is a comment 2=alle anrufe 3=telefonierte anrufe 4=gesamtanrufzeit 5=gesamtverbindungszeit 12=gesamtNBzeit
        for Spalte in wanted_cols:
            summe = int()
#            print ("{}: {}".format("Spalte", Spalte))
            for summenreihen in range(4,28):
                summand = erstes_sheet.cell(summenreihen,Spalte).value
                # print (summand)
                summe = summe+summand
#            print (summe)
            datensatz_fuer_dieses_sheet.append(summe)
#        print(datensatz_fuer_dieses_sheet)
        liste_aller_gelesenen_files.append(datensatz_fuer_dieses_sheet)
#        print
    


#### END READER ####

#### BEGIN WRITER ####

targetfile = '/home/keuch/gits/keuch/code_box/pyt/spreadsheetparsing/target.xls'
target_workbook = xlrd.open_workbook(targetfile)
sheets_in_targetfile = target_workbook.sheet_names()
print (sheets_in_targetfile)
targetsheet = target_workbook.sheet_by_index(0)
schon_befueelt = targetsheet.nrows
print(schon_befueelt)
print (liste_aller_gelesenen_files[0]) # This shows that the list from above is still populated and available even outside the for loop


row_to_write_in = schon_befueelt +1
print (row_to_write_in)

target_workbook_writeable = xlcopy.copy(target_workbook)
sheet_rw = target_workbook_writeable.get_sheet(0)

for einzelner_datensatz in liste_aller_gelesenen_files:
    idx = 0
    for spalte_eines_datensatzes in einzelner_datensatz:
        sheet_rw.write(row_to_write_in, idx, spalte_eines_datensatzes)
        idx = idx + 1
    row_to_write_in = row_to_write_in + 1

target_workbook_writeable.save(targetfile)


# xlrd can't get the values of formula cells because those are only created when the file was saved (with "recalculate" option) in excel (or LO)
# so cells with formulas always return value "0.0" until they've been saved locally
