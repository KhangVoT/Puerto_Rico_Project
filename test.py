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


def interp(points, values):

    # Create desired coordinates
    lat_request = np.arange(-90, 90 + 1, 5)
    long_request = np.arange(-180, 180 + 1, 5)
    depth_request = np.arange(25, 1825 + 1, 100)

    px, ix = np.unique(lat_request, return_inverse=True)
    py, iy = np.unique(long_request, return_inverse=True)
    pz, iz = np.unique(depth_request, return_inverse=True)

    # request = (px, py, pz)
    # print(request)

    # test
    request = np.array([-40, 0, 25])

    output = interpn(points, values, request, method="linear", bounds_error=False, fill_value=None)

    return output


def main():
    mit_file = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/_v_list/ggge1202-sup-0002-ds01.txt"

    points, values = create_model(mit_file)

    output = interp(points, values)
    print(output)


if __name__ == "__main__":
    main()
