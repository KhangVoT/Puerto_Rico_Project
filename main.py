# Project Name: Puerto Rico Project
# Author: Khang Vo
# Date Created: 9/19/2021
# Date Last Modified: 2/13/2022
# Python Version: 3.9

import os
import glob
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import reformat_hdf_res
import study_area_hdf
import study_area_res
import phase_filter
import create_stations_file
import create_event_files
import create_velocity_files
import plot_statistics


# main function:
def main():

    # user specified working directory
    stations_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/_stations_list"
    raw_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/01_raw"
    reformatted_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/02_reformatted"
    study_area_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/03_study_area"
    phase_filter_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/04_phase_filter"
    ak135_file = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/_v_list/ak135.txt"
    mit_file = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/_v_list/ggge1202-sup-0002-ds01.txt"
    teletomoDD_file_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/05_TeletomoDD_files"

    # user specified year range of data
    year_min = 2000
    year_max = 2018
    year_range = np.arange(year_min, year_max + 1, 1)

    # user specified study area data extent
    lon_min = -80
    lon_max = -55
    lat_min = 5
    lat_max = 25

    # # run reformat_hdf_res module
    # reformat_hdf_res.main(raw_path, reformatted_path, year_range)
    #
    # # run study_area_hdf module
    # study_area_hdf.main(reformatted_path, study_area_path, lon_min, lon_max, lat_min, lat_max, year_range)
    #
    # # run study_area_res module
    # study_area_res.main(reformatted_path, study_area_path, year_range)

    # # run phase_filter module
    # phase_filter.main(study_area_path, phase_filter_path)

    # # run create_stations_file
    # create_stations_file.main(stations_path, teletomoDD_file_path, lon_min, lon_max, lat_min, lat_max)
    #
    # # run create_event_files all1a
    # create_event_files.all1a(study_area_path + "/hdf", teletomoDD_file_path)
    #
    # # run create_event_files all1
    # create_event_files.all1(phase_filter_path, teletomoDD_file_path)
    #
    # # run create_velocity_files.glb
    # create_velocity_files.glb(ak135_file, mit_file, teletomoDD_file_path)
    #
    # # run create_velocity_files.reg
    # create_velocity_files.reg(ak135_file, mit_file, teletomoDD_file_path, lon_min, lon_max, lat_min, lat_max)

    # # run plot_statistics module
    # plot_statistics.main(study_area_path, year_range)


# run main()
if __name__ == "__main__":

    # start timer
    time_start = time.perf_counter()

    main()

    # end timer
    time_end = time.perf_counter()
    time_total = time_end - time_start
    print("Elapsed time: " + str(time_total) + " seconds")
