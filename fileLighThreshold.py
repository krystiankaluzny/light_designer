import cv2 as cv
import os


def thresholdFile(inputPath: str, outputPath: str):
    print("Threshold file", "input", inputPath, "output", outputPath)
    src = cv.imread(inputPath)
    srcHls = cv.cvtColor(src, cv.COLOR_BGR2HLS_FULL)
    mask = cv.inRange(srcHls, (0, 160, 0), (255, 255, 255))
    dstHls = cv.bitwise_and(srcHls, srcHls, mask=mask)
    dst = cv.cvtColor(dstHls, cv.COLOR_HLS2BGR_FULL)
    cv.imwrite(outputPath, dst)


def thresholdAllInDir(inputDir: str, outputDir: str):
    for file in os.listdir(inputDir):
        baseName = os.path.basename(file)
        split = os.path.splitext(baseName)
        fileName = split[0]
        ext = split[1]
        if ext == ".jpg" or ext == ".png":
            inFile = os.path.join(inputDir, file)
            outFile = os.path.join(outputDir, "th_" + fileName + ".jpg")
            thresholdFile(inFile, outFile)


def deleteDir(dir: str):
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def runThreshold(srcDir: str):
    thresholdDirName = "threshold_160"
    thresholdDirOldName = "threshold_old"

    deleteDir(thresholdDirOldName)
    if os.path.exists(thresholdDirName):
        os.rename(thresholdDirName, thresholdDirOldName)
    os.mkdir(thresholdDirName)

    thresholdAllInDir(srcDir, thresholdDirName)

# runThreshold("/home/kkaluzny/Pictures/lampki_bez_swiatla")
runThreshold("/home/kkaluzny/Pictures/lampki_swiatlo")