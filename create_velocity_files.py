# File Name: create_velocity_files
# Author: Khang Vo
# Date Created: 3/6/2022
# Date Last Modified: 6/17/2022
# Python Version: 3.9

import os
import glob
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interpn


# function to create plot friendly files:
def plot_friendly(long_unq, lat_unq, depth_unq, dvp, vel_new, teletomoDD_file_path, file_name):
    with open(teletomoDD_file_path + "/" + file_name + "_plot_friendly.txt", "w") as outfile:
        outfile.write("Lat")
        outfile.write("\t")
        outfile.write("Long")
        outfile.write("\t")
        outfile.write("Depth")
        outfile.write("\t")
        outfile.write("dVp")
        outfile.write("\n")

        if "_abs" in file_name:
            m = 0
            for i in depth_unq:
                for j in long_unq:
                    for k in lat_unq:
                        outfile.write(str(format(k, ".2f")))
                        outfile.write("\t")
                        outfile.write(str(format(j, ".2f")))
                        outfile.write("\t")
                        outfile.write(str(format(i, ".1f")))
                        outfile.write("\t")
                        outfile.write(str(format(vel_new[m], ".2f")))
                        outfile.write("\n")
                m += 1
        elif "_perturb" in file_name:
            m = 0
            n = 0
            for i in depth_unq:
                for j in long_unq:
                    for k in lat_unq:
                        if i < 0:
                            outfile.write(str(format(k, ".2f")))
                            outfile.write("\t")
                            outfile.write(str(format(j, ".2f")))
                            outfile.write("\t")
                            outfile.write(str(format(i, ".1f")))
                            outfile.write("\t")
                            outfile.write(str(format(vel_new[n], ".2f")))
                            outfile.write("\n")
                        else:
                            outfile.write(str(format(k, ".2f")))
                            outfile.write("\t")
                            outfile.write(str(format(j, ".2f")))
                            outfile.write("\t")
                            outfile.write(str(format(i, ".1f")))
                            outfile.write("\t")
                            outfile.write(str(format((vel_new[n] * (1 + dvp.iloc[m] / 100)), ".2f")))
                            outfile.write("\n")
                            m += 1
                n += 1


# function to write DataFrame to text file
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


# function to calculate global velocity model
def glb(ak135_file, mit_file, teletomoDD_file_path):
    df_glb = pd.read_csv(mit_file, delim_whitespace=True)

    lat_unq = df_glb["Lat"].unique()
    long_unq = (df_glb["Long"].unique() - 180).round(2)
    depth_unq = df_glb["Depth"].unique()
    dvp = df_glb["dVp"]

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

    # create plot friendly global absolute velocity file
    plot_friendly(long_unq, lat_unq, depth_unq, dvp, vel_new, teletomoDD_file_path, "glb_abs")

    # create plot friendly global perturbation velocity file
    plot_friendly(long_unq, lat_unq, depth_unq, dvp, vel_new, teletomoDD_file_path, "glb_perturb")


# function to calculate regional velocity model
def reg(ak135_file, mit_file, teletomoDD_file_path, lon_min, lon_max, lat_min, lat_max, depth_max):
    df_reg = pd.read_csv(mit_file, delim_whitespace=True)
    df_reg = df_reg[(df_reg["Lat"] >= lat_min) & (df_reg["Lat"] <= lat_max)]
    df_reg = df_reg[(df_reg["Long"] - 180 >= lon_min) & (df_reg["Long"] - 180 <= lon_max)]
    df_reg = df_reg[(df_reg["Depth"] <= depth_max)]

    lat_unq = df_reg["Lat"].unique()
    long_unq = (df_reg["Long"].unique() - 180).round(2)
    depth_unq = df_reg["Depth"].unique()
    dvp = df_reg["dVp"]

    depth_unq = np.insert(depth_unq, 0, -1)

    ak135 = pd.read_csv(ak135_file, delim_whitespace=True, header=None, skiprows=1)

    depth = ak135.iloc[:, 0]
    velP = ak135.iloc[:, 1]
    vel_new = np.interp(depth_unq, depth, velP)
    vel_new = vel_new.round(4)

    # create regional absolute velocity file
    output_df(long_unq, lat_unq, depth_unq, dvp, vel_new, teletomoDD_file_path, "reg_abs")

    # create regional perturbation velocity file
    output_df(long_unq, lat_unq, depth_unq, dvp, vel_new, teletomoDD_file_path, "reg_perturb")

    # create plot friendly regional absolute velocity file
    plot_friendly(long_unq, lat_unq, depth_unq, dvp, vel_new, teletomoDD_file_path, "reg_abs")

    # create plot friendly regional perturbation velocity file
    plot_friendly(long_unq, lat_unq, depth_unq, dvp, vel_new, teletomoDD_file_path, "reg_perturb")


# function to create 3D velocity model for interpolation
def create_model(mit_file):
    df = pd.read_csv(mit_file, delim_whitespace=True)

    # extract the list of coordinates
    xs = np.array(df["Lat"].to_list())
    ys = np.array(df["Long"].to_list())
    zs = np.array(df["Depth"].to_list())
    # extract the associated velocity values
    vs = np.array(df["dVp"].to_list())

    px, ix = np.unique(xs, return_inverse=True)
    py, iy = np.unique(ys, return_inverse=True)
    pz, iz = np.unique(zs, return_inverse=True)

    points = (px, py, pz)

    values = np.empty_like(vs, shape=(px.size, py.size, pz.size))
    values[ix, iy, iz] = vs

    return points, values, df["Lat"], df["Long"], df["Depth"]


# function to interpolate velocities
def interp(mit_file, points, values, lat, long, depth, lat_step, long_step, depth_step):

    # set desired coordinates
    lat_request = np.arange(np.floor(min(lat)), np.ceil(max(lat)) + lat_step, lat_step)
    long_request = np.arange(np.floor(min(long)), np.ceil(max(long)) + long_step, long_step)
    depth_request = np.arange(0, np.ceil(max(depth)), depth_step)
    depth_request = np.insert(depth_request, len(depth_request), 6371.0)

    if ".txt" in mit_file:
        with open(mit_file, "r") as infile:
            header = next(infile)
            with open(mit_file[0:-4] + "_interp.txt", "w") as outfile:
                outfile.write(header)
                for depth in depth_request:
                    for long in long_request:
                        for lat in lat_request:
                            outfile.write(str(format(lat, ".2f")))
                            outfile.write("\t")
                            outfile.write(str(format(long, ".2f")))
                            outfile.write("\t")
                            outfile.write(str(format(depth, ".1f")))
                            outfile.write("\t")

                            dvp_request = np.array([lat, long, depth])
                            dvp = interpn(points, values, dvp_request, method="linear", bounds_error=False,
                                          fill_value=None)
                            outfile.write(str(format(float(dvp), ".2f")))
                            outfile.write("\n")

    interp_file = mit_file[0:-4] + "_interp.txt"
    return interp_file


def main(ak135_file, mit_file, output_path, lon_min, lon_max, lat_min, lat_max, depth_max, lat_step, long_step, depth_step):

    points, values, lat, long, depth = create_model(mit_file)
    interp_file = interp(mit_file, points, values, lat, long, depth, lat_step, long_step, depth_step)

    glb(ak135_file, interp_file, output_path)
    reg(ak135_file, interp_file, output_path, lon_min, lon_max, lat_min, lat_max, depth_max)


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
    depth_max = 1000

    # user specified steps for coordinate interpolation
    lat_step = 5
    long_step = 5
    depth_step = 200

    main(ak135_file, mit_file, output_path, lon_min, lon_max, lat_min, lat_max, depth_max, lat_step, long_step, depth_step)
