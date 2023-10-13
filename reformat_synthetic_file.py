# File Name: reformat_synthetic_file
# Author: Khang Vo
# Date Created: 3/13/2023
# Date Last Modified: 3/13/2023
# Python Version: 3.10

import os
import glob
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def obs(input_file, output_path):
    df_res = pd.read_csv(input_file, delim_whitespace=True)
    df_res.columns = ["ievt", "sta", "ttime", "wgt", "phasej"]

    c_res = df_res[["ievt", "sta", "ttime", "wgt", "phasej"]]

    c_res.to_csv(output_path + "/temp_abs.txt", sep="\t", index=False)

    ievt_seen = set()

    with open(output_path + "/temp_abs.txt", "r") as infile:
        with open(output_path + "/syn_obs.txt", "w") as outfile:
            # outfile.write("sta" + "\t")
            # outfile.write("ttime" + "\t")
            # outfile.write("wgt" + "\t")
            # outfile.write("phasej" + "\n")
            next(infile)
            for line in infile:
                fields = line.split()
                ievt = fields[0]
                sta = fields[1]
                ttime = fields[2]
                wgt = fields[3]
                phasej = fields[4]
                if ievt not in ievt_seen:
                    outfile.write("# " + ievt + "\n")
                    ievt_seen.add(ievt)
                outfile.write(sta + "\t")
                outfile.write(ttime + "\t")
                outfile.write(wgt + "\t")
                outfile.write(phasej + "\n")

    os.remove(output_path + "/temp_abs.txt")


if __name__ == "__main__":
    input_file = "/Users/khangvo/Downloads/absolute.syn"
    output_path = "/Users/khangvo/Downloads"
    obs(input_file, output_path)
