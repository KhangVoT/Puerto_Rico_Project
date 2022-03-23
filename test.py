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


# glb function
def glb(ak135_file, mit_file, teletomoDD_file_path):
    df_glb = pd.read_csv(mit_file, delim_whitespace=True)

    lat_unq = df_glb["Lat"].unique()
    long_unq = (df_glb["Long"].unique() - 180).round(2)
    depth_unq = df_glb["Depth"].unique()

    ak135 = pd.read_csv(ak135_file, delim_whitespace=True, header=None, skiprows=1)

    depth = ak135.iloc[:, 0]
    velP = ak135.iloc[:, 1]
    vel_new = np.interp(depth_unq, depth, velP)
    vel_new = vel_new.round(4)

    # create global perturbation velocity file
    with open(teletomoDD_file_path + "/glb_perturb_test.txt", "w") as outfile_perturb:
        outfile_perturb.write("0.1")
        outfile_perturb.write(" ")
        outfile_perturb.write(str(len(long_unq)))
        outfile_perturb.write(" ")
        outfile_perturb.write(str(len(lat_unq)))
        outfile_perturb.write(" ")
        outfile_perturb.write(str(len(depth_unq)))
        outfile_perturb.write("\n")
        for i in long_unq:
            outfile_perturb.write(str(i))
            outfile_perturb.write(" ")
        outfile_perturb.write("\n")
        for j in lat_unq:
            outfile_perturb.write(str(j))
            outfile_perturb.write(" ")
        outfile_perturb.write("\n")
        for k in depth_unq:
            outfile_perturb.write(str(k))
            outfile_perturb.write(" ")
        outfile_perturb.write("\n")

        m = 0
        n = 0
        for _ in depth_unq:
            for _ in long_unq:
                for _ in lat_unq:
                    # outfile_perturb.write(str(format(df_glb.iloc[m, 3], ".2f")))
                    print(vel_new[n] * (1 + df_glb.iloc[m, 3] / 100))
                    outfile_perturb.write(" ")
                    m += 1
                outfile_perturb.write("\n")
            n += 1


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

    glb(ak135_file, mit_file, output_path)
