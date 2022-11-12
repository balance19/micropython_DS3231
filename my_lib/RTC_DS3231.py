##########################################
### This Code is for Raspberry Pi Pico ###
###      copyright 2021 balance19      ###
##########################################

import machine

# Class for getting Realtime from the DS3231 in different modes.
class RTC:
    w = ["FRI", "SAT", "SUN", "MON", "TUE", "WED", "THU"]
    # If you want different names for Weekdays, feel free to add. Couple examples below:
    # w = ["FR", "SA", "SU", "MO", "TU", "WE", "TH"]
    # w = ["Friday", "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
    # w = ["Freitag", "Samstag", "Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag"]
    # w = ["viernes", "sabado", "domingo", "lunes", "martes", "miercoles", "jueves"]

    # Initialisation of RTC object. Several settings are possible but everything is optional.
    # If you meet these standards no parameters are required.
    def __init__(self, sda_pin=16, scl_pin=17, port=0, speed=100000, address=0x68, register=0x00):
        self.rtc_address = address  # for using different i2c address
        self.rtc_register = register  # for using different register on device. DON'T change for DS3231
        sda = machine.Pin(sda_pin)  # configure the sda pin
        scl = machine.Pin(scl_pin)  # configure the scl pin
        self.i2c = machine.I2C(port, sda=sda, scl=scl, freq=speed)  # configure the i2c interface with given parameters

    # Method for setting the Time
    def DS3231_SetTime(self, NowTime=b"\x00\x23\x12\x28\x14\x07\x21"):
        # NowTime has to be in format like b'\x00\x23\x12\x28\x14\x07\x21'
        # It is encoded like this           sec min hour week day month year
        # Then it's written to the DS3231
        self.i2c.writeto_mem(int(self.rtc_address), int(self.rtc_register), NowTime)

    # DS3231 gives data in bcd format. This has to be converted to a binary format.
    def bcd2bin(self, value):
        return (value or 0) - 6 * ((value or 0) >> 4)

    # Add a 0 in front of numbers smaller than 10
    def pre_zero(self, value):
        pre_zero = True  # Change to False if you don't want a "0" in front of numbers smaller than 10
        if pre_zero:
            if value < 10:
                value = f"0{value}"  # From now on the value is a string!
        return value

    # Read the Realtime from the DS3231 with errorhandling. Currently two output modes can be used.
    def DS3231_ReadTime(self, mode=0):
        try:
            # Read RT from DS3231 and write to the buffer variable. It's a list with 7 entries.
            # Every entry needs to be converted from bcd to bin.
            buffer = self.i2c.readfrom_mem(self.rtc_address, self.rtc_register, 7)
            # The year consists of 2 digits. Here 2000 years are added to get format like "2021"
            year = self.bcd2bin(buffer[6]) + 2000
            month = self.bcd2bin(buffer[5])  # Just put the month value in the month variable and convert it.
            day = self.bcd2bin(buffer[4])  # Same for the day value
            # Weekday will be converted in the weekdays name or shortform like "Sunday" or "SUN"
            weekday = self.w[self.bcd2bin(buffer[3])]
            # Uncomment the line below if you want a number for the weekday and comment the line before.
            # weekday = self.bcd2bin(buffer[3])
            hour = self.pre_zero(self.bcd2bin(buffer[2]))  # Convert bcd to bin and add a "0" if necessary
            minute = self.pre_zero(self.bcd2bin(buffer[1]))  # Convert bcd to bin and add a "0" if necessary
            second = self.pre_zero(self.bcd2bin(buffer[0]))  # Convert bcd to bin and add a "0" if necessary
            if mode == 0:  # Mode 0 returns a list of second, minute, ...
                return second, minute, hour, weekday, day, month, year
            if mode == 1:  # Mode 1 returns a formated string with time, weekday and date
                time_string = f"{hour}:{minute}:{second}      {weekday} {day}.{month}.{year}"
                return time_string
            # If you need different format, feel free to add

        except Exception as e:
            return (
                "Error: is the DS3231 not connected or some other problem (%s)" % e
            )  # exception occurs in any case of error.
