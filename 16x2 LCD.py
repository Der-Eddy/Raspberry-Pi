#!/usr/bin/python
#https://www.youtube.com/watch?v=CeAbyLe2Rdg

from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime, time
from datetime import datetime
from pywapi import get_weather_from_weather_com as pywapi

localcode = "GMXX1903"

lcd = Adafruit_CharLCD()

cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"

lcd.begin(16,1)

def run_cmd(cmd):
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = p.communicate()[0]
        return output

ipaddr = run_cmd(cmd)
weather = pywapi(localcode)
while 1:
        lcd.clear()
        lcd.message(datetime.now().strftime('%b %d  %H:%M:%S\n'))
        lcd.message(" " + ipaddr)
        sleep(2)

        lcd.clear()
        lcd.message(datetime.now().strftime('%b %d  %H:%M:%S\n'))
        unix = str(int(time()))
        lcd.message(unix.center(16, "-"))
        sleep(2)

        lcd.clear()
        lcd.message(datetime.now().strftime('%b %d  %H:%M:%S\n'))
        condition = weather["current_conditions"]["text"]
        if condition.find(" ") > 0:
                #print condition
                #Example: Condition is "Mostly Cloudy"
                condition = condition.split()
                condition = condition[1]
                #print condition
        weather_text = condition + " / " + weather["current_conditions"]["temperature"] + " C"
        lcd.message(weather_text.center(16))
        sleep(2)
        while True:
                weather = pywapi(localcode)
                if len(weather) == 4:
                        break
