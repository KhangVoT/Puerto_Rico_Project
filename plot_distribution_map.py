# File Name: plot_distribution_maps
# Author: Khang Vo
# Date Created: 9/21/2022
# Date Last Modified: 9/21/2022
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


def plot_reg(df, ax, n):

    plt.subplots()

    # m = Basemap(projection="lcc", resolution="h", lat_0=15, lon_0=-67.5, width=1E6, height=1.2E6)
    m = Basemap(resolution="h", llcrnrlat=df["glat"].min(), llcrnrlon=df["glon"].min(),
                urcrnrlat=df["glat"].max(), urcrnrlon=df["glon"].max())
    m.drawparallels(np.arange(-90, 90, 10), labels=[1, 0, 0, 0], linewidth=0, xoffset=0.5, yoffset=0.5)
    m.drawmeridians(np.arange(0, 360, 10), labels=[0, 0, 0, 1], linewidth=0, xoffset=0.5, yoffset=0.5)
    m.shadedrelief(scale=0.5)
    m.drawcoastlines(color="lightgray")
    m.drawcountries(color="lightgray")
    m.drawstates(color="lightgray")

    m.scatter(df["glon"], df["glat"], latlon=True, c=df["depth"], s=df["mb"], cmap="jet", alpha=0.5)

    plt.colorbar(label="Depth (km)")
    plt.clim(min(df["depth"]), max(df["depth"]))

    for a in [1, 5, 9]:
        plt.scatter([], [], c="k", alpha=0.5, s=a,
                    label="Magnitude: " + str(a))
    plt.legend(scatterpoints=1, frameon=True,
               labelspacing=1, loc="upper right")

    plt.show()


def plot_glb(df, ax, n):

    plt.subplots()

    m = Basemap(projection="ortho", resolution=None, lat_0=15, lon_0=-67.5)
    m.shadedrelief(scale=0.5)

    m.scatter(df["glon"], df["glat"], latlon=True, c=df["depth"], s=df["mb"], cmap="jet", alpha=0.5)

    plt.colorbar(label="Depth (km)")
    plt.clim(min(df["depth"]), max(df["depth"]))

    for a in [1, 5, 9]:
        plt.scatter([], [], c="k", alpha=0.5, s=a,
                    label="Magnitude: " + str(a))
    plt.legend(scatterpoints=1, frameon=True,
               labelspacing=1, loc="upper right")

    plt.show()


def main(file):
    # create main plot
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(19, 9), constrained_layout=True)
    fig.suptitle("Distribution Map", fontsize=18, y=0.995)

    df = pd.read_csv(file, delim_whitespace=True)
    df.columns = ["date", "time", "glat", "glon", "depth", "mb", "n1", "n2", "n3", "ievt", "n4"]
    df = df.drop(["n1", "n2", "n3", "n4"], axis=1)
    df = df.astype(float)

    plot_glb(df, ax, 0)

    # user specified study area data extent
    lon_min = -80
    lon_max = -55
    lat_min = 5
    lat_max = 25

    df_zoned = df[(df["glon"].astype(float) >= lon_min) & (df["glon"].astype(float) <= lon_max) &
                  (df["glat"].astype(float) >= lat_min) & (df["glat"].astype(float) <= lat_max)]

    # plot_reg(df_zoned, ax, 1)

    # plt.show()


# run main()
if __name__ == "__main__":

    file = "/Users/khangvo/Python_Projects/Puerto_Rico_Project_Refinement/files/05_TeletomoDD_files/event.txt"

    main(file)
