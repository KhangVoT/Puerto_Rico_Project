# File Name: plot_models
# Author: Khang Vo
# Date Created: 8/21/2023
# Date Last Modified: 1/31/2024
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


def plot_models(ax, df_control, df, df_events, depth):
    # cut df_vp to desired depth
    df = df[df["Depth"] == depth].astype(float)

    # cut df_vp to desired depth
    df_events = df_events[(df_events["depth"] >= depth - 10) & (df_events["depth"] <= depth + 10)]

    # build a regular grid with n cells
    xi, yi = np.meshgrid(np.arange(df["Long"].min(), df["Long"].max(), 0.1),
                         np.arange(df["Lat"].min(), df["Lat"].max(), 0.1))

    # do radial basic function interpolation for Vp
    rbfi = Rbf(df["Long"], df["Lat"], df["Vp"], function="multiquadric", smooth=0.1)
    vi = rbfi(xi, yi)

    # cut df_control to desired depth
    df_control = df_control[df_control["Depth"] == depth].astype(float)

    # create subplots

    # plot initial model
    m = Basemap(resolution="h", llcrnrlat=df["Lat"].min(), llcrnrlon=df["Long"].min(),
                urcrnrlat=df["Lat"].max(), urcrnrlon=df["Long"].max(), ax=ax, suppress_ticks=False)
    m.drawcoastlines(color="black", linewidth=0.5)
    m.drawparallels(np.arange(-90, 90, 10), labels=[1, 0, 0, 0], linewidth=0.001, xoffset=0.5, yoffset=0.5)
    m.drawmeridians(np.arange(0, 360, 10), labels=[0, 0, 0, 1], linewidth=0.001, xoffset=0.5, yoffset=0.5)
    cl = ax.imshow(vi, origin="lower", cmap="turbo_r", vmin=min(df["Vp"]), vmax=max(df["Vp"]), alpha=1,
                   extent=[df["Long"].min(), df["Long"].max(), df["Lat"].min(), df["Lat"].max()])

    # ax.scatter(df_events["glon"], df_events["glat"], c="black", s=df_events["mb"], alpha=1)

    ax.tricontour(df["Long"], df["Lat"], df["Dws"], levels=[10000], linewidths=1, colors="white")

    ax.set_title("Depth = " + str(depth) + " km")

    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.tick_params(labelleft=False, labelright=False, labeltop=False, labelbottom=False)

    cb = plt.colorbar(cl, ax=ax, shrink=0.88)
    cb.set_label("Vp (km/s)")


def main(file_list, depth_list, events_master, lon_min, lon_max, lat_min, lat_max):
    # create main plot
    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(24, 12))
    # fig.suptitle("Velocity Model (Perturbation)", fontsize=18, y=0.95)

    # create control file to set global color bar
    df_control_list = []
    for file in file_list:
        if "MOD" in file:
            df_control = pd.read_csv(file, delim_whitespace=True, dtype=object, usecols=range(5))
            df_control.columns = ["Long", "Lat", "Depth", "Num1", "Vp"]
            df_control = df_control.apply(pd.to_numeric, errors="coerce").dropna()
        elif "vel" in file:
            df_vel = pd.read_csv(file, delim_whitespace=True, dtype=object, usecols=range(6))
            df_vel.columns = ["Long", "Lat", "Depth", "Num1", "Vp", "Dws"]
            df_vel = df_vel.apply(pd.to_numeric, errors="coerce").dropna()

    df_events = pd.read_csv(events_master, delim_whitespace=True)
    df_events.columns = ["date", "time", "glat", "glon", "depth", "mb", "n1", "n2", "n3", "ievt", "n4"]
    df_events = df_events.drop(["n1", "n2", "n3", "n4"], axis=1)
    df_events = df_events.astype(float)
    df_events = df_events[(df_events["glon"] >= lon_min) & (df_events["glon"] <= lon_max) &
                          (df_events["glat"] >= lat_min) & (df_events["glat"] <= lat_max)]

    # loop through each depth to add to subplots
    for i, ax in enumerate(fig.axes):
        depth = depth_list[i]
        plot_models(ax, df_control, df_vel, df_events, depth)

    plt.savefig("/Users/khangvo/Downloads/Velocity_Model_perturb_glb_events.jpeg", bbox_inches="tight")

    plt.show()


# run main()
if __name__ == "__main__":

    root = "/Users/khangvo/Downloads/"

    file_list = glob.glob(root + "*MOD.*") + sorted(glob.glob(root + "*.vel.*"))

    # master events
    events_master = "/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/04_TeletomoDD_files/master_event.txt"

    # depth_list = [12.0, 40.0, 75.0, 120.0, 185.0, 225.0]
    depth_list = [25.0, 40.0, 55.0, 75.0, 95.0, 120.0, 150.0, 185.0, 225.0]

    # user specified study area data extent
    lon_min = -80
    lon_max = -55
    lat_min = 5
    lat_max = 25
    depth_min = 10
    depth_max = 250

    main(file_list, depth_list, events_master, lon_min, lon_max, lat_min, lat_max)
