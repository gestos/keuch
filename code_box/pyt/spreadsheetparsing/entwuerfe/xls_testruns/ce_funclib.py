
# coding: utf-8

# In[1]:
import datetime
import pandas as pd


def determine_kernzeit(datum):
    ### Kernzeiten
    ### ab 01.03.2017: Mo-Fr 11:30-19:30
    ### ab 05.06.2017: Mo-Fr 8-20
    ### ab 08.07. plus Samstag 8-13
    weekday=datum.strftime('%a')
    print(type(datum))
    print(datum, weekday)

    if datum.date() < datetime.date(2017,3,1):
        bzeit = 'k'

    elif datetime.date(2017,3,1) <= datum.date() < datetime.date(2017,6,5):   ## Zeit zwischen 1.Maerz und 1. Juni
        if weekday in ("Sat", "Sun"): ## WE immer Nebenzeit
            bzeit = 'n'
        else:                           ## Werktage von 11:30 bis 19:30
            if datetime.time(11,30) <= datum.time() < datetime.time(19,30):
                bzeit = 'k'
            else:
                bzeit = 'n'

    elif datetime.date(2017,6,5) <= datum.date() < datetime.date(2017,7,8): ## Zeit ab 05.Juni bis 07. Juli
        if weekday in ("Sat", "Sun"): ## WE immer Nebenzeit
            bzeit = 'n'
        else:                           ## Werktage von 8-20
            if datetime.time(8,00) <= datum.time() < datetime.time(20,00):
                bzeit = 'k'
            else:
                bzeit = 'n'
    ### hier noch ab wann samstags 8-13 gezaehlt wird
    elif datum.date() >= datetime.date(2017,7,8): ## Zeit ab Sa, 08. Juli
        if weekday in ("Sun"): ## So. Nebenzeit
            bzeit = 'n'   
        elif weekday in ("Sat"): ## Sa. 8-13
            if datetime.time(8,00) <= datum.time() < datetime.time(13,00):
                bzeit = 'k'
            else:
                bzeit = 'n'
        else:                           ## Werktage von 8-20
            if datetime.time(8,00) <= datum.time() < datetime.time(20,00):
                bzeit = 'k'
            else:
                bzeit = 'n'

    return bzeit



