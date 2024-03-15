# File Name: plot_distribution_maps
# Author: Khang Vo
# Date Created: 9/21/2022
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


def main(events_reg, events_glb, lon_min, lon_max, lat_min, lat_max):
    # create main plot
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(19, 9), constrained_layout=True)

    # plot regional events
    df_reg = pd.read_csv(events_reg, delim_whitespace=True)
    df_reg.columns = ["date", "time", "glat", "glon", "depth", "mb", "n1", "n2", "n3", "ievt", "n4"]
    df_reg = df_reg.drop(["n1", "n2", "n3", "n4"], axis=1)
    df_reg = df_reg.astype(float)
    df_reg = df_reg[(df_reg["glon"] >= lon_min) & (df_reg["glon"] <= lon_max) &
                    (df_reg["glat"] >= lat_min) & (df_reg["glat"] <= lat_max)]

    m = Basemap(resolution="l", llcrnrlat=df_reg["glat"].min(), llcrnrlon=df_reg["glon"].min(),
                urcrnrlat=df_reg["glat"].max(), urcrnrlon=df_reg["glon"].max(), ax=ax[0], suppress_ticks=False)
    m.drawcoastlines()
    m.shadedrelief(scale=1)
    m.drawparallels(np.arange(-90, 90, 10), labels=[1, 0, 0, 0], linewidth=0.001, xoffset=0.5, yoffset=0.5)
    m.drawmeridians(np.arange(0, 360, 10), labels=[0, 0, 0, 1], linewidth=0.001, xoffset=0.5, yoffset=0.5)

    ax[0].set_title("Regional Events")
    ax[0].xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax[0].yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax[0].tick_params(labelleft=False, labelright=False, labeltop=False, labelbottom=False)

    cl = m.scatter(df_reg["glon"], df_reg["glat"], latlon=True, c=df_reg["depth"], s=df_reg["mb"], cmap="turbo", vmin=min(df_reg["depth"]), vmax=max(df_reg["depth"]), alpha=1)

    cb = plt.colorbar(cl, ax=ax[0], location="bottom")
    cb.set_label("Depth (km)")

    for m in [3, 5, 7]:
        if m == 3:
            ax[0].scatter([], [], c="black", s=m, alpha=0.5,
                          label="<=M" + str(m))
        elif m == 5:
            ax[0].scatter([], [], c="black", s=m, alpha=0.5,
                          label="M" + str(m))
        elif m == 7:
            ax[0].scatter([], [], c="black", s=m, alpha=0.5,
                          label=">=M" + str(m))

    ax[0].legend(scatterpoints=1, frameon=True,
                 labelspacing=0.5, loc="upper right")

    # plot global events
    df_glb = pd.read_csv(events_glb, delim_whitespace=True)
    df_glb.columns = ["date", "time", "glat", "glon", "depth", "mb", "n1", "n2", "n3", "ievt", "n4"]
    df_glb = df_glb.drop(["n1", "n2", "n3", "n4"], axis=1)
    df_glb = df_glb.astype(float)

    m = Basemap(projection="ortho", resolution="l", lat_0=15, lon_0=-67.5, ax=ax[1])
    m.drawcoastlines()
    m.shadedrelief(scale=0.5)

    ax[1].set_title("Global Events")

    cl = m.scatter(df_glb["glon"], df_glb["glat"], latlon=True, c=df_glb["depth"], s=df_glb["mb"], cmap="turbo", vmin=min(df_glb["depth"]), vmax=max(df_glb["depth"]), alpha=1)

    cb = plt.colorbar(cl, ax=ax[1], location="bottom")
    cb.set_label("Depth (km)")

    for m in [3, 5, 7]:
        if m == 3:
            ax[1].scatter([], [], c="black", s=m, alpha=0.5,
                          label="<=M" + str(m))
        elif m == 5:
            ax[1].scatter([], [], c="black", s=m, alpha=0.5,
                          label="M" + str(m))
        elif m == 7:
            ax[1].scatter([], [], c="black", s=m, alpha=0.5,
                          label=">=M" + str(m))

    ax[1].legend(scatterpoints=1, frameon=True,
                 labelspacing=0.5, loc="upper right")

    plt.savefig("/Users/khangvo/Downloads/Distribution_Maps.jpeg", bbox_inches="tight")

    plt.show()


# run main()
if __name__ == "__main__":
    # regional events
    events_reg = "/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/04_TeletomoDD_files/sta_glb_event.txt"

    # global events
    events_glb = "/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/04_TeletomoDD_files/sta_reg_event.txt"

    # user specified study area data extent
    lon_min = -80
    lon_max = -55
    lat_min = 5
    lat_max = 25

    main(events_reg, events_glb, lon_min, lon_max, lat_min, lat_max)
