"""
    Written by
    Seth Roffe
    RINSE data handling functions
    Functions:
        getData: get data from file
        displayData: Display data in video format
        saveAsGif: Save data output in gif format
"""
import os
import numpy as np
import scipy.misc as smp ## For image drawing
import cv2
from moviepy.editor import ImageSequenceClip

""" getData from file, fileName
    @param fileName = name of data file
    @param imgSize = size of frame in pixels

    @return data = data generated from file
    @return imgEvts = output matrix of size imgSize for events to go into
    @return tmpImg = gray matrix of size imgSize to put on top of imgEvts
"""
def getData(fileName,imgSize=[320,320]):
    ### Define some constants ###
    GRAY = [128,128,128] ## rgb
    imgSize.reverse() ## Want it to be y,x not x,y

    ### Read in data ###
    data = np.genfromtxt(fileName,dtype=np.int)

    ### Define image ###
    rgbSize = tuple(imgSize + [3]) ## Add 3 to imgSize for RGB vals
    imgEvts = np.zeros(rgbSize,dtype=np.uint8)
    tmpImg = np.zeros(rgbSize,dtype=np.uint8)
    tmpImg[:] = GRAY ## temporary array to add
    return(data,imgEvts,tmpImg)


""" Display the data in video format

    @param fileName: file to read from
    @param imgSize: Size of image frame
    @param TIME_UNIT: how much time to hold in one "frame" of playback (default: 1E3 to bring to 1ms)
    @param show: Boolean to show image output or not
    @param saveGif: filename to save gif of output to.
"""
def displayData(fileName,imgSize,TIME_UNIT=1e3,show=True,saveGif=False):
    print("Viewing datastream. Press 'q' to exit")
    ## TIME_UNIT For converting times ##
    TIME_UNIT = int(TIME_UNIT)

    ### Set up Images ###
    imgSize.reverse() # Want y,x; not x,y
    rgbSize = tuple(imgSize + [3]) ## Add 3 to imgSize for RGB vals
    currFrame = np.zeros(rgbSize,np.uint8)
    lastFrame = 0; # for timing 

    gifImgs = []
    cv2.namedWindow("image",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("image",imgSize[1],imgSize[0])

    f = open(fileName,'r')
    try:
        while True:
            line = f.readline()
            if not line:
                break

            line = line.split()
            xCoord = int(line[0])
            yCoord = int(line[1])
            time = int(line[2])
            polarity = int(line[3]) # >0 for OFF events, else for ON

            ### Set the pixels ###
            if (int(time / TIME_UNIT)) > lastFrame:
                lastFrame = int(time / TIME_UNIT)
                cv2.imshow("image",currFrame)
                key = cv2.waitKey(1)
                if key == ord('q'):
                    cv2.destroyWindow('image')
                    break

                currFrame = np.zeros(rgbSize,np.uint8) + 255
                #currFrame[:,:] = [128,128,128]

                if polarity > 0:
                    # Red
                    currFrame[yCoord,xCoord] = [255,0,0] ## pol = 0, 1; 
                else:
                    # Blue
                    currFrame[yCoord,xCoord] = [0,0,255]

                if saveGif:
                    gifImgs.append(currFrame)
            else:
                if polarity > 0:
                    # Red
                    currFrame[yCoord,xCoord] = [255,0,0] ## pol = 0, 1; 
                else:
                    # Blue
                    currFrame[yCoord,xCoord] = [0,0,255]


        if saveGif:
            print("Save video to gif")
            saveAsGif(gifImgs,fileName)
    except KeyboardInterrupt:
        f.close()
        return
    f.close()

""" Save image stack as gif
    @param gifImgs: array of arrays containing image data
    @param outName: output gif file name
    @param fps: Number of frames per second for gif playback (default: 60)
    @param scale: float for how much to rescale each image (default: 1.0)
"""
def saveAsGif(gifImgs,outName,fps=60,scale=1.0):
    ### ensure that the file has the .gif extension ###
    basename, _ = os.path.splitext(outName)
    outName = basename + '.gif'
    ### make the moviepy clip ###
    clip = ImageSequenceClip(list(gifImgs), fps=fps).resize(scale)
    clip.write_gif(outName, fps=fps)

if __name__ == '__main__':
    #data,imgEvts,tmpImg = getData('multiPattern1_fixed__injected.txt')
    #data,imgEvts,tmpImg = getData('multiPattern1_fixed_.txt')
    #data,imgEvts,tmpImg = getData('nikData/sim_satellites.txt',[600,600])
    displayData("testData.txt",[640,480],TIME_UNIT=1e4,show=True,saveGif=True)
    #while True:
    #    displayData(data,imgEvts,tmpImg,TIME_UNIT=1e4,show=True)
