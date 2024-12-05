import os
from os import listdir
import helper_functions as help
import cv2 as cv

with open("average_colors", "w") as file:
    file.write("Name: BGR Values \n")
    for image in os.listdir("cropped_photos"):
        img = cv.imread("cropped_photos/" + image)
        grid = img.tolist()
        width, height = len(grid[0]), len(grid)
        outputGrid = help.compress_image(grid, 0, 0, width, height, height)
        average = outputGrid[0][0]
        file.write(image + ": " + str(average) + "\n")

if __name__ == '__main__':
    print('Wrong file ran')