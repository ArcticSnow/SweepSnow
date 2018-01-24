from __future__ import division
import os, sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''
File containing functions and classes to print
'''


# Include class and function here
def read_sweepCSV(filename):
    data = pd.read_csv(filename, sep=', ')

    return data

filename = '/home/arcticsnow/Github/sweepy/sweep.csv'
sw = read_sweepCSV(filename)
plt.figure()
plt.scatter(sw.x, sw.y, c=sw.signal_strength)

# Include script in this if statement
if __name__ == '__main__':