# File Name: create_velocity_files
# Author: Khang Vo
# Date Created: 3/6/2022
# Date Last Modified: 3/7/2022
# Python Version: 3.9

import os
import glob
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# glb function
def glb(velocity_file_path, teletomoDD_file_path):
    # create v_reg.txt file
    df_glb = pd.read_csv(velocity_file_path + "/ggge1202-sup-0002-ds01.txt", delim_whitespace=True)

    lat_unq = df_glb["Lat"].unique()
    long_unq = (df_glb["Long"].unique() - 180).round(2)
    depth_unq = df_glb["Depth"].unique()

    with open(teletomoDD_file_path + "/glb.txt", "w") as outfile:
        outfile.write("0.1")
        outfile.write(" ")
        outfile.write(str(len(long_unq)))
        outfile.write(" ")
        outfile.write(str(len(lat_unq)))
        outfile.write(" ")
        outfile.write(str(len(depth_unq)))
        outfile.write("\n")
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
            for y in long_unq:
                for z in lat_unq:
                    outfile.write(str(format(df_glb.iloc[index, 3], ".2f")))
                    outfile.write(" ")
                    index += 1
                outfile.write("\n")


# reg function
def reg(velovity_file_path, teletomoDD_file_path, lon_min, lon_max, lat_min, lat_max):
    # create v_reg.txt file
    df_reg = pd.read_csv(velovity_file_path + "/ggge1202-sup-0002-ds01.txt", delim_whitespace=True)
    df_reg = df_reg[(df_reg["Lat"] >= lat_min) & (df_reg["Lat"] <= lat_max)]
    df_reg = df_reg[(df_reg["Long"] - 180 >= lon_min) & (df_reg["Long"] - 180 <= lon_max)]

    lat_unq = df_reg["Lat"].unique()
    long_unq = (df_reg["Long"].unique() - 180).round(2)
    depth_unq = df_reg["Depth"].unique()

    with open(teletomoDD_file_path + "/reg.txt", "w") as outfile:
        outfile.write("0.1")
        outfile.write(" ")
        outfile.write(str(len(long_unq)))
        outfile.write(" ")
        outfile.write(str(len(lat_unq)))
        outfile.write(" ")
        outfile.write(str(len(depth_unq)))
        outfile.write("\n")
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
            for y in long_unq:
                for z in lat_unq:
                    outfile.write(str(format(df_reg.iloc[index, 3], ".2f")))
                    outfile.write(" ")
                    index += 1
                outfile.write("\n")


# run main()
if __name__ == "__main__":

    # user specified working directory
    input_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/_v_list"
    output_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/05_TeletomoDD_files"

    # user specified study area data extent
    lon_min = -80
    lon_max = -55
    lat_min = 5
    lat_max = 25

    glb(input_path, output_path)
    reg(input_path, output_path, lon_min, lon_max, lat_min, lat_max)
