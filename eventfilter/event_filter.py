import numpy as np
import copy
import matplotlib.pyplot as plt
import sys
import os
from scipy.signal import argrelextrema

# my name is joshua

if __name__ == '__main__':
    # check if incorrect input sequence
    if len(sys.argv) != 3:
        print("error: incorrect Input!\nInput in the form of:\npython3 event_filter.py <input.txt>")
        sys.exit(1)

    # Take in name of the file
    fname = sys.argv[1]
    outfname = sys.argv[2]

    # check if incorrect filename
    if not os.path.isfile(fname):
        print("error: {} does not exist".format(fname))
        sys.exit(1)
    
    # Open the input file and store lines in matrix
    with open(fname) as f:
        lines = f.readlines()

    # Create the object to hold file data
    data = np.zeros(len(lines), dtype='object')

    # PARAMETER VARIABLES
    reference_time = 0
    delta_t = 10**3
    std_multiplier = 0.1

    on_event_count = 0
    off_event_count = 0
    on_event_count_total = 0
    off_event_count_total = 0
<<<<<<< HEAD
    std_multiplier = 0.1
=======
>>>>>>> a2b03500902a0023e3327eb33607e7281759abe2

    numvars = 3
    # (on event, off event, total) <- event rates formatting
    temp_window = np.array([])
    time_series = np.array([np.zeros(numvars)])

    # preserve index to reference original event stream
    index_list = []
    inner_index_list = []

    # Fill data object
    for index, line in enumerate(lines):
        data[index] = [int(x) for x in line.strip().split(' ')]
        on_event_count = on_event_count+1 if data[index][-1] == 1 else on_event_count
        off_event_count = off_event_count+1 if data[index][-1] == 0 else off_event_count
        temp_window = np.append(temp_window, data[index][-2])
        inner_index_list.append(index)

        # if time window has elapsed
        if data[index][-2] - reference_time >= delta_t:
        
            # window computations
            window_event_rate = len(temp_window)/delta_t
            on_event_rate = on_event_count/delta_t
            off_event_rate = off_event_count/delta_t
            time_series = np.append(time_series, [[on_event_rate, off_event_rate, window_event_rate]], axis=0)
            index_list.append(inner_index_list)

            # resets
            reference_time += delta_t
            on_event_count_total += on_event_count
            off_event_count_total += off_event_count
            on_event_count = 0
            off_event_count = 0
            temp_window = np.array([])
            inner_index_list = []

    # delete the initial row of zeros
    time_series = time_series[1:]
    calc_std = np.std(time_series[:, 2])
    calc_mean = np.mean(time_series[:, 2])
    delete_indices = np.where(time_series[:, 2] > calc_std*std_multiplier)[0]
    print(calc_mean, calc_std, 0.1*calc_std)
    final_deleted_indices = np.array([], dtype=int)

    for i in delete_indices:
        final_deleted_indices = np.append(final_deleted_indices, index_list[i])

    filtered_data = np.delete(data, final_deleted_indices, axis=0).tolist()
    

    with open(outfname, 'w') as f:
        for line in filtered_data:
            f.write(str(" ".join([str(x) for x in line])))
            f.write("\n")



