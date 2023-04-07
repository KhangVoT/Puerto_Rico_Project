# File Name: plot_2D_slices
# Author: Khang Vo
# Date Created: 4/6/2023
# Date Last Modified: 4/6/2023
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


def main(df_original):

    # create main plot
    fig = plt.figure()
    fig.suptitle("Volumetric Data", fontsize=18, y=0.90)
    ax = fig.add_subplot(projection="3d")

    depth_list = np.array(df_original["Depth"].unique())

    for depth in depth_list:
        df = df_original[df_original["Depth"] == depth]
        # cl = ax.contourf(vi, origin="lower", cmap="jet", vmin=min(df["Vel_Perturb"]), vmax=max(df["Vel_Perturb"]),
        #                extent=[df["Long"].min(), df["Long"].max(), df["Lat"].min(), df["Lat"].max()])
        # cl = ax.scatter3D(df["Long"], df["Lat"], df["Depth"], c=df['Vel_Perturb'], cmap="turbo", alpha=1)
        cl = ax.scatter3D(df["Long"], df["Lat"], df["Depth"], c=df['Vel_Perturb'], cmap="turbo",
                          vmin=min(df_original["Vel_Perturb"]), vmax=max(df_original["Vel_Perturb"]), alpha=0.1)

    ax.view_init(azim=-135, elev=15)
    ax.set_xlabel('Longitude (°E)', labelpad=20)
    ax.set_ylabel('Latitude (°N)', labelpad=20)
    ax.set_zlabel('Depth (km)', labelpad=20)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.zaxis.set_major_locator(ticker.MultipleLocator(250))
    ax.set_zlim(min(df_original["Depth"]), max(df_original["Depth"]))

    ax.invert_zaxis()
    cbar = plt.colorbar(cl, ax=ax, shrink=0.9)
    cbar.set_label("km")
    cbar.ax.invert_yaxis()

    plt.show()


# run main()
if __name__ == "__main__":

    file = "/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/04_TeletomoDD_files/reg_perturb_vel_plot_friendly.txt"
    df_original = pd.read_csv(file, sep="\t")

    depth_list = np.array(df_original["Depth"].unique())
    depth_list = depth_list[depth_list < 150]

    df_original = df_original[df_original["Depth"].isin(depth_list[1::])]
    print(df_original)

    main(df_original)
