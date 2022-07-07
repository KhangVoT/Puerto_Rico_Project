# File Name: create_interpolated_velocity_file
# Author: Khang Vo
# Date Created: 6/5/2022
# Date Last Modified: 6/5/2022
# Python Version: 3.9

import os
import pandas as pd
import numpy as np
from scipy.interpolate import interpn


def create_model(mit_file):
    df = pd.read_csv(mit_file, delim_whitespace=True)

    # Extract the list of coordinates
    xs = np.array(df["Lat"].to_list())
    ys = np.array(df["Long"].to_list())
    zs = np.array(df["Depth"].to_list())
    # Extract the associated velocity values
    vs = np.array(df["dVp"].to_list())

    px, ix = np.unique(xs, return_inverse=True)
    py, iy = np.unique(ys, return_inverse=True)
    pz, iz = np.unique(zs, return_inverse=True)

    points = (px, py, pz)

    values = np.empty_like(vs, shape=(px.size, py.size, pz.size))
    values[ix, iy, iz] = vs

    return points, values


def interp(points, values, mit_file):

    # Create desired coordinates
    lat_request = np.arange(-90, 90 + 1, 5)
    long_request = np.arange(0, 360 + 1, 5)
    depth_request = np.arange(25, 1825 + 1, 100)

    if ".txt" in mit_file:
        with open(mit_file, "r") as infile:
            header = next(infile)
            with open(mit_file[0:-4] + "_interp.txt", "w") as outfile:
                outfile.write(header)
                for depth in depth_request:
                    for long in long_request:
                        for lat in lat_request:
                            outfile.write(str(format(lat, ".2f")))
                            outfile.write("\t")
                            outfile.write(str(format(long, ".2f")))
                            outfile.write("\t")
                            outfile.write(str(format(depth, ".1f")))
                            outfile.write("\t")

                            dvp_request = np.array([lat, long, depth])
                            dvp = interpn(points, values, dvp_request, method="linear", bounds_error=False,
                                          fill_value=None)
                            outfile.write(str(format(float(dvp), ".2f")))
                            outfile.write("\n")


def main():
    mit_file = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/_v_list/ggge1202-sup-0002-ds01.txt"

    points, values = create_model(mit_file)

    interp(points, values, mit_file)


if __name__ == "__main__":
    main()
