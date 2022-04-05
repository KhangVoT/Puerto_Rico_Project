"""in the works script to interpolate global velocity model to become more coarse"""

import os
import glob
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.interpolate import LinearNDInterpolator

ak135_file = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/_v_list/ak135.txt"
mit_file = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/_v_list/ggge1202-sup-0002-ds01.txt"

df = pd.read_csv(mit_file, delim_whitespace=True)

points = df[["Lat", "Long", "Depth"]].to_numpy()
values = np.array(df["dVp"])

request = np.array([[50, 50, 100], [100, 100, 150]])

print(griddata(points, values, request))

# ak135 = pd.read_csv(ak135_file, delim_whitespace=True, header=None, skiprows=1)
#
# depth = ak135.iloc[:, 0]
# velP = ak135.iloc[:, 1]
# vel_new = np.interp(depth_unq, depth, velP)
# vel_new = vel_new.round(4)
