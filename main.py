# Project Name: Puerto Rico Project
# Author: Khang Vo
# Date Created: 9/19/2021
# Date Last Modified: 10/01/2021
# Python Version: 3.9

import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import reformat_hdf_res
import study_area_constraint
import plot_statistics


# main function:
def main():

    # user specified working directory
    raw_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/01_raw"
    reformatted_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/02_reformatted"
    study_area_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/03_study_area"

    # user specified year range of data
    year_min = 2000
    year_max = 2018
    year_range = np.arange(year_min, year_max + 1, 1)

    # user specified study area data extent
    lon_min = -69
    lon_max = -60
    lat_min = 16
    lat_max = 21

    # run reformat_hdf_res module
    reformat_hdf_res.main(raw_path, reformatted_path, year_range)

    # run data_constraints module
    study_area_constraint.main(reformatted_path, study_area_path, lon_min, lon_max, lat_min, lat_max, year_range)

    # run plot_stats module
    plot_statistics.main(study_area_path, year_range)


# run main()
if __name__ == "__main__":

    # start timer
    time_start = time.perf_counter()

    main()

    # end timer
    time_end = time.perf_counter()
    time_total = time_end - time_start
    print("Elapsed time: " + str(time_total) + " seconds")
