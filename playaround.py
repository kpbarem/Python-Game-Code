from PIL import Image
from PIL import ImageChops
from PIL import ImageMath
from PIL import ImageOps
import numpy as np
import math
import time
#comes with python
from collections import Counter

def calc_root_mean_square_diff(img1, img2):
        hist = ImageChops.difference(img1, img2).histogram()
        return math.sqrt((sum(val*(idx**2) for idx, val in enumerate(hist)))/(float(img1.size[0] * img2.size[1])))

c = Image.open('Problems/Basic Problems B/Basic Problem B-09/C.png')

b = Image.open('Problems/Basic Problems B/Basic Problem B-09/B.png')

solution = Image.open('Problems/Basic Problems B/Basic Problem B-09/5.png')

a = Image.open('Problems/Basic Problems B/Basic Problem B-09/A.png')
b = Image.open('Problems/Basic Problems B/Basic Problem B-09/B.png')

def calculate_dark_pixel_ratio_of_image(img):
    imgArray = np.array(img)
    whitePixelCounter = 0;
    darkPixelCounter = 0;
    overallPixelCounter = 0;
    whitePixelArray = np.array([255,255,255,255])
    for eachRow in imgArray:
        #several pix in separate rows make a column
        for eachPix in eachRow:
            if(np.array_equal(eachPix, whitePixelArray)):
                whitePixelCounter+=1
            else:
                darkPixelCounter+=1
            overallPixelCounter+=1
    return darkPixelCounter/float(overallPixelCounter)

aRatio = calculate_dark_pixel_ratio_of_image(a)
bRatio = calculate_dark_pixel_ratio_of_image(b)

print(aRatio)
print(bRatio)

difference = aRatio * 100 - bRatio * 100

print(difference)

def find_dark_pixel_solution(a_ratio, b_ratio, c_ratio, solution_images):
    a_b_difference = aRatio - b_ratio
    c_to_solution_differences = []
    for solution in solution_images:
        difference = c_ratio - calculate_dark_pixel_ratio_of_image(solution)
        c_to_solution_differences.append(difference)
    #find the closest one to a_b_difference
    #so if a_b difference is -34, I want the number that is closest to negative 34
    return min(c_to_solution_differences, key=lambda x:abs(x-a_b_difference))


# aImgArray=np.array(a)
#
# #
# # a = 1 - np.asarray(a)
#
# X = Image.fromarray(aImgArray)
#
# X.show()
#
# whitePixelArray = np.array([255,255,255,255])
# blackPixelArray = np.array([0,0,0,0])
#
# darkPixelcounter = 0;
# overallPixelCounter = 0;
# whitePixelCounter = 0;
#
# # for each row in the image
# for eachRow in aImgArray:
#     #several pix in separate rows make a column
#     for eachPix in eachRow:
#         if(np.array_equal(eachPix, whitePixelArray)):
#             whitePixelCounter+=1
#         else:
#             darkPixelcounter+=1
#
#         overallPixelCounter+=1
#
#
#
# print ('darkPixelcounter ' + str(darkPixelcounter))
# print ('overallPixelCounter ' + str(overallPixelCounter))
#
# ratio = darkPixelcounter/float(overallPixelCounter)
#
# print(ratio)
#
# X = Image.fromarray(aImgArray)
#
# X.show()
#
#
#
#
#
#
# #convert image to 3 dimensional array
# # iar = np.asarray(i)
# #
# # print iar
#
# #opening video guy's files
# def createExamples():
#     numberArrayExamples = open('newFile.txt', 'a')
#     numbersWeHave = range(0,10)
#     versionsWeHave = range(1,10)
#
#     for eachNum in numbersWeHave:
#         for eachVersion in versionsWeHave:
#             imgFilePath = 'images/numbers' +str(eachNum) + '.' + str(eachVersion) + '.png'
#             ei = Image.open(imgFilePath)
#             eiar = np.array(ei)
#             #copy of numpy array of image as a string
#             eiar1 = str(eiar.tolist())
#
#             #0::wholearraylistofimage plus new line character
#             lineToWrite = str(eachNum) + '::' + eiar1 + '\n'
#             #basically we are taking each answer file as a numpy array and then we will compare each image to determine
#             #which image in the answers it matches most closely
#             #we can do something similar to this in the RPM files for pattern recognition
#             numberArrayExamples.write(lineToWrite)
#
#
#
#
# def threshold(imageArray):
#     balanceArr = []
#     newArr = imageArray
#
#     #for each row in the image
#     for eachRow in imageArray:
#         #several pix in separate rows make a column
#         for eachPix in eachRow:
#             #average of pixels in row
#             avgNum = reduce(lambda x, y: x+y, eachPix[:3])/len(eachPix[:3])
#             balanceArr.append(avgNum)
#     #full average of all pixels
#     balance = reduce(lambda x, y: x+y, balanceArr)/len(balanceArr)
#
#     for eachRow in newArr:
#         for eachPix in eachRow:
#             #if brighter than the average change it to white
#             if(reduce(lambda x, y: x+y, eachPix[:3])/len(eachPix[:3]) > balance):
#                 eachPix[0] = 255
#                 eachPix[1] = 255
#                 eachPix[2] = 255
#                 eachPix[3] = 255
#             else:
#                 #if less bright than the average change it to black
#                 eachPix[0] = 0
#                 eachPix[1] = 0
#                 eachPix[2] = 0
#                 eachPix[3] = 0
#     #returns array for a black and white image
#     return newArr
# #threshold(iar)
#
#
#
# #for image recognition you need examples to compare the image to in order to determine if it's a match
#
# def whatNumIsThis(filePath):
#     matchedArr = []
#     loadExamps = open('numArEx.txt', 'r').read()
#     #take the 3 dimensional array of each solution figure and put it in a list called loadExamps
#     loadExamps = loadExamps.split('\n')
#
#     i = Image.open(filePath)
#     iar = np.array(i)
#     iarl = iar.tolist()
#
#     inQuestion = str(iarl)
#
#     #for each image array in the solution files
#     for eachExample in loadExamps:
#         #if condition to avoid new line as last line in file
#         if(len(eachExample) > 3):
#             splitEx = eachExample.split('::')
#             currentNum  = splitEx[0]
#             currentAr = splitEx[1]
#
#             #getting list of each individual pixel in this particular solution image
#             eachPixEx = currentAr.split('],')
#
#             #getting list of image we are trying to match
#             eachPixInQ = inQuestion.split('],')
#
#             x=0
#
#             while x < len(eachPixEx):
#                 #if solution image pixel == problem image pixel
#                 if eachPixEx[x] == eachPixEx[x]:
#                     #add identifier of image to a matched array
#                     matchedArr.append(int(currentNum))
#                 x += 1
#     print matchedArr
#     #for every individual number it gives you the number identifier and how many times it's found in the array
#     x = Counter(matchedArr)
#     print x
#
