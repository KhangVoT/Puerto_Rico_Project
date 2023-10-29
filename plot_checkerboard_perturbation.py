# File Name: plot_checkerboard_perturbations
# Author: Khang Vo
# Date Created: 2/15/2023
# Date Last Modified: 10/12/2023
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


def plot_models(ax, df, depth):
    # cut df_vp to desired depth
    df = df[df["Depth"] == depth].astype(float)

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
                urcrnrlat=df["Lat"].max(), urcrnrlon=df["Long"].max(), ax=ax, suppress_ticks=False)
    m.drawcoastlines(color="black")
    m.drawparallels(np.arange(-90, 90, 10), labels=[1, 0, 0, 0], linewidth=0.001, xoffset=0.5, yoffset=0.5)
    m.drawmeridians(np.arange(0, 360, 10), labels=[0, 0, 0, 1], linewidth=0.001, xoffset=0.5, yoffset=0.5)
    cl = ax.imshow(vi, origin="lower", cmap="seismic_r", vmin=-10, vmax=10, alpha=1,
                           extent=[df["Long"].min(), df["Long"].max(), df["Lat"].min(), df["Lat"].max()])
    ax.tricontour(df["Long"], df["Lat"], df["Dws"], levels=[1000], linewidths=1, colors="lime")

    ax.set_title("Depth = " + str(depth) + " km")

    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.tick_params(labelleft=False, labelright=False, labeltop=False, labelbottom=False)

    cb = plt.colorbar(cl, ax=ax, shrink=0.88)
    cb.set_label("dVp %")


def main(file_list, depth_list, lon_min, lon_max, lat_min, lat_max):
    # create main plot
    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(24, 12))
    # fig.suptitle("Checkerboard Test (D2 = 5 +-10%)", fontsize=18, y=0.95)

    for file in file_list:
        if "MOD" in file:
            df_mod = pd.read_csv(file, delim_whitespace=True, dtype=object, usecols=range(5))
            df_mod.columns = ["Long", "Lat", "Depth", "Num1", "Vp"]
        elif "vel" in file:
            df_vel = pd.read_csv(file, delim_whitespace=True, dtype=object, usecols=range(6))
            df_vel.columns = ["Long", "Lat", "Depth", "Num1", "Vp", "Dws"]

    df_merged = pd.merge(df_mod, df_vel, how="left", on=["Long", "Lat", "Depth"])

    df_merged = df_merged[0:df_merged[df_merged["Long"] == ">"].index[0]].apply(pd.to_numeric, errors="coerce").dropna()

    df_merged = df_merged[(df_merged["Long"].astype(float) >= lon_min) & (df_merged["Long"].astype(float) <= lon_max) &
                          (df_merged["Lat"].astype(float) >= lat_min) & (df_merged["Lat"].astype(float) <= lat_max)]

    # loop through each depth to add to subplots
    for i, ax in enumerate(fig.axes):
        depth = depth_list[i]
        plot_models(ax, df_merged, depth)

    plt.savefig("/Users/khangvo/Downloads/Checkerboard_Perturbation.jpeg", bbox_inches="tight")

    plt.show()


# run main()
if __name__ == "__main__":

    root = "/Users/khangvo/Downloads/"

    file_list = glob.glob(root + "*MOD.*") + sorted(glob.glob(root + "*.vel.*"))

    # depth_list = [12.0, 40.0, 75.0, 120.0, 185.0, 225.0]
    depth_list = [25.0, 40.0, 55.0, 75.0, 95.0, 120.0, 150.0, 185.0, 225.0]

    # user specified study area data extent
    lon_min = -80
    lon_max = -55
    lat_min = 5
    lat_max = 25
    depth_min = 10
    depth_max = 250

    main(file_list, depth_list, lon_min, lon_max, lat_min, lat_max)
