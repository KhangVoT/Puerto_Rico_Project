# File Name: plot_3D_cube
# Author: Khang Vo
# Date Created: 4/4/2023
# Date Last Modified: 4/9/2023
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

plt.close("all")
fig = plt.figure()
ax = fig.add_subplot(projection="3d")

file = "/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/04_TeletomoDD_files/reg_perturb_vel_plot_friendly.txt"
df = pd.read_csv(file, sep="\t")

cset = [[], [], []]

df_top = df[df["Depth"] == 0]
# cset[0] = ax.contourf(xi, yi, vi, zdir="z", levels=np.linspace(np.min(vi), np.max(vi)), cmap="turbo")
cset[0] = ax.scatter3D(df_top["Long"], df_top["Lat"], df_top["Depth"], marker="s", s=10, c=df_top["Vel_Perturb"], cmap="turbo", alpha=1)

df_side = df[df["Depth"] > 0]
df_side = df_side[df_side["Long"] == -80]
# cset[1] = ax.contourf(vi, yi, xi, zdir="x", levels=np.linspace(np.min(vi), np.max(vi)), cmap="turbo")
cset[1] = ax.scatter3D(df_side["Long"], df_side["Lat"], df_side["Depth"], marker="s", s=25, c=df_side["Vel_Perturb"], cmap="turbo", alpha=1)

df_front = df[df["Depth"] > 0]
df_front = df_front[df_front["Lat"] == 5]
# cset[2] = ax.contourf(xi, vi, yi, zdir="y", levels=np.linspace(np.min(vi), np.max(vi)), cmap="turbo")
cset[2] = ax.scatter3D(df_front["Long"], df_front["Lat"], df_front["Depth"], marker="s", s=25, c=df_front["Vel_Perturb"], cmap="turbo", alpha=1)

ax.view_init(azim=-135, elev=15)
ax.set_xlabel("Longitude (°E)", labelpad=20)
ax.set_ylabel("Latitude (°N)", labelpad=20)
ax.set_zlabel("Depth (km)", labelpad=20)
ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
ax.zaxis.set_major_locator(ticker.MultipleLocator(250))
ax.set_zlim(min(df["Depth"]), max(df["Depth"]))

ax.invert_zaxis()
cbar = plt.colorbar(cset[0], ax=ax, shrink=0.9)
cbar.set_label("Vp")
cbar.ax.invert_yaxis()

plt.show()
