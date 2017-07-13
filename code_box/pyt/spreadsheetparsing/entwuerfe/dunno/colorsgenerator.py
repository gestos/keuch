#!/usr/bin/python
"""Build an .xls file with all background colors vs patterns possibilities"""

import xlwt

wb = xlwt.Workbook()
ws = wb.add_sheet("Colors")

ws.write(0, 0, "Colors/Patterns")
for pat_index in range(0, 16):
    ws.write(0, pat_index + 1, str(pat_index))

for i in range(0, 250):

    hex_color = hex(i)

    # print color hex code
    ws.write(i +1, 0, unicode(hex_color))

    # pattern index may vary between 0 and 16
    for pat_index in range(0, 16):

        pattern = xlwt.Pattern()
        pattern.pattern = pat_index
        pattern.pattern_fore_colour = i

        some_style = xlwt.XFStyle()
        some_style.pattern = pattern

        ws.write(i + 1, 1 + pat_index, "", some_style)

wb.save("excel_color.xls")
