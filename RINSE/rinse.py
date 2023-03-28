"""
    Written by
    Seth Roffe
    Radiation-Induced-Noise Simulation Evironment
    RINSE
    main file
"""

import argparse
import os
import sys

### RINSE Imports ###
import injector
import dataHandling

#TODO: Add savegif option and logic
def main():
    parser = setupArgumentParser()
    options = parser.parse_args()
    ## Print help
    if len(sys.argv) == 1:
        parser.print_help()
        exit(1)
    ## Print out noise rate ##
    #print("Noise Rate: {} +/- {}".format(options.noiseRate[0],options.noiseRate[1]))
    if options.inFile is None:
        print("Input file needed. Use python rinse.py -h for help Exiting...")
        ### Return with error ###
        return 1

    ### make sure input exists ###
    if not os.path.isfile(options.inFile):
        print("Input file {} does not exist.".format(options.inFile))
        return 1
    #data,imgEvts,tmpImg = dataHandling.getData(options.inFile,options.size)

    if options.viewIn:
        print("Frame size:",options.size)
        dataHandling.displayData(options.inFile,options.size,TIME_UNIT=options.delta,saveGif=options.saveGif)

    ### Inject into file ###
    if options.inject:
        if not options.outFile:
            print("Injecting with parameters:")
            print("\tNoise Rate: {} +/- {}".format(options.noiseRate[0],options.noiseRate[1]))
            print("\tImage Size:",options.size)
            print("\tAOI:",options.AOI)
            options.outFile = injector.injectNoiseToFile(options.inFile, noiseRate=options.noiseRate, imgSize=options.size, AOI=options.AOI)
        else:
            print("Injecting to {} with parameters:".format(options.outFile))
            print("\tNoise Rate: {} +/- {}".format(options.noiseRate[0],options.noiseRate[1]))
            print("\tImage Size:",options.size)
            print("\tAOI:",options.AOI)
            injector.injectNoiseToFile(options.inFile, noiseRate=options.noiseRate, imgSize=options.size, AOI=options.AOI, outFile=options.outFile)

    if options.viewOut:
        ### Check if output exists ###
        if not os.path.isfile(options.outFile):
            print("There is no output file to view. Please input output file with -o (--output-file) to imput output_file name or use -h for help.")
            return 1
        ### get output data ###
        #data,imgEvts,tmpImg = dataHandling.getData(options.outFile)
        print("Frame size:",options.size)
        dataHandling.displayData(options.outFile,options.size,TIME_UNIT=options.delta,saveGif=options.saveGif)

    return

"""
    Setup Argument Parser for RINSE
"""
def setupArgumentParser():
    ### Initialize argument parser ###
    parser = argparse.ArgumentParser(description="The Neuromorphic Radiation-Induced-Noise Simulation Environment (RINSE) created by Seth Roffe"
    )
    ### Input File ###
    parser.add_argument(
        "-f", "--input-file",
        type=str,
        metavar="<INPUT>",
        default=None,
        dest="inFile",
        help="The input data file path to read from."
    )
    parser.add_argument(
        "-o", "--output-file",
        type=str,
        metavar="<OUTPUT>",
        default=None,
        dest="outFile",
        help="Output data file path to write to (default: <input_file>_injected.txt)"
    )
    parser.add_argument(
        "-aoi", "--angle-of-incidence",
        type=int,
        metavar="<ANGLE>",
        default=0,
        dest="AOI",
        help="Angle of incidence between sensor with radiation beam (default: 0)"
    )
    parser.add_argument(
        "-s", "--imgSize",
        type=int,
        metavar="<SIZE>",
        default=[640,480],
        nargs=2,
        dest="size",
        help="Size of sensor frame in pixels (default: 640 480)"
    )
    parser.add_argument(
        "-vi", "--view-input",
        action='store_true',
        default=False,
        dest="viewIn",
        help="View video of input file"
    )
    parser.add_argument(
        "-vo", "--view-output",
        action='store_true',
        default=False,
        dest="viewOut",
        help="View video of output file"
    )
    parser.add_argument(
        "-i", "--inject",
        action="store_true",
        default=False,
        dest="inject",
        help="Inject noise into input file and write to output file"
    )
    parser.add_argument(
        "-d", "--delta",
        type=float,
        metavar="<DELTA T>",
        default=1e4,
        dest="delta",
        help="(Delta t timestep * 1 us) to hold in one frame when viewing video. Larger values to speed up video. 1 is us per 'frame' (default = 1e4)."
    )
    parser.add_argument(
        "-n", "--noise",
        type=int,
        metavar="<NOISE EVTS/S>",
        default=[100,20],
        nargs=2,
        dest="noiseRate",
        help="Number of noise events per second and standard deviation (default: 100 +- 20 noise events per second)"
    )
    parser.add_argument(
        "-g", "--save-gif",
        action='store_true',
        default=False,
        dest="saveGif",
        help="Save video output to a gif"
    )

    return parser

if __name__ == '__main__':
    main()
