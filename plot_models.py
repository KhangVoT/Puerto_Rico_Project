# File Name: plot_models
# Author: Khang Vo
# Date Created: 8/21/2023
# Date Last Modified: 8/25/2023
# Python Version: 3.9

import os
import glob
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.interpolate import Rbf
from mpl_toolkits.basemap import Basemap


def plot_models(i, j, axes, df_control, df, depth):
    # cut df_vp to desired depth
    df = df[df["Depth"] == depth].astype(float)

    # build a regular grid with n cells
    xi, yi = np.meshgrid(np.arange(df["Long"].min(), df["Long"].max(), 0.1),
                         np.arange(df["Lat"].min(), df["Lat"].max(), 0.1))

    # do radial basic function interpolation for Vp
    rbfi = Rbf(df["Long"], df["Lat"], df["Vp"], function="multiquadric", smooth=0.1)
    vi = rbfi(xi, yi)

    # cut df_control to desired depth
    df_control = df_control[df_control["Depth"] == depth].astype(float)

    # create subplots

    # plot initial model
    m = Basemap(resolution="h", llcrnrlat=df["Lat"].min(), llcrnrlon=df["Long"].min(),
                urcrnrlat=df["Lat"].max(), urcrnrlon=df["Long"].max(), ax=axes[i, j], suppress_ticks=False)
    m.drawcoastlines(color="black")
    m.drawparallels(np.arange(-90, 90, 10), labels=[1, 0, 0, 0], linewidth=0.001, xoffset=0.5, yoffset=0.5)
    m.drawmeridians(np.arange(0, 360, 10), labels=[0, 0, 0, 1], linewidth=0.001, xoffset=0.5, yoffset=0.5)
    cl = axes[i, j].imshow(vi, origin="lower", cmap="turbo", vmin=min(df["Vp"]), vmax=max(df["Vp"]), alpha=1,
                           extent=[df["Long"].min(), df["Long"].max(), df["Lat"].min(), df["Lat"].max()])

    axes[i, j].set_title("Depth = " + str(depth) + " km")

    axes[i, j].xaxis.set_major_locator(ticker.MultipleLocator(10))
    axes[i, j].yaxis.set_major_locator(ticker.MultipleLocator(10))
    axes[i, j].tick_params(labelleft=False, labelright=False, labeltop=False, labelbottom=False)

    cb = plt.colorbar(cl, ax=axes[i, j], shrink=0.88)
    cb.set_label("Vp (km/s)")


def main(file_list, depth_list, lon_min, lon_max, lat_min, lat_max):
    # create main plot
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(19, 9))
    fig.suptitle("Velocity Model (Perturbation)", fontsize=18, y=0.95)

    # create control file to set global color bar
    df_control_list = []
    for file in file_list:
        if "MOD" in file:
            df_control = pd.read_csv(file, delim_whitespace=True, dtype=object, usecols=range(5))
            df_control.columns = ["Long", "Lat", "Depth", "Num1", "Vp"]
            df_control = df_control.apply(pd.to_numeric, errors="coerce").dropna()
        elif "vel" in file:
            df_vel = pd.read_csv(file, delim_whitespace=True, dtype=object, usecols=range(5))
            df_vel.columns = ["Long", "Lat", "Depth", "Num1", "Vp"]
            df_vel = df_vel.apply(pd.to_numeric, errors="coerce").dropna()

    # loop through each depth to add to subplots
    for j, depth in enumerate(depth_list):
        if j <= 2:
            i = 0
        else:
            j -= 3
            i = 1
        plot_models(i, j, axes, df_control, df_vel, depth)

    plt.savefig("/Users/khangvo/Downloads/Velocity_Model_perturb.jpeg", bbox_inches="tight")

    plt.show()


# run main()
if __name__ == "__main__":

    root = "/Users/khangvo/Downloads/"

    file_list = glob.glob(root + "*MOD.*") + sorted(glob.glob(root + "*.vel.*"))

    depth_list = [12.0, 40.0, 75.0, 120.0, 185.0, 225.0]
    # depth_list = [12.0, 25.0, 40.0, 55.0, 75.0, 95.0]

    # user specified study area data extent
    lon_min = -80
    lon_max = -55
    lat_min = 5
    lat_max = 25
    depth_min = 10
    depth_max = 250

    main(file_list, depth_list, lon_min, lon_max, lat_min, lat_max)
