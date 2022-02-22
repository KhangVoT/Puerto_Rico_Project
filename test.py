import os
import glob
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# user specified working directory
hdf_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/03_study_area/hdf"
res_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/04_phase_filter"
output_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/05_TeletomoDD_files"

# create all1a.txt file
df_hdf = pd.read_csv(hdf_path + "/merged_2000-2018_hdf.txt", sep="\t", low_memory=False)

c_hdf = df_hdf[["iyr", "mon", "iday", "ihr", "min", "sec", "glat", "glon", "depth", "mb"]]

c_hdf.to_csv(output_path + "/temp_all1a.txt", sep="\t", index=False)

with open(output_path + "/temp_all1a.txt", "r") as infile:
    with open(output_path + "/all1a.txt", "w") as outfile:
        # outfile.write("iyr" + "\t")
        # outfile.write("mon" + "\t")
        # outfile.write("iday" + "\t")
        # outfile.write("ihr" + "\t")
        # outfile.write("min" + "\t")
        # outfile.write("sec" + "\t")
        # outfile.write("glat" + "\t")
        # outfile.write("glon" + "\t")
        # outfile.write("depth" + "\t")
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
            mb = fields[9]
            outfile.write(str(iyr).zfill(2) + str(mon).zfill(2) + str(iday).zfill(2) + "\t")
            outfile.write(str(ihr).zfill(2) + str(min).zfill(2) + str(format(float(sec), ".2f").zfill(5)) + "\t")
            outfile.write(glat + "\t")
            outfile.write(glon + "\t")
            outfile.write(depth + "\t")
            outfile.write(mb + "\t")
            outfile.write("0.0" + "\t" + "0.0" + "\t" + "0.0" + "\t")
            outfile.write("0" + "\t" + "0" + "\n")

os.remove(output_path + "/temp_all1a.txt")

# create all1.txt file
df_res = pd.read_csv(res_path + "/P_filter.txt", sep="\t", low_memory=False)

c_res = df_res[["sta", "ttime", "wgt", "phasej", "ievt"]]

c_res.to_csv(output_path + "/temp_all1.txt", sep="\t", index=False)

ievt_seen = set()

with open(output_path + "/temp_all1.txt", "r") as infile:
    with open(output_path + "/all1.txt", "w") as outfile:
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
                outfile.write(ievt + "\n")
                ievt_seen.add(ievt)
            outfile.write(sta + "\t")
            outfile.write(ttime + "\t")
            outfile.write(wgt + "\t")
            outfile.write(phasej + "\n")

os.remove(output_path + "/temp_all1.txt")
