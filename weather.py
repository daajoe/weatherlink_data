#!/usr/bin/env python

import datetime

# timestamp: function takes in a datetime.datetime object and returns the 
#            corresponding "timestamp" value necessary in the API request.
#            The value is just the first 4 bytes of the archive record -- the
#            Date Stamp followed by the Time Stamp. The only trick is to 
#            multiply the Date Stamp by 2^16 (since it is the first 2 of the 4
#            bytes) before summing the Time Stamp and Date Stamp. 
def timestamp(t):
    vantageTimeStamp = (100 * t.hour) + t.minute
    vantageDateStamp = t.day + (t.month * 32) + ((t.year - 2000) * 512)
    return (vantageDateStamp * 2**16) + vantageTimeStamp


# test that the given date produces results in 416351713
d = datetime.datetime.strptime("6/17/2012 15:05", "%m/%d/%Y %H:%M")
print timestamp(d)
