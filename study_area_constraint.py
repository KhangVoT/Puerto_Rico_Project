# File Name: study_area_constraint
# Author: Khang Vo
# Date Created: 9/24/2021
# Date Last Modified: 9/25/2021
# Python Version: 3.9

import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# function to constrain hdf DataFrame to study area
def study_area_hdf(df, lon_min, lon_max, lat_min, lat_max):

    df_zoned = df[(df["glon"].astype(float) >= lon_min) & (df["glon"].astype(float) <= lon_max) &
                  (df["glat"].astype(float) >= lat_min) & (df["glat"].astype(float) <= lat_max)]

    return df_zoned


# function to constrain hdf DataFrame to study area
def study_area_res(df, lon_min, lon_max, lat_min, lat_max):

    # ____________________________need to convert geographic coordinates to geodetic ___________________________________
    lon_min *= 1  # do math here
    lon_max *= 1  # do math here
    lat_min *= 1  # do math here
    lat_max *= 1  # do math here

    df_zoned = df[(df["elon"].astype(float) >= lon_min) & (df["elon"].astype(float) <= lon_max) &
                  (df["elat"].astype(float) >= lat_min) & (df["elat"].astype(float) <= lat_max)]

    return df_zoned


# function to write DataFrame to text file
def output_df(path, df, file_name):

    # output re-formated df to TXT file
    outfile_hdf = path + "/study_area_" + file_name[11:15] + ".txt"
    df.to_csv(outfile_hdf, sep="\t", index=False)


# function to write merged DataFrame to text file
def output_merged_df(path, year_range):

    # define file list, and df list
    file_list = sorted(os.listdir(path))
    df_list = []

    # merge df
    for file in file_list:
        if file.endswith(".txt") and int(file[11:15]) in year_range:
            df_list.append(pd.read_csv(path + "/" + file, sep="\t"))
    df_merged = pd.concat(df_list)

    # output merged df to TXT file
    outfile_merged_hdf = path + "/merged_" + str(min(year_range)) + "-" + str(max(year_range)) + ".txt"
    df_merged.to_csv(outfile_merged_hdf, sep="\t", index=False)


# main function
def main(reformatted_path, study_area_path, lon_min, lon_max, lat_min, lat_max, year_range):

    # changing to working directory and list all HDF/RES files
    os.chdir(reformatted_path)
    file_list = sorted(os.listdir())

    # iterate through files in file list
    for file in file_list:
        if "_hdf" in file and int(file[11:15]) in year_range:
            df_hdf = pd.read_csv(file, sep="\t")
            df_hdf_study = study_area_hdf(df_hdf, lon_min, lon_max, lat_min, lat_max)
            output_df(study_area_path, df_hdf_study, file)
        # elif "_res" in file and int(file[11:15]) in year_range:
        #     df_res = pd.read_csv(file, sep="\t")
        #     df_res_study = study_area_hdf(df_res, lon_min, lon_max, lat_min, lat_max)
        #     output_df(study_area_path, df_res_study, file)

    output_merged_df(study_area_path, year_range)


# run main()
if __name__ == "__main__":

    # user specified working directory
    input_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/02_reformatted"
    output_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/03_study_area"

    # user specified year range of data
    year_min = 2000
    year_max = 2018
    year_range = np.arange(year_min, year_max + 1, 1)

    # user specified study area data extent
    lon_min = -69
    lon_max = -60
    lat_min = 16
    lat_max = 21

    main(input_path, output_path, lon_min, lon_max, lat_min, lat_max, year_range)
