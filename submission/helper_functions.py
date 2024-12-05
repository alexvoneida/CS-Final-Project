from PIL import Image
import numpy as np
import cv2


def image_to_list(image_file):

    image = Image.open(image_file)

    # Check for RGB here
    if image.mode != "RGB":
        image = image.convert("RGB")

    pixel_array = []
    pixels = image.load()

    # Dimensions
    width, height = image.size

    for j in range(height):
        row = []
        for i in range(width):
            row.append(pixels[i, j])
        pixel_array.append(row)
    return pixel_array


def output_image(pixel_grid, filename):
    img = Image.fromarray(np.array(pixel_grid).astype(np.uint8), "RGB")
    img.save(filename)


def show_image(pixel_grid):
    img = Image.fromarray(np.array(pixel_grid).astype(np.uint8), "RGB")
    img.show()


def block_average(grid, x, y, width, height):
    redTotal = 0
    greenTotal = 0
    blueTotal = 0
    for i in range(height):
        for j in range(width):
            redTotal += grid[i + y][j + x][0]
            greenTotal += grid[i + y][j + x][1]
            blueTotal += grid[i + y][j + x][2]

    totalNum = (width) * (height)

    return [redTotal // totalNum, greenTotal // totalNum, blueTotal // totalNum]


def create_compressed_block(avg_color, width, height):
    block = []
    for i in range(height):
        block.append([])
    for i, list in enumerate(block):
        for x in range(width):
            block[i].append(avg_color)
    for i in block:
        for x, value in enumerate(i):
            if value == []:
                block.remove(block[i][x])
    return block


def merge_lists(list1, list2):
    returnList = []
    for i in range(len(list1)):
        returnList.append([])
        for x in list1[i]:
            returnList[i].append(x)
    for i in range(len(list2)):
        for x in list2[i]:
            returnList[i].append(x)
    return returnList


def compress_image(grid, x, y, width, height, threshold):
    if (width) <= threshold and (height) <= threshold:
        average = block_average(grid, x, y, width, height)
        return create_compressed_block(average, width, height)
    else:
        gridList = []
        for i in range(height):
            gridList.append([])
        # recursion
        topLeft = compress_image(grid, x, y, (width // 2), (height // 2), threshold)
        topRight = compress_image(
            grid, x + (width // 2), y, (width // 2), (height // 2), threshold
        )
        bottomLeft = compress_image(
            grid, x, y + (height // 2), (width // 2), (height // 2), threshold
        )
        bottomRight = compress_image(
            grid,
            x + (width // 2),
            y + (height // 2),
            (width // 2),
            (height // 2),
            threshold,
        )

        for i in range(len(topLeft)):
            for x in topLeft[i]:
                gridList[i].append(x)
            for j in topRight[i]:
                gridList[i].append(j)
        for i in range(len(bottomRight)):
            for x in bottomLeft[i]:
                gridList[i + height // 2].append(x)
            for j in bottomRight[i]:
                gridList[i + height // 2].append(j)

    return gridList


def compress_image_iterative(grid, width, height, threshold):
    """Grid length and width must be divisible by threshold in order for this method to work"""

    # creating empty rows
    outputGrid = []
    for i in range(len(grid)):
        outputGrid.append([])

    # iteratively decreasing resolution of grid
    for i in range(0, height, threshold):
        for j in range(0, width, threshold):
            tempGrid = []
            for k in range(threshold):
                tempGrid.append(grid[i][j + k])
            print(tempGrid)


def crop_image(image):
    height, width, _ = image.shape
    if height < 1012 or width < 1012:
        startHeight = (height - 512) // 2
        startWidth = (width - 512) // 2
        return image[startHeight : startHeight + 512, startWidth : startWidth + 512]
    else:
        startHeight = (height - 1024) // 2
        startWidth = (width - 1024) // 2
        return image[startHeight : startHeight + 1024, startWidth : startWidth + 1024]


def crop_input_image(image, threshold):
    height, width, _ = image.shape
    cropHeight, cropWidth = height - (height % threshold), width - (width % threshold)
    startHeight, startWidth = (height - cropHeight) // 2, (width - cropWidth) // 2
    return image[startHeight:(cropHeight + startHeight), startWidth:(cropWidth + startWidth)]

def find_nearest_image(average):
    import ast
    with open('average_colors', 'r') as file:
        averageList = file.readlines()
    
    match = ['',1000000000]
    for i in range(1, len(averageList)):
        score = 0
        line = averageList[i].split(': ')
        sourceName = line[0]
        sourceAverage = line[1].strip()
        sourceAverage = tuple(ast.literal_eval(sourceAverage))
        for j in range(len(sourceAverage)):
            score += (int(average[j]) - int(sourceAverage[j])) ** 2
        if score < match[1]:
            match = [sourceName, score]
    return match[0]

if __name__ == '__main__':
    print('Wrong file ran')