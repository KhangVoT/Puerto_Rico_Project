# File Name: create_velocity_files
# Author: Khang Vo
# Date Created: 3/6/2022
# Date Last Modified: 3/22/2022
# Python Version: 3.9

import os
import glob
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def output_df(long_unq, lat_unq, depth_unq, dvp, vel_new, teletomoDD_file_path, file_name):
    with open(teletomoDD_file_path + "/" + file_name + ".txt", "w") as outfile:
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

        if "_abs" in file_name:
            m = 0
            for _ in depth_unq:
                for _ in lat_unq:
                    for _ in long_unq:
                        outfile.write(str(format(vel_new[m], ".2f")))
                        outfile.write(" ")
                    outfile.write("\n")
                m += 1
        elif "_perturb" in file_name:
            m = 0
            n = 0
            for i in depth_unq:
                for _ in lat_unq:
                    for _ in long_unq:
                        if i < 0:
                            outfile.write(str(format(vel_new[n], ".2f")))
                            outfile.write(" ")
                        else:
                            outfile.write(str(format((vel_new[n] * (1 + dvp.iloc[m] / 100)), ".2f")))
                            outfile.write(" ")
                            m += 1
                    outfile.write("\n")
                n += 1


# glb function
def glb(ak135_file, mit_file, teletomoDD_file_path):
    df_glb = pd.read_csv(mit_file, delim_whitespace=True)

    lat_unq = df_glb["Lat"].unique()
    long_unq = (df_glb["Long"].unique() - 180).round(2)
    depth_unq = df_glb["Depth"].unique()
    dvp = df_glb["dVp"]

    lat_unq[0] = -90
    lat_unq[-1] = 90
    long_unq[0] = -180
    long_unq[-1] = 180
    depth_unq = np.insert(depth_unq, 0, -100)

    ak135 = pd.read_csv(ak135_file, delim_whitespace=True, header=None, skiprows=1)

    depth = ak135.iloc[:, 0]
    velP = ak135.iloc[:, 1]
    vel_new = np.interp(depth_unq, depth, velP)
    vel_new = vel_new.round(4)

    # create global absolute velocity file
    output_df(long_unq, lat_unq, depth_unq, dvp, vel_new, teletomoDD_file_path, "glb_abs")

    # create global perturbation velocity file
    output_df(long_unq, lat_unq, depth_unq, dvp, vel_new, teletomoDD_file_path, "glb_perturb")


# reg function
def reg(ak135_file, mit_file, teletomoDD_file_path, lon_min, lon_max, lat_min, lat_max, depth_max):
    df_reg = pd.read_csv(mit_file, delim_whitespace=True)
    df_reg = df_reg[(df_reg["Lat"] >= lat_min) & (df_reg["Lat"] <= lat_max)]
    df_reg = df_reg[(df_reg["Long"] - 180 >= lon_min) & (df_reg["Long"] - 180 <= lon_max)]
    df_reg = df_reg[(df_reg["Depth"] <= depth_max)]

    lat_unq = df_reg["Lat"].unique()
    long_unq = (df_reg["Long"].unique() - 180).round(2)
    depth_unq = df_reg["Depth"].unique()
    dvp = df_reg["dVp"]

    depth_unq = np.insert(depth_unq, 0, -100)

    ak135 = pd.read_csv(ak135_file, delim_whitespace=True, header=None, skiprows=1)

    depth = ak135.iloc[:, 0]
    velP = ak135.iloc[:, 1]
    vel_new = np.interp(depth_unq, depth, velP)
    vel_new = vel_new.round(4)

    # create regional absolute velocity file
    output_df(long_unq, lat_unq, depth_unq, dvp, vel_new, teletomoDD_file_path, "reg_abs")

    # create regional perturbation velocity file
    output_df(long_unq, lat_unq, depth_unq, dvp, vel_new, teletomoDD_file_path, "reg_perturb")


# run main()
if __name__ == "__main__":

    # user specified working directory
    ak135_file = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/_v_list/ak135.txt"
    mit_file = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/_v_list/ggge1202-sup-0002-ds01.txt"
    output_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/05_TeletomoDD_files"

    # user specified study area data extent
    lon_min = -80
    lon_max = -55
    lat_min = 5
    lat_max = 25
    depth_max = 800

    glb(ak135_file, mit_file, output_path)
    reg(ak135_file, mit_file, output_path, lon_min, lon_max, lat_min, lat_max, depth_max)
