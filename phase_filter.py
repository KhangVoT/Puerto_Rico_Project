# File Name: phase_filter
# Author: Khang Vo
# Date Created: 2/14/2022
# Date Last Modified: 2/14/2022
# Python Version: 3.9

import os
import glob
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# main function:
def main(study_area_path, phase_filter_path):

    # changing to working directory
    os.chdir(study_area_path + "/res")
    file_list = sorted(os.listdir())

    # iterate through files in file list
    for file in file_list:
        if "merged" in file:
            df = pd.read_csv(file, sep="\t", low_memory=False)
            dfP = df.loc[df["phasej"].str.strip() == "P"]
            dfP.to_csv(phase_filter_path + "/P_filter.txt", sep="\t")
            nP = len(pd.unique(dfP['sta']))
            ievtP = len(pd.unique(dfP['ievt']))
            print("number of P events = " + str(ievtP))
            print("number of P phases = " + str(len(dfP)))
            print("number of P stations = " + str(nP))

            dfS = df.loc[df["phasej"].str.strip() == "S"]
            dfS.to_csv(phase_filter_path + "/S_filter.txt", sep="\t")
            nS = len(pd.unique(dfS['sta']))
            ievtS = len(pd.unique(dfS['ievt']))
            print("number of S events = " + str(ievtS))
            print("number of S phases = " + str(len(dfS)))
            print("number of S stations = " + str(nS))


# run main()
if __name__ == "__main__":

    # user specified working directory
    input_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/03_study_area"
    output_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/04_phase_filter"

    main(input_path, output_path)
