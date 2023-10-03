# File Name: plot_faults_map
# Author: Khang Vo
# Date Created: 9/24/2023
# Date Last Modified: 9/24/2023
# Python Version: 3.10

import os
import glob
import time

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.interpolate import Rbf
from mpl_toolkits.basemap import Basemap


def main(faults_path, lon_min, lon_max, lat_min, lat_max):
    # create main plot
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10), constrained_layout=False)

    m = Basemap(resolution="l", llcrnrlat=lat_min, llcrnrlon=lon_min,
                urcrnrlat=lat_max, urcrnrlon=lon_max, ax=ax, suppress_ticks=False)
    m.drawcoastlines()
    m.shadedrelief(scale=1)
    m.drawparallels(np.arange(-90, 90, 10), labels=[1, 0, 0, 0], linewidth=0.001, xoffset=0.5, yoffset=0.5)
    m.drawmeridians(np.arange(0, 360, 10), labels=[0, 0, 0, 1], linewidth=0.001, xoffset=0.5, yoffset=0.5)

    ax.set_title("Caribbean Fault Lines")
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.tick_params(labelleft=False, labelright=False, labeltop=False, labelbottom=False)

    faults = gpd.read_file(faults_path)
    faults.plot(linestyle="--", color="maroon", linewidth=1.5, alpha=1, ax=ax)

    plt.savefig("/Users/khangvo/Downloads/Caribbean_Fault_Lines.jpeg", bbox_inches="tight")

    plt.show()


# run main()
if __name__ == "__main__":
    # faults
    faults_path = "/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/_shp/central_am_carib_faults-master/shapefile/central_am_caribbean_faults.shp"

    # user specified study area data extent
    lon_min = -80
    lon_max = -55
    lat_min = 5
    lat_max = 25

    main(faults_path, lon_min, lon_max, lat_min, lat_max)
