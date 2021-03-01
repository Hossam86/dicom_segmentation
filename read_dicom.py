from testfile import file_name, folder_path, file_path
import pydicom
import matplotlib.pyplot as plt
import numpy as np
import os


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

    slices = files
    slices.sort(key=lambda x: int(x.InstanceNumber))
    try:
        slice_thickness = np.abs(
            slices[0].ImagePositionPatient[2]-slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(
            slices[0].SliceLocation-slices[1].SliceLocation)
    for s in slices:
        s.SliceThickness = slice_thickness
    return slices


def get_pixels_hu(scans):
    image = np.stack([s.pixel_array for s in scans])
    image = image.astype(np.int16)

    # set outside-of-scan pixels to 0
    # The intercept is usually -1024, so air is approximatly 0
    image[image == -2000] = 0

    # Convert to Hounsfield units (HU)
    intercept = scans[0].RescaleIntercept
    slope = scans[0].RescaleSlope

    if slope != 1:
        image = slope * image.astype(np.float64)
        image = image.astype(np.int16)

    image += np.int16(intercept)

    return np.array(image, dtype=np.int16)


def main():
    patient_dicom = load_dicom(folder_path)
    patient_pixels = get_pixels_hu(patient_dicom)
    # sanity check
    plt.imshow(patient_pixels[50], cmap=plt.cm.bone)
    plt.show()


if __name__ == "__main__":
    main()
