#!/usr/bin/env/python
__author__ = 'Simon Filhol'
from __future__ import division
#from __future__ import print_function

import pandas as pd
import sys, os, getopt, serial, re

#===============================================
# include functions here
import time, math
import sqlite3



def maxbotixON():
	# add logic to turn maxbotix ON
   	print('Maxbotix ON')
  	return True


def maxbotixOFF():
	# add logic to turn maxbotix OFF
	print('Maxbotix OFF')
    return True

def get_distance(myserial):
	# define the serial connection to the rangefinder, 9600 8n1
	
	# Output from the rangefinder will be in the following format:
	#  ...R####\rR####\rR####\r...
	#  where "####" is the range in mm, 300-5000, and "\r" is a carriage return

	# Get 65 bytes of output (11 values worth) from the rangefinder,
	#  split it into an array on the '\r' and 'R' characters.
	#  (The first value doesn't drop the "R", so we ignore that, resulting in
	#   10 expected good values)

	timestamp = int(time.time())
	rawdata = myserial.read(65)
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

	if count > 0:
	    # Calculate that average
	    avg = int(round(sum / count))

	return avg, timestamp


def collect_measurments(nbmeasurement=10):

	ser = serial.Serial(
	    port='/dev/ttyAMA0',
	    baudrate = 9600,
	    bytesize=serial.EIGHTBITS,
	    parity=serial.PARITY_NONE,
	    stopbits=serial.STOPBITS_ONE,
	    timeout=1)

	mlist = []
	for i in range(0,nbmeasurement):
		dist, timestamp = get_distance(myserial = ser)
		mlist.update({timestamp:dist})
	pdm = pd.DataFrame(mlist.items(), columns=['timestamp','distance'])
	return pdm


def initialize_db_table(path2db=None, tablename=None, columnList=None):
    if path2db is None:
        path2db = '/home/driftlidar/scanse.db'
    if tablename is None:
        tablename = 'maxbotix_raw'
    if columnList is None:
        columnList = '(id integer,  distance interger,timestamp integer)'
    executeCmd = 'create table if not exists ' + tablename + ' ' + columnList
    conn = sqlite3.connect(path2db)
    cur = conn.cursor()
    cur.execute(executeCmd)
    conn.commit()
    conn.close()


def parse_data_to_raw_DB(df):
    '''
    Parse data into a table containing the raw data
    :param df:
    :return:
    '''

    path2db = '/home/driftlidar/scanse.db'
    tablename = 'sweep_raw'

    initialize_db_table(path2db, tablename)
    conn = sqlite3.connect(path2db)
    try:
        df.to_sql(tablename, conn, if_exists='append', index=False)
        conn.close()
        print("Data added to DB")
    except:
        print("WARNING: could not add data to DB")


def main(argv):

    nbmeasurement = 10

    try:
        opts, args = getopt.getopt(sys.argv[1:], "nbm:" )
    except getopt.GetoptError as e:
        print str(e)
        sys.exit(2)
    for o, a in opts:
        if o == '-nbm':
            nbmeasurement = a
    print ("Number of measurement = %d" % (nbmeasurement))


    maxbotixON()
    df = collect_measurments(nbmeasurement)
    parse_data_to_raw_DB(df)
    maxbotixOFF()


if __name__ == "__main__":
    main(sys.argv)