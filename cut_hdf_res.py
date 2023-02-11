# File Name: cut_hdf_res
# Author: Khang Vo
# Date Created: 10/2/2022
# Date Last Modified: 11/13/2022
# Python Version: 3.9

import os
import glob
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def cut_res(res_path, stations_path, ievt, year_range):
    # define file list, and df list
    file_list = sorted(os.listdir(res_path))
    df_list = []

    sta_type = stations_path[-11:-4]

    # merge df
    for file in file_list:
        if sta_type + "_event" in file and int(file[-12:-8]) in year_range:
            df_res = pd.read_csv(res_path + "/" + file, sep="\t", low_memory=False)
            df_res_zoned = df_res.loc[df_res["ievt"].isin(ievt)]
            df_list.append(df_res_zoned)
    res_merged = pd.concat(df_list)

    # output merged df to TXT file
    res_merged_path = res_path + "/merged_" + sta_type + "_" + str(min(year_range)) + "-" + str(max(year_range)) + "_res.txt"
    res_merged.to_csv(res_merged_path, sep="\t", index=False)


def cut_hdf(hdf_path, stations_path, lon_min, lon_max, lat_min, lat_max, year_range):
    # define file list, and df list
    file_list = sorted(os.listdir(hdf_path))
    df_list = []

    sta_type = stations_path[-11:-4]

    # merge df
    for file in file_list:
        if sta_type + "_event" in file and int(file[-12:-8]) in year_range:
            df_hdf = pd.read_csv(hdf_path + "/" + file, sep="\t", low_memory=False)
            if sta_type == "sta_reg":
                df_hdf_zoned = df_hdf[
                    (df_hdf["glon"].astype(float) <= lon_min) | (df_hdf["glon"].astype(float) >= lon_max) |
                    (df_hdf["glat"].astype(float) <= lat_min) | (df_hdf["glat"].astype(float) >= lat_max)]
                df_list.append(df_hdf_zoned)
            elif stations_path[-11:-4] == "sta_glb":
                df_hdf_zoned = df_hdf[(df_hdf["glon"].astype(float) >= lon_min) & (df_hdf["glon"].astype(float) <= lon_max) &
                                      (df_hdf["glat"].astype(float) >= lat_min) & (df_hdf["glat"].astype(float) <= lat_max)]
                df_list.append(df_hdf_zoned)
    hdf_merged = pd.concat(df_list)

    ievt = hdf_merged["ievt"].drop_duplicates().tolist()

    # output merged df to TXT file
    hdf_merged_path = hdf_path + "/merged_" + sta_type + "_" + str(min(year_range)) + "-" + str(max(year_range)) + "_hdf.txt"
    hdf_merged.to_csv(hdf_merged_path, sep="\t", index=False)

    return ievt


def main(study_area_path, stations_path, lon_min, lon_max, lat_min, lat_max, year_range):
    ievt = cut_hdf(study_area_path + "/hdf", stations_path, lon_min, lon_max, lat_min, lat_max, year_range)

    cut_res(study_area_path + "/res", stations_path, ievt, year_range)


# run main()
if __name__ == "__main__":
    # user specified working directory
    input_path = "/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/03_study_area"
    stations_path = "/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/05_TeletomoDD_files/sta_reg.txt"

    # user specified year range of data
    year_min = 1964
    year_max = 2018
    year_range = np.arange(year_min, year_max + 1, 1)

    # user specified study area data extent
    lon_min = -80
    lon_max = -55
    lat_min = 5
    lat_max = 25
    depth_min = 10
    depth_max = 250

    main(input_path, stations_path, lon_min, lon_max, lat_min, lat_max, year_range)
