# File Name: plot_correlated_events
# Author: Khang Vo
# Date Created: 3/15/2024
# Date Last Modified: 3/15/2024
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


def main(events_orig, events_reloc, lon_min, lon_max, lat_min, lat_max):
    # create main plot
    fig, ax = plt.subplots(figsize=(19, 9), constrained_layout=True)

    # plot original events
    df_reg = pd.read_csv(events_orig, delim_whitespace=True)
    df_reg.columns = ["date", "time", "glat", "glon", "depth", "mb", "n1", "n2", "n3", "ievt", "n4"]
    df_reg = df_reg.drop(["date", "time", "depth", "mb", "n1", "n2", "n3", "n4"], axis=1)
    df_reg = df_reg.astype(float)
    df_reg = df_reg[(df_reg["glon"] >= lon_min) & (df_reg["glon"] <= lon_max) &
                    (df_reg["glat"] >= lat_min) & (df_reg["glat"] <= lat_max)]

    df_reloc = pd.read_csv(events_reloc, delim_whitespace=True, header=None)
    df_reloc = df_reloc.drop(df_reloc.columns[3::], axis=1)
    df_reloc.columns = ["ievt", "glat", "glon"]
    df_reloc = df_reloc.astype(float)
    df_reloc = df_reloc[(df_reloc["glon"] >= lon_min) & (df_reloc["glon"] <= lon_max) &
                        (df_reloc["glat"] >= lat_min) & (df_reloc["glat"] <= lat_max)]

    df_merge = df_reg.merge(df_reloc, left_on="ievt", right_on="ievt", suffixes=("_orig", "_reloc"), how="outer", indicator=True)

    df_nomatch = df_merge[df_merge["_merge"] == "left_only"]
    df_yesmatch = df_merge[df_merge["_merge"] == "both"]

    m = Basemap(resolution="l", llcrnrlat=df_reg["glat"].min(), llcrnrlon=df_reg["glon"].min(),
                urcrnrlat=df_reg["glat"].max(), urcrnrlon=df_reg["glon"].max(), ax=ax, suppress_ticks=False)
    m.drawcoastlines()
    m.shadedrelief(scale=1)
    m.drawparallels(np.arange(-90, 90, 10), labels=[1, 0, 0, 0], linewidth=0.001, xoffset=0.5, yoffset=0.5)
    m.drawmeridians(np.arange(0, 360, 10), labels=[0, 0, 0, 1], linewidth=0.001, xoffset=0.5, yoffset=0.5)

    ax.set_title("Cross Correlated Events")
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.tick_params(labelleft=False, labelright=False, labeltop=False, labelbottom=False)

    no_match = m.scatter(df_nomatch["glon_orig"], df_nomatch["glat_orig"], latlon=True, c="white", s=1, alpha=1)
    yes_match = m.scatter(df_yesmatch["glon_reloc"], df_yesmatch["glat_reloc"], latlon=True, c="black", s=1, alpha=1)

    plt.legend((no_match, yes_match), ('Not Correlated', "Cross Correlated"), fontsize=10, facecolor="gray")

    plt.savefig("/Users/khangvo/Downloads/Distribution_Maps.jpeg", bbox_inches="tight")

    plt.show()


# run main()
if __name__ == "__main__":
    # original events
    events_orig = "/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/04_TeletomoDD_files/master_event.txt"

    # relocated events
    events_reloc = "/Users/khangvo/Downloads/tomoDD.reloc.001.025"

    # user specified study area data extent
    lon_min = -80
    lon_max = -55
    lat_min = 5
    lat_max = 25

    main(events_orig, events_reloc, lon_min, lon_max, lat_min, lat_max)
