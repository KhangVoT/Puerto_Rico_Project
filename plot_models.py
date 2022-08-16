# File Name: plot_models
# Author: Khang Vo
# Date Created: 8/10/2022
# Date Last Modified: 8/15/2022
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


def plot_models(n, axes, df_merged, depth):
    # cut df_vp to desired depth
    df = df_merged[df_merged["Depth"] == depth]

    # build a regular grid with n cells
    xi, yi = np.meshgrid(np.arange(df["Long"].min(), df["Long"].max(), 0.1),
                         np.arange(df["Lat"].min(), df["Lat"].max(), 0.1))

    # do radial basic function interpolation for Vp_init
    rbfi_init = Rbf(df["Long"], df["Lat"], df["Vp_init"], function="multiquadric", smooth=0.1)
    vi_init = rbfi_init(xi, yi)

    # do radial basic function interpolation for Vp_final
    rbfi_final = Rbf(df["Long"], df["Lat"], df["Vp_final"], function="multiquadric", smooth=0.1)
    vi_final = rbfi_final(xi, yi)

    # create subplots

    # plot initial model
    m = Basemap(resolution="h", llcrnrlat=df["Lat"].min(), llcrnrlon=df["Long"].min(),
                urcrnrlat=df["Lat"].max(), urcrnrlon=df["Long"].max(), ax=axes[n], suppress_ticks=False)
    m.drawcoastlines()
    m.drawparallels(np.arange(-90, 90, 5), labels=[1, 0, 0, 0], linewidth=0, xoffset=0.5, yoffset=0.5)
    m.drawmeridians(np.arange(0, 360, 5), labels=[0, 0, 0, 1], linewidth=0, xoffset=0.5, yoffset=0.5)
    cl = axes[n].imshow(vi_init, origin="lower", cmap="jet", vmin=min(df["Vp_final"]), vmax=max(df["Vp_final"]),
                        extent=[df["Long"].min(), df["Long"].max(), df["Lat"].min(), df["Lat"].max()])
    axes[n].set_title("Initial Model: " + "Depth = " + str(depth) + " (km)")
    axes[n].xaxis.set_major_locator(ticker.MultipleLocator(5))
    axes[n].yaxis.set_major_locator(ticker.MultipleLocator(5))
    axes[n].tick_params(labelleft=False, labelright=False, labeltop=False, labelbottom=False)
    cbar = plt.colorbar(cl, ax=axes[n])
    cbar.set_label("Vp (km/s)")

    # plot final model
    m = Basemap(resolution="h", llcrnrlat=df["Lat"].min(), llcrnrlon=df["Long"].min(),
                urcrnrlat=df["Lat"].max(), urcrnrlon=df["Long"].max(), ax=axes[n + 1], suppress_ticks=False)
    m.drawcoastlines()
    m.drawparallels(np.arange(-90, 90, 5), labels=[1, 0, 0, 0], linewidth=0, xoffset=0.5, yoffset=0.5)
    m.drawmeridians(np.arange(0, 360, 5), labels=[0, 0, 0, 1], linewidth=0, xoffset=0.5, yoffset=0.5)
    cl = axes[n + 1].imshow(vi_final, origin="lower", cmap="jet", vmin=min(df["Vp_final"]), vmax=max(df["Vp_final"]),
                            extent=[df["Long"].min(), df["Long"].max(), df["Lat"].min(), df["Lat"].max()])
    axes[n + 1].set_title("Final Model: " + "Depth = " + str(depth) + " (km)")
    axes[n + 1].xaxis.set_major_locator(ticker.MultipleLocator(5))
    axes[n + 1].yaxis.set_major_locator(ticker.MultipleLocator(5))
    axes[n + 1].tick_params(labelleft=False, labelright=False, labeltop=False, labelbottom=False)
    cbar = plt.colorbar(cl, ax=axes[n + 1])
    cbar.set_label("Vp (km/s)")


def main(mod_file, vp_file, depth_list):
    # read mod_file
    df_mod_orig = pd.read_csv(mod_file, delim_whitespace=True, dtype=object)
    df_mod_orig.columns = ["Long", "Lat", "Depth", "Num1", "Vp_init"]
    df_mod_orig = df_mod_orig.drop(["Num1"], axis=1)

    # read vp_file
    df_vp_orig = pd.read_csv(vp_file, delim_whitespace=True, dtype=object)
    df_vp_orig.columns = ["Long", "Lat", "Depth", "Num1", "Vp_final", "Num2"]
    df_vp_orig = df_vp_orig.drop(["Num1", "Num2"], axis=1)

    df_merged = pd.merge(df_mod_orig, df_vp_orig, how="left", left_on=["Long", "Lat", "Depth"], right_on=["Long", "Lat", "Depth"])
    df_merged = df_merged.dropna().astype(float)

    # create main plot
    fig, axes = plt.subplots(nrows=len(depth_list), ncols=2, figsize=(10, 9))
    axes = axes.flatten()

    # loop through each depth to add to subplots
    for n, depth in enumerate(depth_list):
        # skip 1 subplot due to plotting in pairs
        n *= 2
        plot_models(n, axes, df_merged, depth)

    fig.suptitle("tomoDD.vel.001.005", fontsize=18, y=0.95)
    # plt.tight_layout()
    plt.show()


# run main()
if __name__ == "__main__":

    # user specified working directory
    mod_file = "/Users/khangvo/Downloads/MOD.xyzv"
    vp_file = "/Users/khangvo/Downloads/tomoDD.vel.001.005"

    depth_list = [22.6, 338.8, 745.5]

    main(mod_file, vp_file, depth_list)
