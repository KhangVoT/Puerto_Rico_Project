# File Name: reformat_hdf_res
# Author: Khang Vo
# Date Created: 9/19/2021
# Date Last Modified: 9/22/2021
# Python Version: 3.9

import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# function to import and read HDF files
def import_hdf(file_list, year):

    # setting file name
    file = str(year) + ".hdf"

    # read only HDF files in file list
    if file in file_list:
        df_tmp = pd.read_csv(file, header=None)

        # separating variables to different DataFrames
        df_ahyp = df_tmp[0].str[0:1]
        df_isol = df_tmp[0].str[1:4]
        df_iseg11 = df_tmp[0].str[4:5]
        df_iseg22 = df_tmp[0].str[5:6]
        df_iyr = df_tmp[0].str[6:8]
        df_mon = df_tmp[0].str[8:11]
        df_iday = df_tmp[0].str[11:14]
        df_ihr = df_tmp[0].str[15:18]
        df_min = df_tmp[0].str[18:21]
        df_sec = df_tmp[0].str[21:27]
        df_ad = df_tmp[0].str[27:28]
        df_glat = df_tmp[0].str[28:36]
        df_glon = df_tmp[0].str[36:44]
        df_depth = df_tmp[0].str[44:50]
        df_iscdep = df_tmp[0].str[50:56]
        df_mb = df_tmp[0].str[56:60]
        df_ms = df_tmp[0].str[60:64]
        df_mw = df_tmp[0].str[64:68]
        df_ntot = df_tmp[0].str[68:72]
        df_ntel = df_tmp[0].str[72:76]
        df_ndep = df_tmp[0].str[76:80]
        df_igreg = df_tmp[0].str[80:84]
        df_se = df_tmp[0].str[84:92]
        df_ser = df_tmp[0].str[92:100]
        df_sedep = df_tmp[0].str[100:108]
        df_rstadel = df_tmp[0].str[108:114]
        df_openaz1 = df_tmp[0].str[114:120]
        df_openaz2 = df_tmp[0].str[120:126]
        df_az1 = df_tmp[0].str[126:130]
        df_flen1 = df_tmp[0].str[130:134]
        df_az2 = df_tmp[0].str[134:138]
        df_flen2 = df_tmp[0].str[138:142]
        df_avh = df_tmp[0].str[142:147]
        df_ievt = df_tmp[0].str[147:157]

        # merging DataFrames together and set header names
        df_merged = pd.concat([df_ahyp, df_isol, df_iseg11, df_iseg22, df_iyr, df_mon, df_iday, df_ihr, df_min,
                               df_sec, df_ad, df_glat, df_glon, df_depth, df_iscdep, df_mb, df_ms, df_mw, df_ntot,
                               df_ntel, df_ndep, df_igreg, df_se, df_ser, df_sedep, df_rstadel, df_openaz1,
                               df_openaz2, df_az1, df_flen1, df_az2, df_flen2, df_avh, df_ievt], axis=1)
        df_merged.columns = ["ahyp", "isol", "iseg11", "iseg22", "iyr", "mon", "iday", "ihr", "min", "sec", "ad",
                             "glat", "glon", "depth", "iscdep", "mb", "ms", "mw", "ntol", "ntel", "ndep", "igreg",
                             "se", "ser", "sedep", "rstadel", "openaz1", "openaz2", "az1", "flen1", "az2", "flen2",
                             "avh", "ievt"]

        # return merged DataFrame
        return df_merged, file.replace(".", "_")

    else:
        print("No HDF data for selected " + str(year))


# function to import and read RES files
def import_res(file_list, year):

    # setting file name
    file = str(year) + ".res"

    # read only RES files in file list
    if file in file_list:
        df_tmp = pd.read_csv(file, header=None)

        # separating variables to different DataFrames
        df_nev = df_tmp[0].str[0:7]
        df_isol = df_tmp[0].str[8:11]
        df_iseq11 = df_tmp[0].str[11:12]
        df_iseq22 = df_tmp[0].str[12:13]
        df_openaz2 = df_tmp[0].str[13:19]
        df_ropenaz2 = df_tmp[0].str[19:25]
        df_topenaz2 = df_tmp[0].str[25:31]
        df_iyr = df_tmp[0].str[31:36]
        df_imon = df_tmp[0].str[36:39]
        df_iday = df_tmp[0].str[39:42]
        df_ihold = df_tmp[0].str[42:44]
        df_ihr = df_tmp[0].str[44:47]
        df_imin = df_tmp[0].str[47:50]
        df_sec = df_tmp[0].str[50:56]
        df_elat = df_tmp[0].str[56:64]
        df_elon = df_tmp[0].str[64:72]
        df_depth = df_tmp[0].str[72:78]
        df_fmb = df_tmp[0].str[78:82]
        df_fms = df_tmp[0].str[82:86]
        df_ntot = df_tmp[0].str[86:91]
        df_ntel = df_tmp[0].str[91:96]
        df_sta = df_tmp[0].str[102:108]
        df_slat = df_tmp[0].str[108:116]
        df_slon = df_tmp[0].str[116:124]
        df_elev = df_tmp[0].str[124:131]
        df_delta = df_tmp[0].str[131:139]
        df_azim = df_tmp[0].str[139:147]
        df_comp = df_tmp[0].str[153:155]
        df_onset = df_tmp[0].str[156:157]
        df_phasej = df_tmp[0].str[158:166]
        df_iphj = df_tmp[0].str[166:170]
        df_iphi = df_tmp[0].str[170:174]
        df_ipho = df_tmp[0].str[174:178]
        df_rdtdd = df_tmp[0].str[183:191]
        df_rdelta = df_tmp[0].str[191:199]
        df_razim = df_tmp[0].str[199:207]
        df_dbot = df_tmp[0].str[207:214]
        df_gblat = df_tmp[0].str[219:227]
        df_gblon = df_tmp[0].str[227:235]
        df_stadel = df_tmp[0].str[235:243]
        df_bdep = df_tmp[0].str[243:250]
        df_tbath = df_tmp[0].str[250:257]
        df_twater = df_tmp[0].str[257:264]
        df_obstt = df_tmp[0].str[269:279]
        df_iprec = df_tmp[0].str[279:282]
        df_prett = df_tmp[0].str[282:292]
        df_rawres = df_tmp[0].str[292:299]
        df_ecor = df_tmp[0].str[304:311]
        df_scor = df_tmp[0].str[311:318]
        df_elcor = df_tmp[0].str[318:325]
        df_resid = df_tmp[0].str[325:332]
        df_iflg = df_tmp[0].str[332:334]
        df_wgt = df_tmp[0].str[334:339]
        df_tdelta = df_tmp[0].str[344:352]
        df_ttime = df_tmp[0].str[352:362]
        df_delisc = df_tmp[0].str[367:375]
        df_resisc = df_tmp[0].str[375:382]
        df_w = df_tmp[0].str[383:384]
        df_ievt = df_tmp[0].str[384:394]

        # merging DataFrames together and set header names
        df_merged = pd.concat([df_nev, df_isol, df_iseq11, df_iseq22, df_openaz2, df_ropenaz2, df_topenaz2, df_iyr,
                               df_imon, df_iday, df_ihold, df_ihr, df_imin, df_sec, df_elat, df_elon, df_depth,
                               df_fmb, df_fms, df_ntot, df_ntel, df_sta, df_slat, df_slon, df_elev, df_delta,
                               df_azim, df_comp, df_onset, df_phasej, df_iphj, df_iphi, df_ipho, df_rdtdd,
                               df_rdelta, df_razim, df_dbot, df_gblat, df_gblon, df_stadel, df_bdep, df_tbath,
                               df_twater, df_obstt, df_iprec, df_prett, df_rawres, df_ecor, df_scor, df_elcor,
                               df_resid, df_iflg, df_wgt, df_tdelta, df_ttime, df_delisc, df_resisc, df_w,
                               df_ievt], axis=1)
        df_merged.columns = ["nev", "isol", "iseq11", "iseq22", "openaz2", "ropenaz2", "topenaz2", "iyr", "imon",
                             "iday", "ihold", "ihr", "imin", "sec", "elat", "elon", "depth", "fmb", "fms", "ntot",
                             "ntel", "sta", "slat", "slon", "elev", "delta", "azim", "comp", "onset", "phasej",
                             "iphj", "iphi", "ipho", "rdtdd", "rdelta", "razim", "dbot", "gblat", "gblon",
                             "stadel", "bdep", "tbath", "twater", "obstt", "iprec", "prett", "rawres", "ecor",
                             "scor", "elcor", "resid", "iflg", "wgt", "tdelta", "ttime", "delisc", "resisc", "w",
                             "ievt"]

        # return merged DataFrame
        return df_merged, file.replace(".", "_")

    else:
        print("No RES data for selected " + str(year))


# function to write DataFrame to text file
def output_df(path, df, file_name):

    # output re-formated df to TXT file
    outfile_hdf = path + "/reformated_" + file_name + ".txt"
    df.to_csv(outfile_hdf, sep="\t", index=False)


# main function
def main(raw_path, reformatted_path, year_range):

    # changing to working directory and list all HDF/RES files
    os.chdir(raw_path)
    file_list = sorted(os.listdir())

    # iterate through years in range
    for year in year_range:
        # send original HDF file to read_hdf function
        df_hdf, file_hdf_name = import_hdf(file_list, year)

        # send study area HDF file to output_df function
        output_df(reformatted_path, df_hdf, file_hdf_name)

        # send original RES file to read_res function
        df_res, file_res_name = import_res(file_list, year)

        # send re-formated RES file to output_df function
        output_df(reformatted_path, df_res, file_res_name)


# run main()
if __name__ == "__main__":

    # user specified working directory
    input_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/01_raw"
    output_path = "/Users/khangvo/Python_Projects/Puerto_Rico_Project/files/02_reformatted"

    # user specified year range of data
    year_min = 2000
    year_max = 2018
    year_range = np.arange(year_min, year_max + 1, 1)

    main(input_path, output_path, year_range)
