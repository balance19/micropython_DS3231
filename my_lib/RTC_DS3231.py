##########################################
### This Code is for Raspberry Pi Pico ###
###      copyright 2021 balance19      ###
##########################################

import machine

#class for getting Realtime from the DS3231 in different modes.
class RTC:
    w = ["FRI","SAT","SUN","MON","TUE","WED","THU"] #if you want different names for Weekdays, feel free to add.
    #w = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    
    #initialisation of RTC object. Several settings are possible but everything is optional. If you meet this standards no parameter's needed.
    def __init__(self, sda_pin=16, scl_pin=17, port=0, speed=100000, address=0x68, register=0x00):
        self.rtc_address = address      #for using different i2c address
        self.rtc_register = register    #for using different register on device. DON'T change for DS3231
        sda=machine.Pin(sda_pin)        #configure the sda pin
        scl=machine.Pin(scl_pin)        #configure the scl pin
        self.i2c=machine.I2C(port,sda=sda, scl=scl, freq=speed) #configure the i2c interface with given parameters

    #function for setting the Time
    def DS3231_SetTime(self, NowTime = b'\x00\x23\x12\x28\x14\x07\x21'):
        # NowTime has to be in format like b'\x00\x23\x12\x28\x14\x07\x21'
        # It is encoded like this           sec min hour week day month year
        # Then it's written to the DS3231
        self.i2c.writeto_mem(int(self.rtc_address), int(self.rtc_register),NowTime)

    #the DS3231 gives data in bcd format. This has to be converted to binary format.
    def bcd2bin(self, value):
        return (value or 0) - 6 * ((value or 0) >> 4)

    #add a 0 in front of numbers smaler than 10
    def pre_zero(self, value):
        pre_zero = True #change to False if you don't want a "0" in fron of numbers smaler than 10
        if pre_zero:
            if value < 10:
                value = "0"+str(value)  #from now the value is a string!
        return value

    #read the Realtime from the DS3231 with errorhandling. Several output modes can be used.
    def DS3231_ReadTime(self,mode=0):
        try:
            buffer = self.i2c.readfrom_mem(self.rtc_address,self.rtc_register,7)    #read RT from DS3231 and write to the buffer variable. It's a list with 7 entries. Every entry needs to be converted from bcd to bin.
            year = self.bcd2bin(buffer[6]) + 2000           #the year consists of 2 digits. Here 2000 years are added to get format like "2021"
            month = self.bcd2bin(buffer[5])                 #just put the month value in the month variable and convert it.
            day = self.bcd2bin(buffer[4])                   #same for the day value
            weekday = self.w[self.bcd2bin(buffer[3])]       #weekday will be converted in the weekdays name or shortform like "Sunday" or "SUN"
            #weekday = self.bcd2bin(buffer[3])              #remove comment in this line if you want a number for the weekday and comment the line before.
            hour = self.pre_zero(self.bcd2bin(buffer[2]))   #convert bcd to bin and add a "0" if necessary
            minute = self.pre_zero(self.bcd2bin(buffer[1])) #convert bcd to bin and add a "0" if necessary
            second = self.pre_zero(self.bcd2bin(buffer[0])) #convert bcd to bin and add a "0" if necessary
            if mode == 0:   #mode 0 returns a list of second, minute, ...
                return second, minute, hour, weekday, day, month, year
            if mode == 1:   #mode 1 returns a formated string with time, weekday and date
                time_string = str(hour) + ":" + str(minute) + ":" + str(second) + "      " + weekday + " " + str(day) + "." + str(month) + "." + str(year)
                return time_string
            #if you need different format, feel free to add
        
        except Exception as e:
            return "Error: is the DS3231 not connected or some other problem (%s)" % e #exception occurs in any case of error.
