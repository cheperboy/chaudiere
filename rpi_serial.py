#!/usr/bin/python

# SEE http://banjolanddesign.com/logging-well-depth-with-a-raspberry-pi.html


# Python 2.7.9
# RPI act as Master and Arduino act as slave (USB Link)
# Todo : implement timeouts to get out of while() statement if connection is down. SEE : https://pythonadventures.wordpress.com/2012/12/08/raise-a-timeout-exception-after-x-seconds/


#___________
#           |
# CONSTANTS |
#___________|

import serial
import os
import time
import datetime
import zlib

# ----- Packet start/end -----
startMarker = 60
endMarker = 62

# ----- Serial Port Config -----
SERIAL_PORT = "/dev/ttyACM0"
BAUDRATE = 9600

#___________
#           |
# FUNCTIONS |
#___________|

#send a char[] over serial port
def sendToArduino(trame):
#    print "RPI send " + trame
    ser.write(trame)

# read packet on serial port. 
# packet begin with startMarker "<"
# packet end with endMarker ">"
def packetFromArduino():
  global startMarker, endMarker
  trame = ""
  inchar = "z" # any value that is not an end- or startMarker
  byteCount = -1 # to allow for the fact that the last increment will be one too many
  
  # wait for the start character
  while  ord(inchar) != startMarker: 
    inchar = ser.read()
#    print inchar

  # save data until the end marker is found
  while ord(inchar) != endMarker:
    if ord(inchar) != startMarker:
      trame = trame + inchar 
      byteCount += 1
    inchar = ser.read()  
 #   print inchar
#  print "trame " + trame
  return(trame)

# Send a command
# receive response 2 times and check consistency between two packets received
# return
# - Char[] containing the received response from Arduino
# - 0 (false) if consistancy not OK
def sendCommand(command, count = 1):
    values = list()
    sendToArduino(command)
    while ser.inWaiting() == 0:
        pass
    for i in range(1, count):
        print "message count : " + str(i)
        value = packetFromArduino()
        print "value : " + value
        while ser.inWaiting() == 0:
            pass
        valueBis = packetFromArduino()
        print "value bis : " + valueBis
        if value == valueBis :
            values.append(value)
        else :
            logError(LOG_ERROR);
            print LOG_ERROR
            return None
    return values

def NEWsendCommand(command):
    values = list()
    sendToArduino(command)
    while ser.inWaiting() == 0:
        pass
    trame = packetFromArduino()
    trameValues = trame.split(";")[0]
    trameCRC = trame.split(";")[1]

    values = trameValues.split(",")
    if checkCRC(values, trameCRC):
        return values
    logError(LOG_ERROR);
    print LOG_ERROR
    return None

# Open serial port
def initSerial(serPort, baudRate):
    global port
    port = serial.Serial(serPort, baudRate)
    time.sleep(2) # give time for Arduino to reboot (else serial connection doesnet work)

def logError(message) :
    with open(ERROR_LOG_FILENAME,'a') as f:
        f.write(str(datetime.datetime.now())+" "+message+"\n")

def checkCRC(values):
    sum = 0
    crc = values.pop()
    for value in values :
        sum += int(value)
    if (int(sum) == int(crc)) :
        return True
    return False
    
   


#______________
#              |
# MAIN PROGRAM |
#______________|

#open serial port
port = serial.Serial()
initSerial(SERIAL_PORT, BAUDRATE)

port.flushInput() 
while 1:
    values = (port.readline()).split(';')
    values.pop() #remove EOL \n\r
    print values
    print checkCRC(values)

ser.close #close connection

