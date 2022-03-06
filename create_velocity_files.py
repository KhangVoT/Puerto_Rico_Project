import os
import glob
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# user specified working directory
input_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/_v_list"
output_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/05_TeletomoDD_files"

# create v_reg.txt file
df_reg = pd.read_csv(input_path + "/ggge1202-sup-0002-ds01.txt", delim_whitespace=True)

lat_list = df_reg["Lat"].unique()
long_list = df_reg["Long"].unique()
depth_list = df_reg["Depth"].unique()
print(lat_list)
print(long_list)
print(depth_list)
