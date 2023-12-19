import numpy as np

def normalizeByTime(arr, time):
    """Normalize a array by its time"""
    i = 0
    while(arr[i,0] < time):
        i += 1
    arr = arr[i:-1,:]
    arr[:,0] = arr[:,0] - time
    return arr

def loadFile(filename):
    """Extracts array from UTIAS dataset"""
    with open(filename) as file:
        lines = [line for line in file]
        num_entries = -1
        for line in lines:
            if "#" in line:
                continue
            entries = line.split()
            if num_entries == -1:
                num_entries = len(entries)
                arr = np.zeros(shape=(0,num_entries))
            arr = np.vstack([arr, [float(i) for i in entries]])

    return arr

def loadFiles(truthFile, measFile, odomFile, offset=0):
    """Gets data from files and normalizes the time"""
    truth_array = loadFile(truthFile)
    meas_array = loadFile(measFile)
    odom_array = loadFile(odomFile)
    
    greatest_time = max(truth_array[0,0], meas_array[0,0], odom_array[0,0]) + offset
    
    truth_array = normalizeByTime(truth_array, greatest_time)
    meas_array = normalizeByTime(meas_array, greatest_time)
    odom_array = normalizeByTime(odom_array, greatest_time)
    
    return truth_array, meas_array, odom_array

def loadLandmarks(landmarkFile, barcodeFile):
    barcode_array = loadFile(barcodeFile)
    landmark_array = loadFile(landmarkFile)

    for i, landmark in enumerate(landmark_array):
        landmark_id = landmark[0]
        barcode_index = 0
        while(landmark_id != barcode_array[barcode_index][0]):
            barcode_index += 1
        landmark_array[i][0] = barcode_array[barcode_index][1]

    return landmark_array

def createBarcodeDict(barcodeFile):
    """Creates dictiobnary from barcode file"""
    barcode_array = loadFile(barcodeFile)
    bar_dict = dict(zip(barcode_array[:,1], [int(i) for i in barcode_array[:,0]]))
    return bar_dict