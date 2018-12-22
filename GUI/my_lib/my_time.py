from datetime import datetime
import math

def float_to_minute(duration_f):
    hour = int(duration_f)
    minute = int(math.ceil((duration_f - int(duration_f))  * 100))

    return hour * 60 + minute

def float_to_timestr(time_f):
    hour = int(time_f)
    minute = int(math.ceil((time_f - int(time_f))  * 100))

    return str(hour) + "." + str(minute)

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