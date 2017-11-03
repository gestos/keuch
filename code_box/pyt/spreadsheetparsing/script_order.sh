#!/bin/bash
bpp='/home/keuch/gits/keuch/code_box/pyt/spreadsheetparsing'
echo ${base_parse_path}

${bpp}/rename_only.py ${bpp}/test_stats/
cp ${bpp}/test_stats/*xls ${bpp}/test_stats/archiv/
${bpp}/hotline_daily1458.py ${bpp}/test_stats/archiv/ ${bpp}/hotline_daily1458.xls
${bpp}/hotline_daily1459.py ${bpp}/test_stats/archiv/ ${bpp}/hotline_daily1459.xls
${bpp}/kws_agenten.py ${bpp}/test_stats/archiv/ ${bpp}/kws_agenten.xls
${bpp}/hotline_to_pickle1458.py ${bpp}/test_stats/archiv/ ${bpp}/pkl_plots_calls_1458.pkl
${bpp}/hotline_to_pickle1459.py ${bpp}/test_stats/archiv/ ${bpp}/pkl_plots_calls_1459.pkl
