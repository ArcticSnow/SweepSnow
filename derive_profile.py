#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys, os

import dataset


#===============================================
# include functions here


'''
1- connect to DB table containing the raw data
2- load latest data
3- derive snow surface from raw data

Sqlite DB ressources:
https://sqlite.org/cli.html
https://www.tutorialspoint.com/sqlite/sqlite_create_database.htm


'''

db = dataset.connect('sqlite:///scanse.db')
table = db['sweep_raw']


def load_raw_data()

    return df

def estimate_snow_profile(df_raw):
    return


#===============================================


def main(argv):
    #===========================================
    # My code here
    pass


if __name__ == "__main__":
    main(sys.argv)
