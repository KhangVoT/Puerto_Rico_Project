# Project Name: Puerto Rico Project
# Author: Khang Vo
# Date Created: 9/19/2021
# Date Last Modified: 1/27/2023
# Python Version: 3.9

import os
import glob
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import create_stations_file
import reformat_hdf_res
import study_area_res
import study_area_hdf
# import phase_filter
import cut_hdf_res
import create_event_files
import merge_event_files
import create_velocity_files


# main function:
def main():

    # user specified working directory
    ak135_file = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/_v_list/ak135.txt"
    mit_file = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/_v_list/ggge1202-sup-0002-ds01.txt"
    stations_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/_stations_list"
    raw_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/01_raw"
    reformatted_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/02_reformatted"
    study_area_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/03_study_area"
    teletomoDD_file_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/04_TeletomoDD_files"

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

    # user specified steps for coordinate interpolation
    long_step_glb = 5
    lat_step_glb = 5
    depth_step_glb = 200
    long_step_reg = 0.5
    lat_step_reg = 0.5
    depth_step_reg = 10

    # # run create_stations_file module
    # create_stations_file.main(stations_path, teletomoDD_file_path, lon_min, lon_max, lat_min, lat_max)

    # # run reformat_hdf_res module
    # reformat_hdf_res.main(raw_path, reformatted_path, year_range)

    # run study_area_res module
    study_area_res.main(reformatted_path + "/res", study_area_path, teletomoDD_file_path + "/sta_glb.txt", year_range)

    # run study_area_hdf module
    study_area_hdf.main(reformatted_path + "/hdf", study_area_path, teletomoDD_file_path + "/sta_glb.txt", year_range)

    # run cut_hdf_res module
    cut_hdf_res.main(study_area_path, teletomoDD_file_path + "/sta_glb.txt", lon_min, lon_max, lat_min, lat_max, year_range)

    # run create_event_files event module
    create_event_files.event(study_area_path + "/hdf", teletomoDD_file_path)

    # run create_event_files obs module
    create_event_files.obs(study_area_path + "/res", teletomoDD_file_path)

    # run merge_event_files module
    merge_event_files.main(teletomoDD_file_path)

    # run create_velocity_files module
    create_velocity_files.main(ak135_file, mit_file, teletomoDD_file_path, lon_min, lon_max, lat_min, lat_max,
                               depth_min, depth_max, long_step_glb, lat_step_glb, depth_step_glb, long_step_reg,
                               lat_step_reg, depth_step_reg)


# run main()
if __name__ == "__main__":

    # start timer
    time_start = time.perf_counter()

    main()

    # end timer
    time_end = time.perf_counter()
    time_total = time_end - time_start
    print("Elapsed time: " + str(time_total) + " seconds")
