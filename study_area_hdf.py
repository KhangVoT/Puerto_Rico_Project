# File Name: study_area_hdf
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
def study_area_hdf(df, ievt):

    df_zoned = df.loc[df["ievt"].isin(ievt)]

    return df_zoned


# function to write DataFrame to text file
def output_df(study_area_path, stations_path, df, file_name):
    sta_type = stations_path[-11:-4]

    # output re-formated df to TXT file
    outfile_hdf = study_area_path + "/hdf/" + sta_type + "_event_" + file_name[11:15] + "_hdf.txt"

    df.to_csv(outfile_hdf, sep="\t", index=False)


# main function
def main(reformatted_path, study_area_path, stations_path, year_range):
    file_list = sorted(os.listdir(study_area_path + "/res"))
    df_list = []

    sta_type = stations_path[-11:-4]

    # get all ievt from RES files
    for file in file_list:
        if sta_type + "_event" in file and int(file[-12:-8]) in year_range:
            df = pd.read_csv(study_area_path + "/res" + "/" + file, sep="\t", low_memory=False, usecols=["ievt"]).drop_duplicates()
            df_list.append(df)
    df_merged = pd.concat(df_list)
    ievt = df_merged["ievt"].tolist()

    # changing to working directory and list all HDF/RES files
    os.chdir(reformatted_path)
    file_list = sorted(os.listdir())

    # iterate through files in file list
    for file in file_list:
        if "_hdf" in file and int(file[-12:-8]) in year_range:
            df_hdf = pd.read_csv(file, sep="\t")
            df_hdf_study = study_area_hdf(df_hdf, ievt)
            output_df(study_area_path, stations_path, df_hdf_study, file)


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
