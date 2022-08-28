# File Name: study_area_res
# Author: Khang Vo
# Date Created: 2/13/2022
# Date Last Modified: 2/13/2022
# Python Version: 3.9

import os
import glob
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# function to constrain RES DataFrame to study area
def study_area_res(df, ievt):

    df_zoned = df.loc[df["ievt"].isin(ievt)]

    return df_zoned


# function to write DataFrame to text file
def output_df(path, df, file_name):

    # output re-formated df to TXT file
    outfile_hdf = path + "/res/study_area_" + file_name[11:15] + "_res.txt"
    df.to_csv(outfile_hdf, sep="\t", index=False)


# function to write merged DataFrame to text file
def output_merged_df(path, year_range):

    # define file list, and df list
    file_list = sorted(os.listdir(path + "/res"))
    df_list = []

    # merge df
    for file in file_list:
        if file.endswith(".txt") and int(file[11:15]) in year_range:
            df_list.append(pd.read_csv(path + "/res/" + file, sep="\t", low_memory=False))
    df_merged = pd.concat(df_list)

    # output merged df to TXT file
    outfile_merged_hdf = path + "/res/merged_" + str(min(year_range)) + "-" + str(max(year_range)) + "_res.txt"
    df_merged.to_csv(outfile_merged_hdf, sep="\t", index=False)


# main function
def main(reformatted_path, study_area_path, year_range):

    # collect ievt from combined HDF file to match to all RES files
    df_study = pd.read_csv(study_area_path + "/hdf/merged_" + str(min(year_range)) + "-" + str(max(year_range)) +
                           "_hdf.txt", sep="\t", low_memory=False)
    ievt = df_study["ievt"].tolist()

    # changing to working directory and list all HDF/RES files
    os.chdir(reformatted_path + "/res")
    file_list = sorted(os.listdir())

    # iterate through files in file list
    for file in file_list:
        if "_res" in file and int(file[11:15]) in year_range:
            df_res = pd.read_csv(file, sep="\t", low_memory=False)
            df_res_study = study_area_res(df_res, ievt)
            output_df(study_area_path, df_res_study, file)

    output_merged_df(study_area_path, year_range)


# run main()
if __name__ == "__main__":

    # user specified working directory
    input_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/02_reformatted"
    output_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/03_study_area"

    # user specified year range of data
    year_min = 1964
    year_max = 2018
    year_range = np.arange(year_min, year_max + 1, 1)

    main(input_path, output_path, year_range)
