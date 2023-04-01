# File Name: plot_distribution_slices
# Author: Khang Vo
# Date Created: 3/27/2023
# Date Last Modified: 3/27/2023
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


def plot_models(i, j, axes, df_events, depth, depth_list):
    depth_list = [0] + depth_list + [250]

    index = depth_list.index(depth)

    # cut df_vp to desired depth
    df_events = df_events[(df_events["depth"] >= ((depth_list[index - 1] + depth_list[index]) / 2)) &
                          (df_events["depth"] <= ((depth_list[index] + depth_list[index + 1]) / 2))]

    # create subplots

    # plot initial model
    m = Basemap(resolution="l", llcrnrlat=lat_min, llcrnrlon=lon_min, urcrnrlat=lat_max, urcrnrlon=lon_max,
                ax=axes[i, j], suppress_ticks=False)
    m.drawcoastlines(color="black")
    m.drawparallels(np.arange(-90, 90, 10), labels=[1, 0, 0, 0], linewidth=0.001, xoffset=0.5, yoffset=0.5)
    m.drawmeridians(np.arange(0, 360, 10), labels=[0, 0, 0, 1], linewidth=0.001, xoffset=0.5, yoffset=0.5)

    axes[i, j].set_title(str(((depth_list[index - 1] + depth_list[index]) / 2)) + " (km) <= " + "Depth" + " <= " +
                         str(((depth_list[index] + depth_list[index + 1]) / 2)) + " (km)")
    axes[i, j].xaxis.set_major_locator(ticker.MultipleLocator(10))
    axes[i, j].yaxis.set_major_locator(ticker.MultipleLocator(10))
    axes[i, j].tick_params(labelleft=False, labelright=False, labeltop=False, labelbottom=False)

    cl = m.scatter(df_events["glon"], df_events["glat"], latlon=True, c=df_events["depth"], s=df_events["mb"],
                   cmap="turbo", vmin=min(df_events["depth"]), vmax=max(df_events["depth"]), alpha=1)

    cb = plt.colorbar(cl, ax=axes[i, j], shrink=0.88)
    cb.set_label("Depth (km)")


def main(events_master, mod, lon_min, lon_max, lat_min, lat_max, depth_list):
    # create main plot
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(19, 9))
    fig.suptitle("Distribution by Depths")

    # plot regional events
    df_events = pd.read_csv(events_master, delim_whitespace=True)
    df_events.columns = ["date", "time", "glat", "glon", "depth", "mb", "n1", "n2", "n3", "ievt", "n4"]
    df_events = df_events.drop(["n1", "n2", "n3", "n4"], axis=1)
    df_events = df_events.astype(float)
    df_events = df_events[(df_events["glon"] >= lon_min) & (df_events["glon"] <= lon_max) &
                          (df_events["glat"] >= lat_min) & (df_events["glat"] <= lat_max)]

    # read individual files in file list
    for j, depth in enumerate(depth_list):
        if j <= 2:
            i = 0
        else:
            j -= 3
            i = 1
        plot_models(i, j, axes, df_events, depth, depth_list)

    plt.savefig("/Users/khangvo/Downloads/Distribution_Maps.jpeg")

    plt.show()


# run main()
if __name__ == "__main__":
    # master events
    events_master = "/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/04_TeletomoDD_files/master_event.txt"

    # inversion model
    mod = "/Users/khangvo/Downloads/MOD.xyzv"

    # user specified study area data extent
    lon_min = -80
    lon_max = -55
    lat_min = 5
    lat_max = 25

    depth_list = [12.0, 40.0, 75.0, 120.0, 185.0, 225.0]

    main(events_master, mod, lon_min, lon_max, lat_min, lat_max, depth_list)
