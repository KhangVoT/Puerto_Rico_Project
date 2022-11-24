# File Name: create_velocity_files
# Author: Khang Vo
# Date Created: 3/6/2022
# Date Last Modified: 8/20/2022
# Python Version: 3.9

import os
import glob
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interpn


# function to create plot friendly files:
def plot_friendly(df, teletomoDD_file_path, file_name):

    df = df.sort_values(by=["Depth", "Long", "Lat"]).reset_index(drop=True)

    df = df.applymap(lambda x: format(x, ".2f"))

    if "_abs" in file_name:
        headers = ["Lat", "Long", "Depth", "Vel"]
        df.to_csv(teletomoDD_file_path + "/" + file_name + "_plot_friendly.txt", columns=headers, sep="\t", index=False)
    elif "_perturb" in file_name:
        headers = ["Lat", "Long", "Depth", "Vel_Perturb"]
        df.to_csv(teletomoDD_file_path + "/" + file_name + "_plot_friendly.txt", columns=headers, sep="\t", index=False)


# function to write DataFrame to text file
def output_df(df, teletomoDD_file_path, file_name):

    long_unq = df["Long"].unique()
    lat_unq = df["Lat"].unique()
    depth_unq = df["Depth"].unique()

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
            outfile.write(str(format(i, ".2f")))
            outfile.write(" ")
        outfile.write("\n")
        for j in lat_unq:
            outfile.write(str(format(j, ".2f")))
            outfile.write(" ")
        outfile.write("\n")
        for k in depth_unq:
            outfile.write(str(format(k, ".1f")))
            outfile.write(" ")
        outfile.write("\n")

        if "_abs" in file_name:
            m = 0
            for _ in depth_unq:
                for _ in lat_unq:
                    for _ in long_unq:
                        outfile.write(str(format(df.loc[m, "Vel"], ".2f")))
                        outfile.write(" ")
                        m += 1
                    outfile.write("\n")
        elif "_perturb" in file_name:
            n = 0
            for _ in depth_unq:
                for _ in lat_unq:
                    for _ in long_unq:
                        outfile.write(str(format(df.loc[n, "Vel_Perturb"], ".2f")))
                        outfile.write(" ")
                        n += 1
                    outfile.write("\n")


# function to calculate global velocity model
def glb(ak135_file, interp_file_glb, teletomoDD_file_path):
    df_glb = pd.read_csv(interp_file_glb, delim_whitespace=True)
    df_glb["Long"] = (df_glb["Long"] - 180).round(2)

    df_glb = df_glb.sort_values(by=["Depth", "Lat", "Long"]).reset_index(drop=True)

    df_upper = df_glb[(df_glb["Depth"] == min(df_glb["Depth"]))].copy()
    df_upper.loc[:, "Depth"] = -100
    df_upper.loc[:, "dVp"] = 0

    df_glb = pd.concat([df_upper, df_glb]).reset_index(drop=True)

    ak135 = pd.read_csv(ak135_file, delim_whitespace=True, header=None, skiprows=1)

    depth = ak135.iloc[:, 0]
    velP = ak135.iloc[:, 1]
    df_glb["Vel"] = np.interp(df_glb["Depth"], depth, velP)
    df_glb["Vel_Perturb"] = df_glb["Vel"] * (1 + df_glb["dVp"] / 100)

    # create global absolute velocity file
    output_df(df_glb, teletomoDD_file_path, "glb_abs")

    # create global perturbation velocity file
    output_df(df_glb, teletomoDD_file_path, "glb_perturb")

    # create plot friendly global absolute velocity file
    plot_friendly(df_glb, teletomoDD_file_path, "glb_abs")

    # create plot friendly global perturbation velocity file
    plot_friendly(df_glb, teletomoDD_file_path, "glb_perturb")


# function to calculate regional velocity model
def reg(ak135_file, interp_file_reg, teletomoDD_file_path):
    df_reg = pd.read_csv(interp_file_reg, delim_whitespace=True)
    df_reg["Long"] = (df_reg["Long"] - 180).round(2)

    df_reg = df_reg.sort_values(by=["Depth", "Lat", "Long"]).reset_index(drop=True)

    df_upper = df_reg[(df_reg["Depth"] == min(df_reg["Depth"]))].copy()
    df_upper.loc[:, "Depth"] = -1
    df_upper.loc[:, "dVp"] = 0

    df_reg = pd.concat([df_upper, df_reg]).reset_index(drop=True)

    ak135 = pd.read_csv(ak135_file, delim_whitespace=True, header=None, skiprows=1)

    depth = ak135.iloc[:, 0]
    velP = ak135.iloc[:, 1]
    df_reg["Vel"] = np.interp(df_reg["Depth"], depth, velP)
    df_reg["Vel_Perturb"] = df_reg["Vel"] * (1 + df_reg["dVp"] / 100)

    # create regional absolute velocity file
    output_df(df_reg, teletomoDD_file_path, "reg_abs")

    # create regional perturbation velocity file
    output_df(df_reg, teletomoDD_file_path, "reg_perturb")

    # create plot friendly regional absolute velocity file
    plot_friendly(df_reg, teletomoDD_file_path, "reg_abs")

    # create plot friendly regional perturbation velocity file
    plot_friendly(df_reg, teletomoDD_file_path, "reg_perturb")


# function to create 3D velocity model for interpolation
def create_model(mit_file):
    df = pd.read_csv(mit_file, delim_whitespace=True)

    # extract the list of coordinates
    xs = np.array(df["Long"].to_list())
    ys = np.array(df["Lat"].to_list())
    zs = np.array(df["Depth"].to_list())
    # extract the associated velocity values
    vs = np.array(df["dVp"].to_list())

    px, ix = np.unique(xs, return_inverse=True)
    py, iy = np.unique(ys, return_inverse=True)
    pz, iz = np.unique(zs, return_inverse=True)

    points = (px, py, pz)

    values = np.empty_like(vs, shape=(px.size, py.size, pz.size))
    values[ix, iy, iz] = vs

    return points, values, df["Long"], df["Lat"], df["Depth"]


# function to interpolate velocities
def interp(mit_file, points, values, long, lat, depth, long_step, lat_step, depth_step, suffix):

    # set desired coordinates
    long_request = np.arange(np.floor(min(long)), np.ceil(max(long)) + long_step, long_step)
    lat_request = np.arange(np.floor(min(lat)), np.ceil(max(lat)) + lat_step, lat_step)
    depth_request = np.arange(min(depth), max(depth) + depth_step, depth_step)

    if ".txt" in mit_file:
        with open(mit_file, "r") as infile:
            header = next(infile)
            with open(mit_file[0:-4] + "_interp_" + suffix + ".txt", "w") as outfile:
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

                            dvp_request = np.array([long, lat, depth])
                            dvp = interpn(points, values, dvp_request, method="linear", bounds_error=False,
                                          fill_value=None)
                            outfile.write(str(format(float(dvp), ".2f")))
                            outfile.write("\n")

    interp_file = mit_file[0:-4] + "_interp_" + suffix + ".txt"
    return interp_file


def main(ak135_file, mit_file, teletomoDD_file_path, lon_min, lon_max, lat_min, lat_max, depth_min, depth_max, long_step_glb, lat_step_glb, depth_step_glb, long_step_reg, lat_step_reg, depth_step_reg):

    points, values, long_glb, lat_glb, depth_glb = create_model(mit_file)

    lon_reg = [lon_min + 180, lon_max + 180]
    lat_reg = [lat_min, lat_max]
    depth_reg = [depth_min, depth_max]

    interp_file_glb = interp(mit_file, points, values, long_glb, lat_glb, depth_glb, long_step_glb, lat_step_glb, depth_step_glb, "abs")
    glb(ak135_file, interp_file_glb, teletomoDD_file_path)

    interp_file_reg = interp(mit_file, points, values, lon_reg, lat_reg, depth_reg, long_step_reg, lat_step_reg, depth_step_reg, "reg")
    reg(ak135_file, interp_file_reg, teletomoDD_file_path)


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
    depth_min = 0
    depth_max = 800

    # user specified steps for coordinate interpolation
    long_step_glb = 5
    lat_step_glb = 5
    depth_step_glb = 200
    long_step_reg = 0.5
    lat_step_reg = 0.5
    depth_step_reg = 25

    main(ak135_file, mit_file, output_path, lon_min, lon_max, lat_min, lat_max, depth_min, depth_max, long_step_glb, lat_step_glb, depth_step_glb, long_step_reg, lat_step_reg, depth_step_reg)
