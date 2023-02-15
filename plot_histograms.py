# File Name: plot_histograms
# Author: Khang Vo
# Date Created: 8/13/2022
# Date Last Modified: 10/5/2022
# Python Version: 3.9

import os
import glob
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main(events_reg, events_glb, lon_min, lon_max, lat_min, lat_max):
    # create main plot
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(19, 9), constrained_layout=True)
    # fig.suptitle("Histograms", fontsize=18, y=0.995)

    # plot regional events
    df_reg = pd.read_csv(events_reg, delim_whitespace=True)
    df_reg.columns = ["date", "time", "glat", "glon", "depth", "mb", "n1", "n2", "n3", "ievt", "n4"]
    df_reg = df_reg[(df_reg["glon"].astype(float) >= lon_min) & (df_reg["glon"].astype(float) <= lon_max) &
                    (df_reg["glat"].astype(float) >= lat_min) & (df_reg["glat"].astype(float) <= lat_max)]

    df_reg["depth"].hist(ax=ax[0], bins=50, color="red", alpha=0.5, histtype="bar", edgecolor="black")

    ax[0].set_title("Regional Data")
    ax[0].set_xlabel("Depth (km)")
    ax[0].set_ylabel("Number of Earthquakes")
    ax[0].grid(True)

    # plot global events
    df_glb = pd.read_csv(events_glb, delim_whitespace=True)
    df_glb.columns = ["date", "time", "glat", "glon", "depth", "mb", "n1", "n2", "n3", "ievt", "n4"]

    df_glb["depth"].hist(ax=ax[1], bins=50, color="red", alpha=0.5, histtype="bar", edgecolor="black")

    ax[1].set_title("Global Data")
    ax[1].set_xlabel("Depth (km)")
    ax[1].set_ylabel("Number of Earthquakes")
    ax[1].grid(True)

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
