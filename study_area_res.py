# File Name: study_area_res
# Author: Khang Vo
# Date Created: 2/13/2022
# Date Last Modified: 1/27/2023
# Python Version: 3.9

import os
import glob
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# function to constrain RES DataFrame to study area
def study_area_res(df, sta):

    df_zoned = df.loc[df["sta"].str.strip().isin(sta)]

    return df_zoned


# function to write merged DataFrame to text file
def output_df(study_area_path, stations_path, df, file_name):
    sta_type = stations_path[-11:-4]

    # output re-formated df to TXT file
    outfile_res = study_area_path + "/res/" + sta_type + "_event_" + file_name[11:15] + "_res.txt"
    df.to_csv(outfile_res, sep="\t", index=False)


# main function
def main(reformatted_path, study_area_path, stations_path, year_range):

    # collect sta from sta_reg file
    df_sta = pd.read_csv(stations_path, sep="\t", header=None)
    df_sta.columns = ["sta", "lon", "lat", "elev"]
    sta = df_sta["sta"].tolist()

    # changing to working directory and list all HDF/RES files
    os.chdir(reformatted_path)
    file_list = sorted(os.listdir())

    # iterate through files in file list
    for file in file_list:
        if "_res" in file and int(file[11:15]) in year_range:
            df_res = pd.read_csv(file, sep="\t", low_memory=False)
            df_res_p = df_res.loc[df_res["phasej"].str.strip() == "P"]
            df_res_study = study_area_res(df_res_p, sta)
            output_df(study_area_path, stations_path, df_res_study, file)


# run main()
if __name__ == "__main__":

    # user specified working directory
    input_path = "/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/02_reformatted"
    output_path = "/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/03_study_area"
    stations_path = "/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/04_TeletomoDD_files/sta_reg.txt"

    # user specified year range of data
    year_min = 1964
    year_max = 2018
    year_range = np.arange(year_min, year_max + 1, 1)

    main(input_path, output_path, stations_path, year_range)
