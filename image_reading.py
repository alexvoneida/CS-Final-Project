import os
from os import listdir
import helper_functions as help
import cv2 as cv

for image in os.listdir("photos"):
    processedImage = cv.imread("photos/" + image)
    crop = help.crop_image(processedImage)
    name = "crop" + image
    cv.imwrite("cropped_photos/" + name, crop)

if __name__ == '__main__':
    print('Wrong file ran')