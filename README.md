# micropython_DS3231

<h3>Motivation:</h3>
I wrote this code mostly to learn new things in coding. I have a lot of experience with Atmel µControllers of course even Arduino's. Normally i code in Python and found out that there is micropython out there. That leads me to buy a "Raspberry Pi Pico"
  
<h3>Why did i build this project:</h3>
Honestly i didn't search the internet, wether there is already a solution out there or not. As i already mentioned i want to learn. ;-)
    
<h3>What problem does this project solve:</h3>
There isn't really a problem but makes the use of this board pretty easy. In addition the "Raspberry Pi Pico" is now capable to tell the correct time with high precision and more or less two lines of code.

<h3>What did I learn:</h3>
I learned the following things in this project 
<ul>
  <li>how to get started with the Raspberry Pi Pico and use VS Code to develope</li>
  <li>how to work with classes</li>
  <li>writing a library (never did this before)</li>
</ul>

<h3>What Features will follow in this project:</h3>
As my DS3231 Board has a EEPROM (24C32 32kbit) on board, i will include the functionalaty in this project. The Board i use, was originally for Arduino. Sadly i don't know the name of my board anymore.

<h2>How to use this library:</h2>
<ul>
  <li>copy the folder my_lib in your project</li>  
  <li>add "from my_lib import RTC_DS3231" on top of your main file.</li>
  <li>create the RTC object with "rtc = RTC_DS3231.RTC()"</li>
  <li>use "rtc.DS3231_SetTime(b'\x00\x14\x18\x28\x14\x07\x21')" (modify the time and date) to set the Time. Do this only once or if you want to correct the Time.</li>
  <li>use "t = rtc.DS3231_ReadTime(1)" to get the current Time.</li>
  <li>use "print(t)" to send the time over uart to the PC</li>
</ul>
