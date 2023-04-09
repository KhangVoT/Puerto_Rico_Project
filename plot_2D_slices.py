# File Name: plot_2D_slices
# Author: Khang Vo
# Date Created: 4/6/2023
# Date Last Modified: 4/9/2023
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


def plot(df_merged, ax):

    lat_list = np.array(df_merged["Lat"].unique())

    for lat in lat_list:
        df = df_merged[df_merged["Lat"] == lat]
        # cl = ax.contourf(vi, origin="lower", cmap="jet", vmin=min(df["Vel_Perturb"]), vmax=max(df["Vel_Perturb"]),
        #                extent=[df["Long"].min(), df["Long"].max(), df["Lat"].min(), df["Lat"].max()])
        # cl = ax.scatter3D(df["Long"], df["Lat"], df["Depth"], c=df["Vel_Perturb"], cmap="turbo", alpha=1)
        cl = ax.scatter3D(df["Long"], df["Lat"], df["Depth"], c=df["Per"], marker="s", s=25, cmap="seismic", vmin=-10, vmax=10, alpha=0.5)

    ax.view_init(azim=-135, elev=15)
    ax.set_xlabel("Longitude (°E)", labelpad=20)
    ax.set_ylabel("Latitude (°N)", labelpad=20)
    ax.set_zlabel("Depth (km)", labelpad=20)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.zaxis.set_major_locator(ticker.MultipleLocator(250))
    ax.set_zlim(min(df_merged["Depth"]), max(df_merged["Depth"]))

    ax.invert_zaxis()
    cbar = plt.colorbar(cl, ax=ax, shrink=0.9)
    cbar.set_label("km")
    cbar.ax.invert_yaxis()


def main(file_list, lat_list, lon_min, lon_max, lat_min, lat_max):
    # create main plot
    fig = plt.figure()
    fig.suptitle("2D Slices", fontsize=18, y=0.90)
    ax = fig.add_subplot(projection="3d")

    for file in file_list:
        if "MOD" in file:
            df_mod = pd.read_csv(file, delim_whitespace=True, dtype=object, usecols=range(5))
            df_mod.columns = ["Long", "Lat", "Depth", "Num1", "Vp"]
        elif "vel" in file:
            df_vel = pd.read_csv(file, delim_whitespace=True, dtype=object, usecols=range(5))
            df_vel.columns = ["Long", "Lat", "Depth", "Num1", "Vp"]

    df_merged = pd.merge(df_mod, df_vel, how="left", on=["Long", "Lat", "Depth"])

    df_merged = df_merged[0:df_merged[df_merged["Long"] == ">"].index[0]].apply(pd.to_numeric, errors="coerce").dropna()

    df_merged = df_merged[(df_merged["Long"].astype(float) >= lon_min) & (df_merged["Long"].astype(float) <= lon_max) &
                          (df_merged["Lat"].astype(float) >= lat_min) & (df_merged["Lat"].astype(float) <= lat_max)]

    df_merged = df_merged[df_merged["Lat"].isin(lat_list)]

    df_merged["Per"] = ((df_merged["Vp_y"] - df_merged["Vp_x"]) / df_merged["Vp_x"]) * 100

    plot(df_merged, ax)

    plt.show()


# run main()
if __name__ == "__main__":

    root = "/Users/khangvo/Downloads/"

    file_list = glob.glob(root + "*MOD.*") + sorted(glob.glob(root + "*.vel.*"))

    lat_list = [5.0, 10.0, 15.0, 20.0, 25.0]

    # user specified study area data extent
    lon_min = -80
    lon_max = -55
    lat_min = 5
    lat_max = 25
    depth_min = 10
    depth_max = 250

    main(file_list, lat_list, lon_min, lon_max, lat_min, lat_max)
