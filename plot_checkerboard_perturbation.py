# File Name: plot_checkerboard_perturbations
# Author: Khang Vo
# Date Created: 2/15/2023
# Date Last Modified: 3/11/2023
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


def plot_models(j, axes, df, depth):
    # cut df_vp to desired depth
    df = df[df["Depth"] == str(depth)].astype(float)

    df["Per"] = ((df["Vp_y"] - df["Vp_x"]) / df["Vp_x"]) * 100

    # build a regular grid with n cells
    xi, yi = np.meshgrid(np.arange(df["Long"].min(), df["Long"].max(), 0.1),
                         np.arange(df["Lat"].min(), df["Lat"].max(), 0.1))

    # do radial basic function interpolation for Vp
    rbfi = Rbf(df["Long"], df["Lat"], df["Per"], function="multiquadric", smooth=0.1)
    vi = rbfi(xi, yi)

    # create subplots

    # plot initial model
    m = Basemap(resolution="h", llcrnrlat=df["Lat"].min(), llcrnrlon=df["Long"].min(),
                urcrnrlat=df["Lat"].max(), urcrnrlon=df["Long"].max(), ax=axes[j], suppress_ticks=False)
    m.drawcoastlines(color="black")
    m.drawparallels(np.arange(-90, 90, 10), labels=[1, 0, 0, 0], linewidth=0.001, xoffset=0.5, yoffset=0.5)
    m.drawmeridians(np.arange(0, 360, 10), labels=[0, 0, 0, 1], linewidth=0.001, xoffset=0.5, yoffset=0.5)
    cl = axes[j].imshow(vi, origin="lower", cmap="seismic", vmin=-10, vmax=10, alpha=1,
                           extent=[df["Long"].min(), df["Long"].max(), df["Lat"].min(), df["Lat"].max()])

    axes[j].set_title("Depth = " + str(depth) + " km")

    axes[j].xaxis.set_major_locator(ticker.MultipleLocator(10))
    axes[j].yaxis.set_major_locator(ticker.MultipleLocator(10))
    axes[j].tick_params(labelleft=False, labelright=False, labeltop=False, labelbottom=False)

    cb = plt.colorbar(cl, ax=axes[j], shrink=0.97)
    cb.set_label("dVp %")


def main(file_list, depth_list):
    # create main plot
    fig, axes = plt.subplots(nrows=len(depth_list), ncols=1, figsize=(4, 9))
    fig.suptitle("Checkerboard Test")

    for file in file_list:
        if "MOD" in file:
            df_mod = pd.read_csv(file, delim_whitespace=True, dtype=object, usecols=range(5))
            df_mod.columns = ["Long", "Lat", "Depth", "Num1", "Vp"]
        elif "vel" in file:
            df_vel = pd.read_csv(file, delim_whitespace=True, dtype=object, usecols=range(5))
            df_vel.columns = ["Long", "Lat", "Depth", "Num1", "Vp"]

    df_merged = pd.merge(df_mod, df_vel, how="left", on=["Long", "Lat", "Depth"])

    # read individual files in file list
    for j, depth in enumerate(depth_list):
        plot_models(j, axes, df_merged, depth)

    plt.savefig("/Users/khangvo/Downloads/velocity_models_abs.jpeg")

    plt.show()


# run main()
if __name__ == "__main__":

    root = "/Users/khangvo/Downloads/"

    file_list = glob.glob(root + "*MOD.*") + sorted(glob.glob(root + "*.vel.*"))

    depth_list = [12.0, 40.0, 75.0]
    # depth_list = [120.0, 185.0, 225.0]

    main(file_list, depth_list)
