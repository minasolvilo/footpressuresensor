#!/usr/bin/python
from time import sleep, strftime, time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_MCP3008
import RPi.GPIO as GPIO
import csv
import os

# Software SPI configuration:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
# SPI_PORT   = 0
# SPI_DEVICE = 0
# mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
def button_callback_2(channel) :
    print('hi')

def button_callback(channel) :
    with open("/home/pi/test.csv","a") as log:
     sleep(3)
     GPIO.output(17, GPIO.HIGH)
     while True:
        # The read_adc function will get the value of the specified channel (0-7).
            values1 = mcp.read_adc(0)
            values2 = mcp.read_adc(2)
            values3 = mcp.read_adc(4)
            log.write("{0},{1},{2},{3}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(values1),str(values2),str(values3)))
            sleep(0.5)
            if ( GPIO.input(16) == True ) :
                log.close()
                GPIO.output(17, GPIO.LOW)
                sleep(2)
                GPIO.output(19, GPIO.HIGH)
                with open("/home/pi/max.csv","a") as e:
                    with open("/home/pi/test.csv","r+") as f:
                        reader = csv.reader(f)
                        answer1 = max(reader, key=lambda column: int(column[1].replace(',','')))
                        e.write("{0}\n".format(str(answer1)))
                        sleep(3)
                        GPIO.output(19, GPIO.LOW)
                        break
                    break
                    
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.add_event_detect(12,GPIO.FALLING, callback=button_callback, bouncetime=5000)

message = input("Press enter to quit\n\n")

GPIO.cleanup()
