# File Name: plot_cross_sections
# Author: Khang Vo
# Date Created: 10/10/2023
# Date Last Modified: 10/10/2023
# Python Version: 3.10

import os
import glob
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.interpolate import Rbf
from mpl_toolkits.basemap import Basemap


def plot_models(i, j, axes, df_control, df, lat):
    df = df[25 <= df["Depth"] <= 225].astype(float)
    # cut df_vp to desired depth
    df = df[df["Lat"] == lat].astype(float)

    # build a regular grid with n cells
    xi, zi = np.meshgrid(np.arange(df["Long"].min(), df["Long"].max(), 0.1),
                         np.arange(df["Depth"].min(), df["Depth"].max(), 0.1))

    # do radial basic function interpolation for Vp
    rbfi = Rbf(df["Long"], df["Depth"], df["Vp"], function="multiquadric", smooth=0.1)
    vi = rbfi(xi, zi)

    # create subplots

    # plot initial model
    # cl = axes[i, j].imshow(vi, origin="lower", cmap="turbo_r", vmin=min(df["Vp"]), vmax=max(df["Vp"]), aspect="auto",
    #                        alpha=1, extent=[df["Long"].min(), df["Long"].max(), df["Depth"].min(), df["Depth"].max()])
    cl = axes[i, j].scatter(df["Long"], df["Depth"], c=df["Vp"],  marker="s", s=10, cmap="turbo_r", vmin=min(df["Vp"]), vmax=max(df["Vp"]), alpha=1)
    # axes[i, j].tricontour(df["Long"], df["Depth"], df["Dws"], levels=[10000], linewidths=1, colors="white")

    axes[i, j].set_title("Latitude = " + str(lat) + " $^\circ$N")
    axes[i, j].set_xlabel("Longitude ($^\circ$W)")
    axes[i, j].set_ylabel("Depth (km)")

    cb = plt.colorbar(cl, ax=axes[i, j], shrink=1)
    cb.set_label("Vp (km/s)")

    axes[i, j].invert_yaxis()


def main(file_list, lat_list, lon_min, lon_max, lat_min, lat_max):
    # create main plot
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(19, 9))
    # fig.suptitle("Velocity Model (Perturbation)", fontsize=18, y=0.95)

    # create control file to set global color bar
    df_control_list = []
    for file in file_list:
        if "MOD" in file:
            df_control = pd.read_csv(file, delim_whitespace=True, dtype=object, usecols=range(5))
            df_control.columns = ["Long", "Lat", "Depth", "Num1", "Vp"]
            df_control = df_control.apply(pd.to_numeric, errors="coerce").dropna()
        elif "vel" in file:
            df_vel = pd.read_csv(file, delim_whitespace=True, dtype=object, usecols=range(6))
            df_vel.columns = ["Long", "Lat", "Depth", "Num1", "Vp", "Dws"]
            df_vel = df_vel.apply(pd.to_numeric, errors="coerce").dropna()

    # loop through each depth to add to subplots
    for j, lat in enumerate(lat_list):
        if j <= 2:
            i = 0
        else:
            j -= 3
            i = 1
        plot_models(i, j, axes, df_control, df_vel, lat)

    plt.savefig("/Users/khangvo/Downloads/cross_section.jpeg", bbox_inches="tight")

    plt.show()


# run main()
if __name__ == "__main__":
    root = "/Users/khangvo/Downloads/"

    file_list = glob.glob(root + "*MOD.*") + sorted(glob.glob(root + "*.vel.*"))

    lat_list = [6.0, 9.0, 12.0, 15.0, 18.0, 21.0]

    # user specified study area data extent
    lon_min = -80
    lon_max = -55
    lat_min = 5
    lat_max = 25
    depth_min = 10
    depth_max = 250

    main(file_list, lat_list, lon_min, lon_max, lat_min, lat_max)
