# File Name: plot_single_model
# Author: Khang Vo
# Date Created: 8/10/2022
# Date Last Modified: 10/2/2023
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


def plot_glb(file, depth):

    # create main plot
    fig, ax = plt.subplots(figsize=(19, 9))
    # fig.suptitle("Plot Friendly", fontsize=18, y=0.95)

    df = pd.read_csv(file, sep="\t")
    df = df[df["Depth"] == depth]

    # build a regular grid with n cells
    xi, yi = np.meshgrid(np.arange(df["Long"].min(), df["Long"].max(), 1),
                         np.arange(df["Lat"].min(), df["Lat"].max(), 1))

    # do radial basic function interpolation for Vp
    rbfi = Rbf(df["Long"], df["Lat"], df["Vel_Perturb"], function="multiquadric", smooth=1)
    vi = rbfi(xi, yi)

    # create subplots
    m = Basemap(projection="cyl", resolution="l", ax=ax, suppress_ticks=False)
    m.drawcoastlines()
    m.drawparallels(np.arange(-90, 90, 30), labels=[1, 0, 0, 0], linewidth=0.001, xoffset=5, yoffset=5)
    m.drawmeridians(np.arange(0, 360, 30), labels=[0, 0, 0, 1], linewidth=0.001, xoffset=5, yoffset=5)
    cl = ax.imshow(vi, origin="lower", cmap="turbo_r", vmin=min(df["Vel_Perturb"]), vmax=max(df["Vel_Perturb"]),
                   extent=[df["Long"].min(), df["Long"].max(), df["Lat"].min(), df["Lat"].max()])

    # cl = m.scatter(df["Long"], df["Lat"], latlon=True, c=df["Vel_Perturb"], cmap="turbo", vmin=min(df["Vel_Perturb"]), vmax=max(df["Vel_Perturb"]), alpha=1)

    ax.set_title("Depth = " + str(depth) + " km")

    ax.xaxis.set_major_locator(ticker.MultipleLocator(30))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(30))
    ax.tick_params(labelleft=False, labelright=False, labeltop=False, labelbottom=False)
    cbar = plt.colorbar(cl, ax=ax, shrink=0.85)
    cbar.set_label("Vp (km/s)")

    plt.savefig("/Users/khangvo/Downloads/Velocity_Model_glb.jpeg", bbox_inches="tight")

    plt.show()


def plot_reg(file, depth):

    # create main plot
    fig, ax = plt.subplots(figsize=(19, 9))
    # fig.suptitle("Plot Friendly", fontsize=18, y=0.95)

    df = pd.read_csv(file, sep="\t")
    df = df[df["Depth"] == depth]

    # build a regular grid with n cells
    xi, yi = np.meshgrid(np.arange(df["Long"].min(), df["Long"].max(), 0.1),
                         np.arange(df["Lat"].min(), df["Lat"].max(), 0.1))

    # do radial basic function interpolation for Vp
    rbfi = Rbf(df["Long"], df["Lat"], df["Vel_Perturb"], function="multiquadric", smooth=0.1)
    vi = rbfi(xi, yi)

    # create subplots
    m = Basemap(resolution="h", llcrnrlat=df["Lat"].min(), llcrnrlon=df["Long"].min(),
                urcrnrlat=df["Lat"].max(), urcrnrlon=df["Long"].max(), ax=ax, suppress_ticks=False)
    m.drawcoastlines()
    m.drawparallels(np.arange(-90, 90, 10), labels=[1, 0, 0, 0], linewidth=0.001, xoffset=0.5, yoffset=0.5)
    m.drawmeridians(np.arange(0, 360, 10), labels=[0, 0, 0, 1], linewidth=0.001, xoffset=0.5, yoffset=0.5)
    cl = ax.imshow(vi, origin="lower", cmap="turbo_r", vmin=min(df["Vel_Perturb"]), vmax=max(df["Vel_Perturb"]),
                   extent=[df["Long"].min(), df["Long"].max(), df["Lat"].min(), df["Lat"].max()])

    ax.set_title("Depth = " + str(depth) + " km")

    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.tick_params(labelleft=False, labelright=False, labeltop=False, labelbottom=False)
    cbar = plt.colorbar(cl, ax=ax)
    cbar.set_label("Vp (km/s)")

    plt.savefig("/Users/khangvo/Downloads/Velocity_Model_reg.jpeg", bbox_inches="tight")

    plt.show()


# run main()
if __name__ == "__main__":

    vel_reg = "/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/04_TeletomoDD_files/reg_perturb_vel_plot_friendly.txt"
    depth_reg = 55

    vel_glb = "/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/04_TeletomoDD_files/glb_perturb_vel_plot_friendly.txt"
    depth_glb = 55

    plot_reg(vel_reg, depth_reg)
    plot_glb(vel_glb, depth_glb)
