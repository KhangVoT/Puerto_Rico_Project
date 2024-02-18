# File Name: plot_cross_sections
# Author: Khang Vo
# Date Created: 10/10/2023
# Date Last Modified: 11/20/2023
# Python Version: 3.10

import os
import glob
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.ticker as ticker
from scipy.interpolate import interpn
from scipy.interpolate import griddata
from pyproj import Geod


def plot_models(ax, df, profile):
    df_control = df
    df = df[df["Profile"] == profile]

    # create grid and interpolate
    zi, xi = np.mgrid[df["Depth"].min():df["Depth"].max():0.1, df["Dist_Tot"].min():df["Dist_Tot"].max():0.1]
    vi = griddata((df["Depth"], df["Dist_Tot"]), df["Vp"], (zi, xi), method="cubic")

    # plot subplots
    cl = ax.imshow(vi, origin="lower", cmap="turbo_r", vmin=min(df_control["Vp"]), vmax=max(df_control["Vp"]),
                   aspect="auto",
                   alpha=1,
                   extent=[df["Dist_Tot"].min(), df["Dist_Tot"].max(), df["Depth"].min(), df["Depth"].max()])
    # cl = ax.scatter(df["Dist_Tot"], df["Depth"], c=df["Vp"],  marker="s", s=10, cmap="turbo_r", vmin=min(df["Vp"]), vmax=max(df["Vp"]), alpha=1)
    ax.tricontour(df["Dist_Tot"], df["Depth"], df["Dws"], levels=[10000], linewidths=1, colors="white")

    ax.set_title("Profile = " + profile)
    ax.set_xlabel("Distance (km)")
    ax.set_ylabel("Depth (km)")

    cb = plt.colorbar(cl, ax=ax, shrink=1)
    cb.set_label("Vp (km/s)")

    ax.invert_yaxis()


def plot_path_profiles(vel_file, key, profile, ax):
    df = pd.read_csv(vel_file, delim_whitespace=True, dtype=object, usecols=range(6))
    df.columns = ["Long", "Lat", "Depth", "Num1", "Vp", "Dws"]
    df = df.apply(pd.to_numeric, errors="coerce").dropna()

    if key == "A":
        m = Basemap(resolution="h", llcrnrlat=df["Lat"].min(), llcrnrlon=df["Long"].min(),
                    urcrnrlat=df["Lat"].max(), urcrnrlon=df["Long"].max(), ax=ax, suppress_ticks=False)
        m.drawcoastlines(color="black")
        m.shadedrelief(scale=1)
        m.drawparallels(np.arange(-90, 90, 10), labels=[1, 0, 0, 0], linewidth=0.001, xoffset=0.5, yoffset=0.5)
        m.drawmeridians(np.arange(0, 360, 10), labels=[0, 0, 0, 1], linewidth=0.001, xoffset=0.5, yoffset=0.5)
        ax.tick_params(labelleft=False, labelright=False, labeltop=False, labelbottom=False)

    profile_long = np.linspace(profile[0], profile[2], 2)
    profile_lat = np.linspace(profile[1], profile[3], 2)

    ax.plot(profile_long, profile_lat, c="hotpink")
    ax.annotate(key, xy=(profile[0] - 1, profile[1] - 1))
    ax.annotate(key + "'", xy=(profile[2] + 1, profile[3] + 1))


# function to interpolate velocities
def interp(points, vp_values, dws_values, profile, key, min_depth, max_depth, depth_step, long_lat_linspace):
    # create profile
    profile_long = np.linspace(profile[0], profile[2], long_lat_linspace)
    profile_lat = np.linspace(profile[1], profile[3], long_lat_linspace)
    profile_depth = np.arange(min_depth, max_depth + depth_step, depth_step)

    df_list = []
    for i, depth in enumerate(profile_depth):
        df = pd.DataFrame(columns=["Long", "Lat", "Depth", "Vp", "Dws", "Profile"])
        df["Long"] = profile_long
        df["Lat"] = profile_lat
        df["Depth"] = profile_depth[i]
        df["Profile"] = key
        df_list.append(df)
    df_combined = pd.concat(df_list, axis=0).reset_index(drop=True)

    wgs_84_geod = Geod(ellps="WGS84")
    for j in range(len(df_combined) - 1):
        az12, az21, dist = wgs_84_geod.inv(df_combined.loc[j, "Lat"], df_combined.loc[j, "Long"],
                                           df_combined.loc[j + 1, "Lat"], df_combined.loc[j + 1, "Long"])
        df_combined.loc[j + 1, "Dist"] = dist / 1000
    df_combined.loc[df_combined.groupby("Depth")["Dist"].head(1).index, "Dist"] = 0
    df_combined["Dist_Tot"] = df_combined.groupby(by=["Depth"])["Dist"].transform(lambda x: x.cumsum())

    for k in range(len(df_combined)):
        dvp_request = np.array([df_combined.loc[k, "Long"], df_combined.loc[k, "Lat"], df_combined.loc[k, "Depth"]])
        dvp = interpn(points, vp_values, dvp_request, method="linear", bounds_error=False, fill_value=None)
        df_combined.loc[k, "Vp"] = float(dvp)
        dws_request = np.array([df_combined.loc[k, "Long"], df_combined.loc[k, "Lat"], df_combined.loc[k, "Depth"]])
        dws = interpn(points, dws_values, dws_request, method="linear", bounds_error=False, fill_value=None)
        df_combined.loc[k, "Dws"] = float(dws)

    return df_combined


# function to create 3D velocity model for interpolation
def create_model(vel_file):
    df = pd.read_csv(vel_file, delim_whitespace=True, dtype=object, usecols=range(6))
    df.columns = ["Long", "Lat", "Depth", "Num1", "Vp", "Dws"]
    df = df.apply(pd.to_numeric, errors="coerce").dropna()

    # extract the list of coordinates
    xs = np.array(df["Long"].to_list())
    ys = np.array(df["Lat"].to_list())
    zs = np.array(df["Depth"].to_list())
    # extract the associated velocity values
    vs = np.array(df["Vp"].to_list())
    # extract the associated dws values
    dws = np.array(df["Dws"].to_list())

    px, ix = np.unique(xs, return_inverse=True)
    py, iy = np.unique(ys, return_inverse=True)
    pz, iz = np.unique(zs, return_inverse=True)

    points = (px, py, pz)

    vp_values = np.empty_like(vs, shape=(px.size, py.size, pz.size))
    vp_values[ix, iy, iz] = vs

    dws_values = np.empty_like(dws, shape=(px.size, py.size, pz.size))
    dws_values[ix, iy, iz] = dws

    return points, vp_values, dws_values


def main(vel_file):
    min_depth = 25
    max_depth = 225
    depth_step = 10
    long_lat_linspace = 10

    profiles_list = []
    profiles_list.append([-73.44, 17.26, -72.35, 20.90])
    profiles_list.append([-69.29, 17.32, -68.80, 20.02])
    profiles_list.append([-66.51, 17.36, -66.33, 19.26])
    profiles_list.append([-63.47, 16.97, -62.59, 18.93])
    profiles_list.append([-62.30, 15.39, -60.43, 16.19])
    profiles_list.append([-62.05, 13.79, -60.08, 13.25])
    profile_names = ["A", "B", "C", "D", "E", "F"]
    profiles = dict(zip(profile_names, profiles_list))

    points, vp_values, dws_values = create_model(vel_file)

    # loop through each depth to add to subplots
    df_list = []
    for i, profile in enumerate(profiles):
        df = interp(points, vp_values, dws_values, profiles[profile], profile, min_depth, max_depth, depth_step,
                    long_lat_linspace)
        df_list.append(df)
    df_combined = pd.concat(df_list, axis=0).reset_index(drop=True)
    df_combined["Dws"] = df_combined["Dws"].astype(float)

    # create main plot
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(19, 9))
    # loop through each profile to add to subplots
    for i, ax in enumerate(fig.axes):
        profile = profile_names[i]
        plot_models(ax, df_combined, profile)

    # create main plot
    fig, ax = plt.subplots(figsize=(19, 9))
    for key in profiles:
        plot_path_profiles(vel_file, key, profiles[key], ax)

    plt.show()


# run main()
if __name__ == "__main__":
    vel_file = "/Users/khangvo/Downloads/tomoDD.vel.001.025"

    main(vel_file)
