##########################################
### This Code is for Raspberry Pi Pico ###
###      copyright 2021 balance19      ###
##########################################

from my_lib import RTC_DS3231
import time

# Initialisation of RTC object. Several settings are possible but everything is optional.
# If you meet the standards (see /my_lib/RTC_DS3231.py) no parameters are needed.
rtc = RTC_DS3231.RTC()

# It is encoded like this: sec min hour week day month year.
# Uncomment the line below to set time. Do this only once otherwise time will be set everytime the code is executed.
# rtc.DS3231_SetTime(b'\x00\x14\x18\x28\x14\x07\x21')

while True:
    t = rtc.DS3231_ReadTime(1)  # Read RTC and receive data in Mode 1 (see /my_lib/RTC_DS3231.py)
    print(t)
    time.sleep(1)
