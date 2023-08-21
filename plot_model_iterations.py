# File Name: plot_models
# Author: Khang Vo
# Date Created: 8/10/2022
# Date Last Modified: 10/6/2022
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


def plot_models(max_i, i, j, axes, df_control, df, depth):
    # cut df_vp to desired depth
    df = df[df["Depth"] == str(depth)].astype(float)

    # build a regular grid with n cells
    xi, yi = np.meshgrid(np.arange(df["Long"].min(), df["Long"].max(), 0.1),
                         np.arange(df["Lat"].min(), df["Lat"].max(), 0.1))

    # do radial basic function interpolation for Vp
    rbfi = Rbf(df["Long"], df["Lat"], df["Vp"], function="multiquadric", smooth=0.1)
    vi = rbfi(xi, yi)

    # cut df_control to desired depth
    df_control = df_control[df_control["Depth"] == str(depth)].astype(float)

    # create subplots

    # plot initial model
    m = Basemap(resolution="h", llcrnrlat=df["Lat"].min(), llcrnrlon=df["Long"].min(),
                urcrnrlat=df["Lat"].max(), urcrnrlon=df["Long"].max(), ax=axes[j, i], suppress_ticks=False)
    m.drawcoastlines(color="black")
    m.drawparallels(np.arange(-90, 90, 10), labels=[1, 0, 0, 0], linewidth=0.001, xoffset=0.5, yoffset=0.5)
    m.drawmeridians(np.arange(0, 360, 10), labels=[0, 0, 0, 1], linewidth=0.001, xoffset=0.5, yoffset=0.5)
    cl = axes[j, i].imshow(vi, origin="lower", cmap="turbo", vmin=min(df_control["Vp"]), vmax=max(df_control["Vp"]), alpha=1,
                           extent=[df["Long"].min(), df["Long"].max(), df["Lat"].min(), df["Lat"].max()])

    if i == 0:
        axes[j, i].set_title("(Initial) " + " Depth = " + str(depth) + " km")
    elif i > 0:
        axes[j, i].set_title("(N" + str(i) + ") Depth = " + str(depth) + " km")

    axes[j, i].xaxis.set_major_locator(ticker.MultipleLocator(10))
    axes[j, i].yaxis.set_major_locator(ticker.MultipleLocator(10))
    axes[j, i].tick_params(labelleft=False, labelright=False, labeltop=False, labelbottom=False)

    if i == max_i:
        cb = plt.colorbar(cl, ax=axes[j, i], shrink=0.685)
        cb.set_label("Vp (km/s)")


def main(file_list, depth_list):
    # create main plot
    fig, axes = plt.subplots(nrows=len(depth_list), ncols=len(file_list), figsize=(19, 9), constrained_layout=True)
    fig.suptitle("Velocity Models (Perturbation)", fontsize=18, y=0.995)

    # create control file to set global color bar
    df_control_list = []
    for file in file_list:
        df_control = pd.read_csv(file, delim_whitespace=True, dtype=object, usecols=range(5))
        df_control.columns = ["Long", "Lat", "Depth", "Num1", "Vp"]
        df_control = df_control.drop(["Num1"], axis=1)
        df_control_list.append(df_control)
    df_control = pd.concat(df_control_list, ignore_index=True)

    # read individual files in file list
    for i, file in enumerate(file_list):
        df = pd.read_csv(file, delim_whitespace=True, dtype=object, usecols=range(5))
        df.columns = ["Long", "Lat", "Depth", "Num1", "Vp"]
        df = df.drop(["Num1"], axis=1)

        # loop through each depth to add to subplots
        for j, depth in enumerate(depth_list):
            plot_models(len(file_list) - 1, i, j, axes, df_control, df, depth)

    plt.savefig("/Users/khangvo/Downloads/Velocity_Models_perturb.jpeg")

    plt.show()


# run main()
if __name__ == "__main__":

    root = "/Users/khangvo/Downloads/"

    file_list = glob.glob(root + "*MOD.*") + sorted(glob.glob(root + "*.vel.*"))

    depth_list = [12.0, 40.0, 75.0]

    main(file_list, depth_list)
