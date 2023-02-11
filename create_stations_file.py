# File Name: create_stations_file
# Author: Khang Vo
# Date Created: 2/15/2022
# Date Last Modified: 3/7/2022
# Python Version: 3.9

import os
import glob
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# main function:
def main(stations_path, teletomoDD_file_path, lon_min, lon_max, lat_min, lat_max):

    sta = pd.read_csv(stations_path + "/stations_ehb.txt",
                      delim_whitespace=True, skiprows=3, skipfooter=5, engine="python")

    sta.columns = ["sta", "slat", "slon", "elev", "status"]

    sta.drop(["status"], axis=1, inplace=True)

    for i in range(len(sta)):
        if sta.loc[i, "slon"] > 180:
            sta.loc[i, "slon"] = sta.loc[i, "slon"] - 360

    sta = sta.round({"slon": 2, "slat": 2})

    sta.to_csv(teletomoDD_file_path + "/sta_glb.txt", sep="\t", index=False, header=False)

    sta_zoned = sta[(sta["slon"].astype(float) >= lon_min) & (sta["slon"].astype(float) <= lon_max) &
                    (sta["slat"].astype(float) >= lat_min) & (sta["slat"].astype(float) <= lat_max)]

    sta_zoned = sta_zoned.round({"slon": 2, "slat": 2})

    sta_zoned.to_csv(teletomoDD_file_path + "/sta_reg.txt", sep="\t", index=False, header=False)


# run main()
if __name__ == "__main__":

    # user specified study area data extent
    lon_min = -80
    lon_max = -55
    lat_min = 5
    lat_max = 25

    # user specified working directory
    input_path = "/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/_stations_list"
    output_path = "/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/04_TeletomoDD_files"

    main(input_path, output_path, lon_min, lon_max, lat_min, lat_max)
