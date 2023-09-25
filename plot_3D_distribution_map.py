# File Name: plot_3D_distribution_map
# Author: Khang Vo
# Date Created: 4/2/2023
# Date Last Modified: 4/3/2023
# Python Version: 3.10

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import PolyCollection


def read_df(path, lon_min, lon_max, lat_min, lat_max):
    # plot master events
    df = pd.read_csv(path, delim_whitespace=True)
    df.columns = ["date", "time", "glat", "glon", "depth", "mb", "n1", "n2", "n3", "ievt", "n4"]
    df = df.drop(["n1", "n2", "n3", "n4"], axis=1)
    df = df.astype(float)
    df = df[(df["glon"] >= lon_min) & (df["glon"] <= lon_max) & (df["glat"] >= lat_min) & (df["glat"] <= lat_max)]

    return df


def plot3d(df):
    fig = plt.figure(figsize=(10, 10))
    fig.suptitle("3D Distribution Map", fontsize=18, y=0.80)
    ax = fig.add_subplot(projection="3d")
    # Define lower left, uperright lontitude and lattitude respectively
    m = Basemap(resolution="h", llcrnrlat=df["glat"].min(), llcrnrlon=df["glon"].min(),
                urcrnrlat=df["glat"].max(), urcrnrlon=df["glon"].max(), ax=ax, suppress_ticks=False)
    cl = m.scatter(df["glon"], df["glat"], latlon=True, c=df["depth"], s=df["mb"], cmap="turbo",
                   vmin=min(df["depth"]), vmax=max(df["depth"]), alpha=1, zs=-50.1)

    # ax.add_collection3d(m.drawcoastlines(linewidth=1), zs=-50.1)
    # ax.add_collection3d(m.drawcountries(linewidth=1), zs=-50.1)

    land_poly = []
    for polygon in m.landpolygons:
        land_poly.append(polygon.get_coords())
    land_color = PolyCollection(land_poly, edgecolor="black", facecolor="wheat", alpha=1, closed=False)
    ax.add_collection3d(land_color, zs=-50)

    rectangle_polygon = np.array([[df["glon"].min(), df["glat"].min()], [df["glon"].min(), df["glat"].max()],
                            [df["glon"].max(), df["glat"].max()], [df["glon"].max(), df["glat"].min()]])
    sea_polygon = [rectangle_polygon]
    sea_color = PolyCollection(sea_polygon, edgecolor="none", linewidth=0.1, facecolor="powderblue", alpha=1, closed=False)
    ax.add_collection3d(sea_color, zs=-49.9)

    ax.view_init(azim=-135, elev=15)
    ax.set_xlabel("Longitude (°E)", labelpad=10)
    ax.set_ylabel("Latitude (°N)", labelpad=10)
    ax.set_zlabel("Depth (km)", labelpad=10)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.zaxis.set_major_locator(ticker.MultipleLocator(50))
    ax.set_zlim(min(df["depth"]), max(df["depth"]))

    img = ax.scatter(df["glon"], df["glat"], df["depth"], c=df["depth"], s=5, cmap="turbo")

    ax.invert_zaxis()
    cbar = plt.colorbar(cl, ax=ax, shrink=0.7)
    cbar.set_label("km")
    cbar.ax.invert_yaxis()


def main():
    model_path = "/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/04_TeletomoDD_files/master_event.txt"

    # user specified study area data extent
    lon_min = -80
    lon_max = -55
    lat_min = 5
    lat_max = 25

    df = read_df(model_path, lon_min, lon_max, lat_min, lat_max)

    plot3d(df)

    plt.savefig("/Users/khangvo/Downloads/3D_Distribution_Maps.jpeg", bbox_inches="tight", pad_inches=0.5)

    plt.show()


if __name__ == "__main__":
    main()
