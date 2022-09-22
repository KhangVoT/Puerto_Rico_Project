# File Name: plot_models
# Author: Khang Vo
# Date Created: 8/10/2022
# Date Last Modified: 8/19/2022
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


def main(file, depth):

    # create main plot
    fig, ax = plt.subplots(figsize=(19, 9))
    fig.suptitle("Plot Friendly", fontsize=18, y=0.95)

    df = pd.read_csv(file, sep="\t")
    df = df[df["Depth"] == depth]

    # build a regular grid with n cells
    xi, yi = np.meshgrid(np.arange(df["Long"].min(), df["Long"].max(), 0.1),
                         np.arange(df["Lat"].min(), df["Lat"].max(), 0.1))

    # do radial basic function interpolation for Vp
    rbfi = Rbf(df["Long"], df["Lat"], df["Vel_Perturb"], function="multiquadric", smooth=0.1)
    vi = rbfi(xi, yi)

    # create subplots
    m = Basemap(resolution="h", llcrnrlat=df["Lat"].min(), llcrnrlon=df["Long"].min(),
                urcrnrlat=df["Lat"].max(), urcrnrlon=df["Long"].max(), ax=ax, suppress_ticks=False)
    m.drawcoastlines()
    m.drawparallels(np.arange(-90, 90, 10), labels=[1, 0, 0, 0], linewidth=0, xoffset=0.5, yoffset=0.5)
    m.drawmeridians(np.arange(0, 360, 10), labels=[0, 0, 0, 1], linewidth=0, xoffset=0.5, yoffset=0.5)
    cl = ax.imshow(vi, origin="lower", cmap="jet", vmin=min(df["Vel_Perturb"]), vmax=max(df["Vel_Perturb"]),
                     extent=[df["Long"].min(), df["Long"].max(), df["Lat"].min(), df["Lat"].max()])

    ax.set_title("Depth = " + str(depth) + " km")

    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.tick_params(labelleft=False, labelright=False, labeltop=False, labelbottom=False)
    cbar = plt.colorbar(cl, ax=ax)
    cbar.set_label("Vp (km/s)")

    plt.show()


# run main()
if __name__ == "__main__":

    file = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/05_TeletomoDD_files/reg_perturb_plot_friendly.txt"

    depth = 50

    main(file, depth)
