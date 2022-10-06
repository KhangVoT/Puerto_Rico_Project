# File Name: plot_distribution_maps
# Author: Khang Vo
# Date Created: 9/21/2022
# Date Last Modified: 10/5/2022
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
    # fig.suptitle("Distribution Map", fontsize=18, y=0.995)

    # plot regional events
    df_reg = pd.read_csv(events_reg, delim_whitespace=True)
    df_reg.columns = ["date", "time", "glat", "glon", "depth", "mb", "n1", "n2", "n3", "ievt", "n4"]
    df_reg = df_reg.drop(["n1", "n2", "n3", "n4"], axis=1)
    df_reg = df_reg.astype(float)
    df_reg = df_reg[(df_reg["glon"].astype(float) >= lon_min) & (df_reg["glon"].astype(float) <= lon_max) &
                    (df_reg["glat"].astype(float) >= lat_min) & (df_reg["glat"].astype(float) <= lat_max)]

    m = Basemap(resolution="h", llcrnrlat=df_reg["glat"].min(), llcrnrlon=df_reg["glon"].min(),
                urcrnrlat=df_reg["glat"].max(), urcrnrlon=df_reg["glon"].max(), ax=ax[0])
    m.drawparallels(np.arange(-90, 90, 10), labels=[1, 0, 0, 0], linewidth=0, xoffset=0.5, yoffset=0.5)
    m.drawmeridians(np.arange(0, 360, 10), labels=[0, 0, 0, 1], linewidth=0, xoffset=0.5, yoffset=0.5)
    m.shadedrelief(scale=0.5)
    m.drawcoastlines(color="lightgray")
    m.drawcountries(color="lightgray")
    m.drawstates(color="lightgray")

    cl = m.scatter(df_reg["glon"], df_reg["glat"], latlon=True, c=df_reg["depth"], s=df_reg["mb"], cmap="jet", alpha=0.5)

    cb = plt.colorbar(cl, ax=ax[0])
    cb.set_label("Depth (km)")

    ax[0].set_title("Regional Data")

    # plot global events
    df_glb = pd.read_csv(events_glb, delim_whitespace=True)
    df_glb.columns = ["date", "time", "glat", "glon", "depth", "mb", "n1", "n2", "n3", "ievt", "n4"]
    df_glb = df_glb.drop(["n1", "n2", "n3", "n4"], axis=1)
    df_glb = df_glb.astype(float)

    m = Basemap(projection="ortho", resolution=None, lat_0=15, lon_0=-67.5, ax=ax[1])
    m.shadedrelief(scale=0.5)

    cl = m.scatter(df_glb["glon"], df_glb["glat"], latlon=True, c=df_glb["depth"], s=df_glb["mb"], cmap="jet", alpha=0.5)

    cb = plt.colorbar(cl, ax=ax[1])
    cb.set_label("Depth (km)")

    ax[1].set_title("Global Data")

    plt.show()


# run main()
if __name__ == "__main__":
    # regional events
    events_reg = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/05_TeletomoDD_files/event.txt"

    # global events
    events_glb = "/Users/khangvo/Python_Projects/Puerto_Rico_Project_Refinement/files/05_TeletomoDD_files/event.txt"

    # user specified study area data extent
    lon_min = -80
    lon_max = -55
    lat_min = 5
    lat_max = 25

    main(events_reg, events_glb, lon_min, lon_max, lat_min, lat_max)
