"""
   Written by
   Seth Roffe
   RINSE injection functions
   Functions: injectNoiseToFile - inject noise into datafile and output injected data
   genNoisePDF - generate probability density function of noise
"""
import os
import numpy as np

"""
    Inject noise to file
    @param fileName: data file to inject noise into
    @param noiseRate: Noise rate and standard deviation in evts/s
    @param imgSize: size of the frame in pixels
    @param AOI: Angle of incidence in degrees
    @param outFile: what the injected datafile should be called
                        defaults to fileName_injected.txt
"""
def injectNoiseToFile(fileName,noiseRate, imgSize=[640,480], AOI=0, outFile=None):
    ### Default to the same filename with _injected at the end ###
    injcount = 0
    MIN_CLUSTER_SIZE = 1
    MAX_CLUSTER_SIZE = 15
    MIN_LINE_SIZE = 4
    ### Max diagonal ###
    MAX_LINE_SIZE = int(np.sqrt(imgSize[0]**2 + imgSize[1]**2))

    #CLUSTER_PROB = 0.999 ## Probability of cluster vs line
    #LINE_PROB = 1.0 - CLUSTER_PROB
    CLUSTER_PROB = AOIClusterProb(AOI) ## Probability of cluster vs line
    LINE_PROB = 1.0 - CLUSTER_PROB

    if outFile is None:
        nameWithoutExt, fileExt = os.path.splitext(fileName)
        outFile = nameWithoutExt + "_injected.txt"
    out = open(outFile,"w")

    ### Open file to read data lines ###
    ##TODO: Change to loop through line by line without putting all in memory
    with open(fileName, 'r') as f:
        lines = f.readlines()

    ### Loop through the times and see where to insert noise from PDF ###
    prevTime = 0
    PERCENT_ITER = 10
    for i in range(len(lines)):
        ### Print progress ###
        if i % int(len(lines)/PERCENT_ITER) == 0:
            print("Injecting... {}%".format(int(float(i)/len(lines)*100)),end='\r')

        currLine = lines[i]

        ### Put current line in output ###
        out.write(currLine)

        ### get the timestamp ###
        ## x, y, currTime, polarity format ##
        currTime = int(currLine.split()[2])
        #injectedTime = np.random.randint(0,prevTime+1)

        timeDiff = currTime - prevTime

        ### Injections ###
        for j in range(timeDiff):
            #gaussianPick = np.random.normal(1193,382) ### In evts/s
            gaussianPick = np.random.normal(noiseRate[0],noiseRate[1]) ### In evts/s
            probOfInject = poisson(lam=gaussianPick * 10**-6,k=1) ## Probability of injection in 1 us

            ### Perform injection ###
            ## Get pixels to inject to ##
            if np.random.random() <= probOfInject:
                if np.random.random() < CLUSTER_PROB:
                    injNoisePixels = genNoiseCluster(imgSize,np.random.randint(MIN_CLUSTER_SIZE,MAX_CLUSTER_SIZE))
                else:
                    injNoisePixels = genNoiseLine(imgSize,np.random.randint(MIN_LINE_SIZE,MAX_LINE_SIZE))

                ## Get noise string ##
                injNoise = genNoiseEvent(injNoisePixels,currTime+j)

                ### Write injected noise to output and output Array ###
                out.write(injNoise)
                injcount += len(injNoise.splitlines())

        prevTime = currTime
    print("Injecting... 100%")
    out.close()
    print("Ensuring file is sorted by timestamp")
    outLines = open(outFile,'r').readlines()
    out = open(outFile,'w')
    for line in sorted(outLines, key=lambda line: int(line.split()[2])):
        out.write(line)
    print("{} events injected into {}".format(injcount,outFile))
    return outFile

"""
    Generate pixels for noise cluster events
    @param imgSize = size of the frame in pixels
    @param timeStamp = Time of noise injection in us
    @param clusterSize = How large the cluster will be
    @return injPixels = Tuple of all pixels to inject to
"""
def genNoiseCluster(imgSize,clusterSize):
    ### Choose random coordinates to inject noise to ###
    xSize = imgSize[0]
    ySize = imgSize[1]
    init_xCoord = np.random.randint(0,xSize)
    init_yCoord = np.random.randint(0,ySize)
    NEIGHBORHOOD = int(np.ceil(clusterSize/2))
    #print("Neighborhood",NEIGHBORHOOD)

    ## TODO: Double check this
    injPixels = []
    #for i in range(1,clusterSize):
    for x in range(-NEIGHBORHOOD,NEIGHBORHOOD):
        for y in range (-NEIGHBORHOOD,NEIGHBORHOOD):
            ### Random Direction with boundary conditions ###
            xCoord = init_xCoord + x
            yCoord = init_yCoord + y

            # xCoord = xCoord + np.random.randint(-1,2)
            # yCoord = yCoord + np.random.randint(-1,2)

            if (xCoord >= xSize or xCoord <= 0):
                break
            if (yCoord >= ySize or yCoord <= 0):
                break

            ## Chance at injecting at pixel
            if np.random.random() < 0.1:
                injPixels.append((xCoord,yCoord))

    return injPixels

"""
    Generate pixels for noise line events
    @param imgSize = image frame size in pixels
    @param timeStamp = timestamp of the noise events in us
    @param lineSize = How long the injected noise line will be
    @return injPixels = Tuple of all pixels to inject to
"""
def genNoiseLine(imgSize,lineSize):
    ## Choose random coordinates to start noise line###
    xSize = imgSize[0]
    ySize = imgSize[1]
    xCoord = np.random.randint(0,xSize)
    yCoord = np.random.randint(0,ySize)

    ### Random Starting Direction ###
    xDirection = posOrNeg()
    yDirection = posOrNeg()

    slope = np.random.randint(1,360) ## TODO: Make angle more precise
    #slope = 10000000000000
    #slope = 2
    ##TODO: look into Line timestamping so you don't have too many events of single timestamp
    injPixels = [(xCoord,yCoord)]
    for i in range(1,lineSize):
        if i % slope == 0:
            xCoord += xDirection
        else:
            yCoord += yDirection

        ### Can't wrap around with line ###
        ### X-Boundary conditions ###
        if (xDirection > 0 and xCoord == xSize):
            break
        elif (xDirection < 0 and xCoord == 0):
            break
        ### Y-Boundary conditions ###
        if (yDirection > 0 and yCoord == ySize):
            break
        elif (yDirection < 0 and yCoord == 0):
            break
        injPixels.append((xCoord,yCoord))

    return injPixels


"""
    Generate pixels for noise event string to write to file
    @param injPixels = Pixels to inject to
    @param timestamp = Starting timestamp of injection
    @return outString = String of noise events to write to file
"""
def genNoiseEvent(injPixels,timeStamp):
    ## Constants ##
    posTime = int(np.random.normal(2000, 200)) #us
    waitTime = int(np.random.normal(100,50)) #us
    negTime = int(np.random.normal(8000, 1000)) #us

    outString = ""
    ## Positive Bursts ##
    sigma = 340
    for t in range(timeStamp, timeStamp + posTime):
        for pixel in injPixels:
            ## Need to zero-mean gaussian with timestamp, and do some timing
            ## adjustments to match real data
            gaussian = np.exp(-(1.0/2.0)*(((t - timeStamp) - posTime + 230)/sigma)**2)
            ## TODO: Check out gaussian normalization?
            #gaussian = 1.0/np.sqrt(2*np.pi*sigma**2)*np.exp(-(1.0/2.0)*(((t - timeStamp) - posTime + 230)/beta)**2)
            if gaussian > np.random.random():
                outString += str(pixel[0]) + " " + str(pixel[1]) + " " + \
                        str(t) + " " + "1" + "\n"


    ## Negative Bursts after waiting ##
    negTimeStart = timeStamp + posTime + waitTime
    beta = 5200.0

    for t in range(negTimeStart, negTimeStart + negTime):
        for pixel in injPixels:
            exp = 1/beta * np.exp(-(1.0/beta)*(abs(t - negTimeStart) - 900))
            if exp > np.random.random():
                outString += str(pixel[0]) + " " + str(pixel[1]) + " " + \
                        str(t) + " " + "0" + "\n"

    return outString

"""
    Poisson distribution
    @param lam: Frequency of event per timestamp
    @param k: Number of events happening per timestamp
    @return out: Probability of k events with frequency lam happening per timestamp (1us timestamp is used)
"""
def poisson(lam,k=1):
    out = (np.exp(-lam) * lam**k) / np.math.factorial(k)
    return out

"""
    Choose 1 or -1 at random
"""
def posOrNeg():
    if np.random.random() < 0.5:
        return 1
    else:
        return -1

"""
    Calculate probability based on angle of incidence (with jitter) in degrees
    @param angle: Angle of incidence in degrees
    @param jitterOOM: Order of magnitude of jitter
    @return clustProb: probability of cluster event
"""
def AOIClusterProb(angle,jitterOOM=1e-3):
    jitterAngle = angle + (np.random.random() * jitterOOM)
    rad = np.radians(jitterAngle)
    clustProb = abs(np.cos(rad))
    return clustProb

if __name__ == '__main__':
    injectNoiseToFile('multiPattern1_fixed_.txt')
