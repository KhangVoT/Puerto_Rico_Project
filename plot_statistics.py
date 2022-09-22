# File Name: plot_statistics
# Author: Khang Vo
# Date Created: 9/24/2021
# Date Last Modified: 9/21/2022
# Python Version: 3.9

import os
import glob
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# function to import reformatted HDF and plotting statistics
def plot_stats(file_list, year_range):

    # read merged study area TXT file
    for file in file_list:
        if "merged" in file:
            df = pd.read_csv(file, sep="\t")

            # plot 1 with 2 subplots
            fig, axes = plt.subplots(1, 2)

            # subplot 1/2
            df["mon"].value_counts().sort_index().plot(kind="bar", ax=axes[0],
                                                       title="# Earthquakes/month from " + str(min(year_range)) + "-" +
                                                             str(max(year_range)), xlabel="Month", ylabel="# events")

            # subplot 2/2
            df.plot(x="mon", y="mb", kind="scatter", ax=axes[1],
                    title="Earthquake magnitudes from " + str(min(year_range)) + "-" + str(max(year_range)),
                    xlabel="Month", ylabel="Magnitude")

            plt.show()


# main function
def main(study_area_path, year_range):

    # changing to working directory and list all HDF/RES files
    os.chdir(study_area_path)
    file_list = sorted(os.listdir())

    plot_stats(file_list, year_range)


# run main()
if __name__ == "__main__":

    # user specified working directory
    input_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/03_study_area/hdf"

    # user specified year range of data
    year_min = 2000
    year_max = 2018
    year_range = np.arange(year_min, year_max + 1, 1)

    main(input_path, year_range)
