# File Name: create_event_files
# Author: Khang Vo
# Date Created: 3/6/2022
# Date Last Modified: 11/13/2022
# Python Version: 3.9

import os
import glob
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# event function
def event(hdf_path, output_path):

    file_list = sorted(os.listdir(hdf_path))

    # iterate through files in file list and read only merged file
    for file in file_list:
        if "merge" in file:
            df_hdf = pd.read_csv(hdf_path + "/" + file, sep="\t", low_memory=False)

            c_hdf = df_hdf[["iyr", "mon", "iday", "ihr", "min", "sec", "glat", "glon", "depth", "ievt", "mb"]]

            c_hdf.to_csv(output_path + "/temp_event.txt", sep="\t", index=False)

            with open(output_path + "/temp_event.txt", "r") as infile:
                with open(output_path + "/" + file[7:14] + "_event.txt", "w") as outfile:
                    # outfile.write("iyr" + "\t")
                    # outfile.write("mon" + "\t")
                    # outfile.write("iday" + "\t")
                    # outfile.write("ihr" + "\t")
                    # outfile.write("min" + "\t")
                    # outfile.write("sec" + "\t")
                    # outfile.write("glat" + "\t")
                    # outfile.write("glon" + "\t")
                    # outfile.write("depth" + "\t")
                    # outfile.write("ievt" + "\t")
                    # outfile.write("mb" + "\n")
                    next(infile)
                    for line in infile:
                        fields = line.split()
                        iyr = fields[0]
                        mon = fields[1]
                        iday = fields[2]
                        ihr = fields[3]
                        min = fields[4]
                        sec = fields[5]
                        glat = fields[6]
                        glon = fields[7]
                        depth = fields[8]
                        ievt = fields[9]
                        mb = fields[10]
                        outfile.write(str(iyr).zfill(2) + str(mon).zfill(2) + str(iday).zfill(2) + "\t")
                        outfile.write(str(ihr).zfill(2) + str(min).zfill(2) + str(format(float(sec), ".2f").zfill(5)) + "\t")
                        outfile.write(glat + "\t")
                        outfile.write(glon + "\t")
                        outfile.write(depth + "\t")
                        outfile.write(mb + "\t")
                        outfile.write("0.0" + "\t" + "0.0" + "\t" + "0.0" + "\t")
                        outfile.write(ievt + "\t")
                        outfile.write("0" + "\n")

            os.remove(output_path + "/temp_event.txt")


# abs function
def obs(res_path, output_path):
    file_list = sorted(os.listdir(res_path))

    # iterate through files in file list and read only merged file
    for file in file_list:
        if "merge" in file:
            df_res = pd.read_csv(res_path + "/" + file, sep="\t", low_memory=False)

            c_res = df_res[["sta", "ttime", "wgt", "phasej", "ievt"]]

            c_res.to_csv(output_path + "/temp_abs.txt", sep="\t", index=False)

            ievt_seen = set()

            with open(output_path + "/temp_abs.txt", "r") as infile:
                with open(output_path + "/" + file[7:14] + "_obs.txt", "w") as outfile:
                    # outfile.write("sta" + "\t")
                    # outfile.write("ttime" + "\t")
                    # outfile.write("wgt" + "\t")
                    # outfile.write("phasej" + "\n")
                    next(infile)
                    for line in infile:
                        fields = line.split()
                        sta = fields[0]
                        ttime = fields[1]
                        wgt = fields[2]
                        phasej = fields[3]
                        ievt = fields[4]
                        if ievt not in ievt_seen:
                            outfile.write("# " + ievt + "\n")
                            ievt_seen.add(ievt)
                        outfile.write(sta + "\t")
                        outfile.write(ttime + "\t")
                        outfile.write(wgt + "\t")
                        outfile.write(phasej + "\n")

            os.remove(output_path + "/temp_abs.txt")


if __name__ == "__main__":

    # user specified working directory
    input_path = "/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/03_study_area"
    output_path = "/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/04_TeletomoDD_files"

    event(input_path + "/hdf", output_path)
    obs(input_path + "/res", output_path)
