from datetime import datetime
import math
from decimal import Decimal, getcontext

def float_to_minute(duration_f):
    getcontext().prec = 2
    hour = int(duration_f)
    minute = int((Decimal(duration_f) - Decimal(int(duration_f)))  * 100)

    return hour * 60 + minute

def float_to_timestr(time_f):
    getcontext().prec = 2
    hour = int(time_f)
    minute = int((Decimal(time_f) - Decimal(int(time_f))) * 100)

    return str(hour) + "." + str(minute)

def float_to_datetime(time_f):
    if time_f >= 24.00:
        return "23:59"
    t1_str = float_to_timestr(time_f)
    fmt = "%H.%M"
    return datetime.strptime(t1_str,fmt).strftime("%H:%M")

def distance_between_time_in_minute(time_f1, time_f2):
    t1_str = float_to_timestr(time_f1)
    t2_str = float_to_timestr(time_f2)

    fmt = "%H.%M"
    d1 = datetime.strptime(t1_str,fmt)
    d2 = datetime.strptime(t2_str,fmt)

    if d2 > d1:
        diff = d2 - d1
    else:
        diff = d1 - d2

    return diff.seconds // 60

def minutes_to_float(minutes):
    return (minutes // 60) + (minutes % 60)/100