# File Name: merge_event_files
# Author: Khang Vo
# Date Created: 11/22/2022
# Date Last Modified: 2/27/2023
# Python Version: 3.9

import os
import glob
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv


def combine_event(teletomoDD_file_path):
    # define file list, and df list
    file_list = sorted(os.listdir(teletomoDD_file_path))

    # merge df
    if "sta_glb_event.txt" in file_list and "sta_reg_event.txt" in file_list:
        df_glb = pd.read_csv(teletomoDD_file_path + "/sta_glb_event.txt", delim_whitespace=True, header=None)
        df_reg = pd.read_csv(teletomoDD_file_path + "/sta_reg_event.txt", delim_whitespace=True, header=None)
        df_merged = pd.concat([df_glb, df_reg])

        # output merged df to TXT file
        df_merged_path = teletomoDD_file_path + "/master_event.txt"
        df_merged.to_csv(df_merged_path, sep="\t", index=False, header=False)


def combine_abs(teletomoDD_file_path):
    # define file list, and df list
    file_list = sorted(os.listdir(teletomoDD_file_path))

    # merge df
    if "sta_glb_obs.txt" in file_list and "sta_reg_obs.txt" in file_list:
        df_glb = pd.read_csv(teletomoDD_file_path + "/sta_glb_obs.txt", header=None, low_memory=False)
        df_reg = pd.read_csv(teletomoDD_file_path + "/sta_reg_obs.txt", header=None, low_memory=False)
        df_merged = pd.concat([df_glb, df_reg])

        # output merged df to TXT file
        df_merged_path = teletomoDD_file_path + "/master_obs.txt"
        df_merged.to_csv(df_merged_path, index=False, header=False, quoting=csv.QUOTE_NONE, escapechar=" ")

def main(teletomoDD_file_path):
    combine_event(teletomoDD_file_path)

    combine_abs(teletomoDD_file_path)


# run main()
if __name__ == "__main__":
    # user specified working directory
    input_path = "/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/04_TeletomoDD_files"

    main(input_path)
