##########################################
### This Code is for Raspberry Pi Pico ###
###      copyright 2021 balance19      ###
##########################################

from my_lib import RTC_DS3231
import time

#initialisation of RTC object. Several settings are possible but everything is optional. If you meet the standards (see /my_lib/RTC_DS3231.py) no parameter's needed.
rtc = RTC_DS3231.RTC()

while True:
    t = rtc.DS3231_ReadTime(1)  #read RTC and receive data in Mode 1 (see /my_lib/RTC_DS3231.py)
    print(t)
    time.sleep(1)
