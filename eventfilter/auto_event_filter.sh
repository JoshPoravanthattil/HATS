#!/bin/bash

outdir="/mnt/c/Users/Linus/Documents/NMNIST/Test_Injected_5_1"
EVENT_FILTER_DIR="/home/linus/RINSE"

if [ ! -d ${outdir} ]; then
    mkdir -p ${outdir}
fi

## TODO: add for loop for different noise rates
for d in /mnt/c/Users/Linus/Documents/NMNIST/TestF/*/; do
    curr_class=$(basename $d)
    if [ ! -d ${outdir}/${curr_class} ]; then
        echo "Making directory" ${outdir}/${curr_class}
        mkdir -p ${outdir}/${curr_class}
    fi
    curr_output=${outdir}/${curr_class}

    for file in ${d}*; do
        file_basename=$(basename ${file})
        filename_no_ext=${file_basename%.*}
        outfile=${curr_output}/${filename_no_ext}.txt
        echo ${file} ${outfile}
        ## RINSE Here
        python3 ${EVENT_FILTER_DIR}/event_filter.py ${file} ${outfile}
    done
done