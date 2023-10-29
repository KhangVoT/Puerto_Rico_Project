# File Name: plot_dws_histogram
# Author: Khang Vo
# Date Created: 10/19/2023
# Date Last Modified: 10/20/2023
# Python Version: 3.10

import os
import glob
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def main(file, depth_list):
    # create main plot
    fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(24, 12), constrained_layout=True)
    # fig.suptitle("DWS", fontsize=18, y=0.95)

    df_vel = pd.read_csv(file, delim_whitespace=True, dtype=object, usecols=range(6))
    df_vel.columns = ["Long", "Lat", "Depth", "Num1", "Vp", "Dws"]
    df_vel = df_vel.astype(float)
    df_vel = df_vel[df_vel["Dws"] > 0]
    df_vel = df_vel[df_vel["Dws"] <= 10000]

    for i, ax in enumerate(fig.axes):
        depth = depth_list[i]
        df_cut = df_vel[df_vel["Depth"] == depth]
        df_cut["Dws"].hist(ax=ax, bins=100, color="red", alpha=0.5, histtype="bar", edgecolor="black")

        ax.set_title("Depth = " + str(depth) + " km")
        ax.set_xlabel("DWS")
        ax.set_ylabel("Frequency")
        ax.grid(True)

        ax.xaxis.set_major_locator(ticker.MultipleLocator(1000))

    plt.savefig("/Users/khangvo/Downloads/DWS_Histogram.jpeg", bbox_inches="tight")

    plt.show()


# run main()
if __name__ == "__main__":
    file = "/Users/khangvo/Downloads/tomoDD.vel.001.005"

    depth_list = [25.0, 40.0, 55.0, 75.0, 95.0, 120.0, 150.0, 185.0, 225.0]

    main(file, depth_list)
