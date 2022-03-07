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

lat_unq = df_reg["Lat"].unique()
long_unq = (df_reg["Long"].unique() - 180).round(2)
depth_unq = df_reg["Depth"].unique()

lat_list = df_reg["Lat"]
long_list = (df_reg["Long"] - 180).round(2)
depth_list = df_reg["Depth"]

with open(output_path + "/glb.txt", "w") as outfile:
    for i in long_unq:
        outfile.write(str(i))
        outfile.write(" ")
    outfile.write("\n")
    for j in lat_unq:
        outfile.write(str(j))
        outfile.write(" ")
    outfile.write("\n")
    for k in depth_unq:
        outfile.write(str(k))
        outfile.write(" ")
    outfile.write("\n")

    index = 0
    for x in depth_unq:
        for y in lat_unq:
            for z in long_unq:
                outfile.write(str(df_reg.iloc[index, 3]))
                outfile.write(" ")
                index += 1
            outfile.write("\n")
