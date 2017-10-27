#!/bin/bash

./rename_only.py test_stats/
cp test_stats/*xls test_stats/archiv/
./hotline_daily1458.py test_stats/archiv/ hotline_daily1458.xls
./hotline_daily1459.py test_stats/archiv/ hotline_daily1459.xls
./kws_agenten.py test_stats/archiv/ kws_agenten.xls
./hotline_to_pickle1458.py test_stats/archiv/ pkl_plots_calls_1458.pkl
./hotline_to_pickle1459.py test_stats/archiv/ pkl_plots_calls_1459.pkl
