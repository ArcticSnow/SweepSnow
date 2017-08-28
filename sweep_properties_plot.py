from __future__ import division
import os, sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Include class and function here



# Include script in this if statement
if __name__ == '__main__':

    # Plot Laser foot print as function of distance
    x = np.linspace(0,40,1000)*1000
    beam_d_original = 12.7 # mm
    beam_divergence = 0.5  # degree
    beam_footprint = 12.7 + np.tan(beam_divergence * np.pi/180) * x
    plt.figure()
    plt.plot(x/1000, beam_footprint/10)
    plt.grid()
    plt.xlim(0,40)
    plt.ylim(0,40)
    plt.xlabel('Distance [m]')
    plt.ylabel('Laser footprint [cm]')