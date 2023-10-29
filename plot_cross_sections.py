# File Name: plot_cross_section
# Author: Khang Vo
# Date Created: 10/10/2023
# Date Last Modified: 10/29/2023
# Python Version: 3.10

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata


def plot_models(i, j, axes, df, lat, min_depth, max_depth):
    # cutting df
    df = df[min_depth <= df["Depth"]].astype(float)
    df = df[df["Depth"] <= max_depth].astype(float)
    df = df[df["Lat"] == lat].astype(float)

    # create grid and interpolate
    xi, zi = np.mgrid[df["Depth"].min():df["Depth"].max():1, df["Long"].min():df["Long"].max():0.1]
    vi = griddata((df["Depth"], df["Long"]), df["Vp"], (xi, zi), method="cubic")

    # plot subplots
    cl = axes[i, j].imshow(vi, origin="lower", cmap="turbo_r", vmin=min(df["Vp"]), vmax=max(df["Vp"]),
                           aspect="auto",
                           alpha=1,
                           extent=[df["Long"].min(), df["Long"].max(), df["Depth"].min(), df["Depth"].max()])
    # cl = axes[i, j].scatter(df["Long"], df["Depth"], c=df["Vp"],  marker="s", s=10, cmap="turbo_r", vmin=min(df["Vp"]), vmax=max(df["Vp"]), alpha=1)
    axes[i, j].tricontour(df["Long"], df["Depth"], df["Dws"], levels=[1000], linewidths=1, colors="white")

    axes[i, j].set_title("Latitude = " + str(lat) + " $^\circ$N")
    axes[i, j].set_xlabel("Longitude ($^\circ$W)")
    axes[i, j].set_ylabel("Depth (km)")

    cb = plt.colorbar(cl, ax=axes[i, j], shrink=1)
    cb.set_label("Vp (km/s)")

    axes[i, j].invert_yaxis()


def main(vel_file):
    # create main plot
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(19, 9))

    df = pd.read_csv(vel_file, delim_whitespace=True, dtype=object, usecols=range(6))
    df.columns = ["Long", "Lat", "Depth", "Num1", "Vp", "Dws"]
    df = df.apply(pd.to_numeric, errors="coerce").dropna()

    lat_list = [6, 9, 12, 15, 18, 21]
    min_depth = 25
    max_depth = 225

    # loop through each lat to add to subplots
    for j, lat in enumerate(lat_list):
        if j <= 2:
            i = 0
        else:
            j -= 3
            i = 1
        plot_models(i, j, axes, df, lat, min_depth, max_depth)

    # plt.savefig("/Users/khangvo/Downloads/test.jpeg", bbox_inches="tight")

    plt.show()


# run main()
if __name__ == "__main__":

    # user specified working directory
    vel_file = "/Users/khangvo/Downloads/tomoDD.vel.001.005"

    main(vel_file)
