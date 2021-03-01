from testfile import file_name, folder_path, file_path
import pydicom
import matplotlib.pyplot as plt
import os

import numpy as np

import sys
import glob

# load dicom


def load_dicom(folder_path):
    files = [pydicom.dcmread(folder_path+'/'+s)
              for s in os.listdir(folder_path)]
    # slices = [s for s in slices if 'SliceLocation' in s]     #   skip files with no SliceLocation (eg scout views)
    # slices = []
    # skipcount = 0
    # for f in files:
    #     if hasattr(f, 'SliceLocation'):
    #         slices.append(f)
    #     else:
    #         skipcount = skipcount + 1
    # print("skipped, no SliceLocation: {}".format(skipcount))

    slices=files
    slices.sort(key=lambda x: int(x.InstanceNumber))
    try:
        slice_thickness = np.abs(
            slices[0].ImagePositionPatient[2]-slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(
            slices[0].SliceLocation-slices[1].SliceLocation)
    for s in slices:
        s.SliceThickness = slice_thickness
        print(slice_thickness)
    return slices
