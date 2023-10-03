# File Name: plot_stations
# Author: Khang Vo
# Date Created: 10/2/2022
# Date Last Modified: 10/2/2023
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


def main(sta_reg, sta_glb, lon_min, lon_max, lat_min, lat_max):
    # create main plot
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(19, 9), constrained_layout=True)

    # plot regional stations
    df_reg = pd.read_csv(sta_reg, delim_whitespace=True)
    df_reg.columns = ["sta", "slat", "slon", "elev"]
    df_reg = df_reg[(df_reg["slon"] >= lon_min) & (df_reg["slon"] <= lon_max) &
                    (df_reg["slat"] >= lat_min) & (df_reg["slat"] <= lat_max)]

    m = Basemap(resolution="l", llcrnrlat=df_reg["slat"].min(), llcrnrlon=df_reg["slon"].min(),
                urcrnrlat=df_reg["slat"].max(), urcrnrlon=df_reg["slon"].max(), ax=ax[0], suppress_ticks=False)
    m.drawcoastlines()
    m.shadedrelief(scale=1)
    m.drawparallels(np.arange(-90, 90, 10), labels=[1, 0, 0, 0], linewidth=0.001, xoffset=0.5, yoffset=0.5)
    m.drawmeridians(np.arange(0, 360, 10), labels=[0, 0, 0, 1], linewidth=0.001, xoffset=0.5, yoffset=0.5)

    ax[0].set_title("Regional Data")
    ax[0].xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax[0].yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax[0].tick_params(labelleft=False, labelright=False, labeltop=False, labelbottom=False)

    cl = m.scatter(df_reg["slon"], df_reg["slat"], latlon=True, marker="^", color="black", edgecolors="white", alpha=1)

    # plot global stations
    df_glb = pd.read_csv(sta_glb, delim_whitespace=True)
    df_glb.columns = ["sta", "slat", "slon", "elev"]

    m = Basemap(projection="ortho", resolution="l", lat_0=15, lon_0=-67.5, ax=ax[1])
    m.drawcoastlines()
    m.shadedrelief(scale=0.5)

    ax[1].set_title("Global Data")

    cl = m.scatter(df_glb["slon"], df_glb["slat"], latlon=True, marker="^", color="black", edgecolors="white", alpha=1)

    plt.savefig("/Users/khangvo/Downloads/Stations_Maps.jpeg", bbox_inches="tight")

    plt.show()


# run main()
if __name__ == "__main__":
    # regional stations
    sta_reg = "/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/04_TeletomoDD_files/sta_reg.txt"

    # global stations
    sta_glb = "/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/04_TeletomoDD_files/sta_glb.txt"

    # user specified study area data extent
    lon_min = -80
    lon_max = -55
    lat_min = 5
    lat_max = 25

    main(sta_reg, sta_glb, lon_min, lon_max, lat_min, lat_max)
