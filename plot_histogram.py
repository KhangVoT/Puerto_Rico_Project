# File Name: plot_histograms
# Author: Khang Vo
# Date Created: 8/13/2022
# Date Last Modified: 9/24/2022
# Python Version: 3.9

import os
import glob
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_glb(df, ax):
    df["depth"].hist(ax=ax[1], bins=50, color="red", alpha=0.5, histtype="bar", edgecolor="black")

    ax[1].set_title("Global Data")
    ax[1].set_xlabel("Depth (km)")
    ax[1].set_ylabel("Number of Earthquakes")


def plot_reg(df, ax, lon_min, lon_max, lat_min, lat_max):

    df = df[(df["glon"].astype(float) >= lon_min) & (df["glon"].astype(float) <= lon_max) &
            (df["glat"].astype(float) >= lat_min) & (df["glat"].astype(float) <= lat_max)]

    df["depth"].hist(ax=ax[0], bins=50, color="red", alpha=0.5, histtype="bar", edgecolor="black")

    ax[0].set_title("Regional Data")
    ax[0].set_xlabel("Depth (km)")
    ax[0].set_ylabel("Number of Earthquakes")


def main(event_file, lon_min, lon_max, lat_min, lat_max):
    # create main plot
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(19, 9), constrained_layout=True)
    # fig.suptitle("Histograms", fontsize=18, y=0.995)

    df = pd.read_csv(event_file, sep="\t", header=None)
    df.columns = ["date", "time", "glat", "glon", "depth", "mb", "n1", "n2", "n3", "ievt", "n4"]

    plot_reg(df, ax, lon_min, lon_max, lat_min, lat_max)
    plot_glb(df, ax)

    plt.show()


# run main()
if __name__ == "__main__":

    # user specified working directory
    event_file = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/05_TeletomoDD_files/event.txt"

    # user specified study area data extent
    lon_min = -80
    lon_max = -55
    lat_min = 5
    lat_max = 25
    depth_min = 10
    depth_max = 250

    main(event_file, lon_min, lon_max, lat_min, lat_max)
