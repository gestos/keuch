#!/bin/bash
bp='/home/keuch/gits/keuch/code_box/pyt/spreadsheetparsing/'
bpp='/home/keuch/gits/keuch/code_box/pyt/spreadsheetparsing/datenhalde/'
echo ${bpp}

${bp}/rename_only.py ${bpp} &&
mv ${bpp}/1458_daily* ${bpp}/1458/ &&
mv ${bpp}/1459_daily* ${bpp}/1459/ &&
mv ${bpp}/CE_alle* ${bpp}/alle_agents_taeglich/ &&

${bp}/daily_1458.py ${bpp}/1458/ ${bp}/hotline_daily1458.xls &&
${bp}/daily1459.py ${bpp}/1459/ ${bp}/hotline_daily1459.xls &&
${bp}/kws_agenten.py ${bpp}/alle_agents_taeglich/ ${bp}/kws_agenten.xls &&

${bp}/Datensammler.py
