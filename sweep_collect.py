
from __future__ import division
#from __future__ import print_function

import pandas as pd
import sys, os

#===============================================
# include functions here


from sweeppy import Sweep
import time
import sqlite3

#===============================================

'''
1- get data raw data
1.5 - get timestamp for data
2- parse data to csv
3- dump data to database (use dataset package)
[optional] 4- push data to UIO ftp server 

Function scannerON() and scannerOFF() must either power USB port on/off, or trigger a switch
'''

def scannerON():
   print('Scanner ON')
   return True


def scannerOFF():
    print('Scanner OFF')
    return True


def get_scanner_parameter():
    '''
    Function to print scanner parameters
    '''
    with Sweep('/dev/ttyUSB0') as sweep:
        motor_ready = sweep.get_motor_ready()
        motor_speed = sweep.get_motor_speed()
        sample_rate = sweep.get_sample_rate()
        sweep.get_motor_ready()
        print('Motor ready: ' + str(motor_ready))
        print('Motor speed: ' + str(motor_speed))
        print('Sample rate: ' + str(sample_rate))

        return {'motor_ready':motor_ready, 'motor_speed':motor_speed, 'sample_rate':sample_rate}


def get_profile(nscan=3):
    '''
    Function to record scan profiles
    :param nscan: number of scan profile to perform and merge
    :return: a dataframe containing the data in table format
    '''
    lscan = []
    with Sweep('/dev/ttyUSB0') as sweep:
        if sweep.get_motor_ready():
            motor_speed = sweep.get_motor_speed()
            sample_rate = sweep.get_sample_rate()
            sweep.start_scanning()
            print('Scan nbr: ')
            for n, scan in enumerate(sweep.get_scans()):
                print n,
                lscan.append(scan)

                if n == nscan:
                    sweep.stop_scanning()
                    print(' ')
                    print("======================")
                    break

    if lscan.__len__()>0:
        measurements = []
        for scan in lscan:
            for sample in scan.samples:
                measurements.append(sample)
        pdm = pd.DataFrame(measurements)
	pdm.columns = ['angle','distance','signal_strength']
        pdm['timestamp'] = int(time.time())
        pdm['sample_rate'] = sample_rate
        pdm['motor_speed'] = motor_speed

        return pdm
    else:
        return


def initialize_db_table(path2db=None, tablename=None, columnList=None):
    if path2db is None:
        path2db = '../../scanse.db'
    if tablename is None:
        tablename = 'sweep_raw'
    if columnList is None:
        columnList = '(id integer, angle integer, distance integer, signal_strength integer, timestamp integer, sample_rate integer, motor_speed integer)'
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

    path2db = '/home/bluesnow/scanse.db'
    tablename = 'sweep_raw'

    initialize_db_table(path2db, tablename)
    conn = sqlite3.connect(path2db)
    df.to_sql(tablename, conn, if_exists='append', index=False)
    conn.close()
    print("Data added to DB")


def main(argv):

    scannerON()
    #time.sleep(10)
    get_scanner_parameter()
    df = get_profile(20)
    parse_data_to_raw_DB(df)
    scannerOFF()


if __name__ == "__main__":
    main(sys.argv)
