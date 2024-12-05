import cv2 as cv
import helper_functions as help
import os
from os import listdir




def main():
    for image in os.listdir("input_file"):
        image1 = image
        # processing input image
        threshold = 64
        image = cv.imread("input_file/" + image)
        cropImage = help.crop_input_image(image, threshold)
        imageList = cropImage.tolist()
        width = len(imageList[0])
        height = len(imageList)
        cropImage = cv.resize(
            cropImage, ((width // threshold) * 64, (height // threshold) * 64)
        )
        # splitting image into average chunks
        for row in range(0, height, threshold):
            for column in range(0, width, threshold):
                grid = []
                for i in range(threshold):
                    grid.append([])
                for i in range(threshold):
                    for j in range(threshold):
                        grid[i].append(imageList[row + i][column + j])
                average = help.block_average(grid, 0, 0, threshold, threshold)
                # matching source images and writing
                closeMatch = help.find_nearest_image(tuple(average))
                matchImage = cv.imread("cropped_photos/" + closeMatch)
                matchImageCrop = cv.resize(matchImage, (64, 64))
                cropImage[
                    (row // threshold * 64) : (row // threshold * 64) + 64,
                    (column // threshold * 64) : (column // threshold * 64) + 64,
                ] = matchImageCrop
    name = 'OUTPUT' + image1
    cv.imwrite("output_images/" + name, cropImage)


if __name__ == "__main__":
    str = input("First time running? Y/N\n")
    if str.lower() == "y":
        print("Writing average colors text file...")
        import average_color
        print("Done")

    str2 = input('Have you added 1 or more images to "input_file"? Y/N\n')
    if str2.lower() == 'y':
        print('Running program...')
        main()
        print('Check "output_image" folder for output(s)!')
        
