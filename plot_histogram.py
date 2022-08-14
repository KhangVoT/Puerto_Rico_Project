# File Name: plot_histogram
# Author: Khang Vo
# Date Created: 8/13/2022
# Date Last Modified: 8/14/2022
# Python Version: 3.9

import os
import glob
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main(event_file):
    df = pd.read_csv(event_file, sep="\t", header=None)
    df.columns = ["yymmdd", "hhmmss", "glat", "glon", "depth", "mb", "num1", "num2", "num3", "ievt", "num4"]

    fig, ax = plt.subplots(figsize=(10, 6))

    df["depth"].hist(ax=ax, bins=50, color="red", alpha=0.5, histtype="bar", edgecolor="black")

    ax.set_title("Histogram of Earthquake Depths")
    ax.set_xlabel("Depth (km)")
    ax.set_ylabel("Number of Events")

    plt.show()


# run main()
if __name__ == "__main__":

    # user specified working directory
    event_file = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/05_TeletomoDD_files/event.txt"

    depth_list = [22.6, 338.8, 745.5]

    main(event_file)
