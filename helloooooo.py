from PIL import Image
from PIL import ImageChops
from PIL import ImageMath
from PIL import ImageOps
import numpy as np
import math
import time

problemImageG = Image.open('Problems/Basic Problems D/Basic Problem D-10/G.png')
problemImageH = Image.open('Problems/Basic Problems D/Basic Problem D-10/H.png')
problemImageC = Image.open('Problems/Basic Problems D/Basic Problem D-10/C.png')
problemImageF = Image.open('Problems/Basic Problems D/Basic Problem D-10/F.png')
problemImageA = Image.open('Problems/Basic Problems D/Basic Problem D-10/A.png')
problemImageE = Image.open('Problems/Basic Problems D/Basic Problem D-10/E.png')
problemImageB = Image.open('Problems/Basic Problems D/Basic Problem D-10/B.png')
problemImageD = Image.open('Problems/Basic Problems D/Basic Problem D-10/D.png')

solutionImage1 = Image.open('Problems/Basic Problems D/Basic Problem D-10/1.png')
solutionImage2 = Image.open('Problems/Basic Problems D/Basic Problem D-10/2.png')
solutionImage3 = Image.open('Problems/Basic Problems D/Basic Problem D-10/3.png')
solutionImage4 = Image.open('Problems/Basic Problems D/Basic Problem D-10/4.png')
solutionImage5 = Image.open('Problems/Basic Problems D/Basic Problem D-10/5.png')
solutionImage6 = Image.open('Problems/Basic Problems D/Basic Problem D-10/6.png')
solutionImage7 = Image.open('Problems/Basic Problems D/Basic Problem D-10/7.png')
solutionImage8 = Image.open('Problems/Basic Problems D/Basic Problem D-10/8.png')


def calc_root_mean_square_diff(img1, img2):
    hist = ImageChops.difference(img1, img2).histogram()
    return math.sqrt((sum(y*(x**2) for x, y in enumerate(hist)))/(float(img1.size[0] * img2.size[1])))

print('difference between 1 and D is ' + str(calc_root_mean_square_diff(solutionImage1, problemImageD)));


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

def imageMultiply(img1, img2):
    img1 = img1.convert("1")
    img2 = img2.convert("1")
    solution = ImageChops.multiply(img1, img2)
    solution.convert("RGBA")
    solution.show()

def imageUnion(probImg, probImg2):

    probImg = probImg.convert("1")
    probImg2 = probImg2.convert("1")
    solved = ImageChops.logical_and(probImg, probImg2)

    solved = solved.convert("RGBA");

    return solved

# solved = imageUnion(problemImageA, problemImageB)
#
# problemImageE.show()
# problemImageH.show()
#
# print(calc_root_mean_square_diff(problemImageE, problemImageH))




# imageMultiply(problemImageG, problemImageH)
# dprRatioA = calculate_dark_pixel_ratio_of_image(problemImageA)
# dprRatioB = calculate_dark_pixel_ratio_of_image(problemImageB)
# dprRatioC = calculate_dark_pixel_ratio_of_image(problemImageC)
# dprRatioD = calculate_dark_pixel_ratio_of_image(problemImageD)
# dprRatioE = calculate_dark_pixel_ratio_of_image(problemImageE)
# dprRatioF = calculate_dark_pixel_ratio_of_image(problemImageF)
# dprRatioG = calculate_dark_pixel_ratio_of_image(problemImageG)
# drpRatioH = calculate_dark_pixel_ratio_of_image(problemImageH)
#
# dprSubtractLastRow = abs(dprRatioG - drpRatioH)
#
# print('The DPR for G is ' + str(dprRatioG))
# print('The DPR for H is ' + str(drpRatioH))
#
#
# print('DPR subtraction of last row is ' + str(dprSubtractLastRow))
#
# dprRatio1 = calculate_dark_pixel_ratio_of_image(solutionImage1)
# dprRatio2 = calculate_dark_pixel_ratio_of_image(solutionImage2)
# dprRatio3 = calculate_dark_pixel_ratio_of_image(solutionImage3)
# dprRatio4 = calculate_dark_pixel_ratio_of_image(solutionImage4)
# dprRatio5 = calculate_dark_pixel_ratio_of_image(solutionImage5)
# dprRatio6 = calculate_dark_pixel_ratio_of_image(solutionImage6)
# dprRatio7 = calculate_dark_pixel_ratio_of_image(solutionImage7)
# dprRatio8 = calculate_dark_pixel_ratio_of_image(solutionImage8)
#
# print('DPR ratio for solution image 1 ' + str(dprRatio1))
# print('DPR ratio for solution image 2 ' + str(dprRatio2))
# print('DPR ratio for solution image 3 ' + str(dprRatio3))
# print('DPR ratio for solution image 4 ' + str(dprRatio4))
# print('DPR ratio for solution image 5 ' + str(dprRatio5))
# print('DPR ratio for solution image 6 ' + str(dprRatio6))
# print('DPR ratio for solution image 7 ' + str(dprRatio7))
# print('DPR ratio for solution image 8 ' + str(dprRatio8))
