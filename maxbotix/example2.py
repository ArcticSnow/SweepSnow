#!/usr/bin/env python

# apt-get install python-serial
import serial
import re

# define the serial connection to the rangefinder, 9600 8n1
ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate = 9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

# Output from the rangefinder will be in the following format:
#  ...R####\rR####\rR####\r...
#  where "####" is the range in mm, 300-5000, and "\r" is a carriage return

# Get 65 bytes of output (11 values worth) from the rangefinder,
#  split it into an array on the '\r' and 'R' characters.
#  (The first value doesn't drop the "R", so we ignore that, resulting in
#   10 expected good values)
rawdata = ser.read(65)
rawdata = re.split('\rR', rawdata)

# Initialize the vars used in the loop
sum = 0
count = 0

# Step through the raw data
for item in rawdata:
    # Make sure the array item is valid data
    if re.search('^[0-9][0-9][0-9][0-9]$', item):
        # Convert the array item to a float
        value = float(item)
        # Make sure it's inside the reasonable range of the rangefinder
        if value > 299 and value < 5001:
            # Increment the values
            sum = sum + value
            count = count + 1

print count

if count > 0:
    # Calculate that average
    avg = sum / count

    # Dump the output as an integer
    #  It's not really accurate sub-millimeter, let's not pretend it is.
    print "%0.0f" % avg

