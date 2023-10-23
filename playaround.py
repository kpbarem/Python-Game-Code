from PIL import Image
from PIL import ImageChops
from PIL import ImageMath
from PIL import ImageOps
import numpy as np
import math
import time
#comes with python
from collections import Counter


# x= 0.0723062381853
# y = 0.0725425330813
# z = 0.0727788279773


problemImageG = Image.open('Problems/Basic Problems E/Basic Problem E-04/G.png')
problemImageH = Image.open('Problems/Basic Problems E/Basic Problem E-04/H.png')
problemImageC = Image.open('Problems/Basic Problems E/Basic Problem E-04/C.png')
problemImageF = Image.open('Problems/Basic Problems E/Basic Problem E-04/F.png')
problemImageA = Image.open('Problems/Basic Problems E/Basic Problem E-04/A.png')
problemImageE = Image.open('Problems/Basic Problems E/Basic Problem E-04/E.png')
problemImageB = Image.open('Problems/Basic Problems E/Basic Problem E-04/B.png')

solutionImage1 = Image.open('Problems/Basic Problems E/Basic Problem E-04/1.png')
solutionImage2 = Image.open('Problems/Basic Problems E/Basic Problem E-04/2.png')

def calc_root_mean_square_diff(img1, img2):
    hist = ImageChops.difference(img1, img2).histogram()
    return math.sqrt((sum(y*(x**2) for x, y in enumerate(hist)))/(float(img1.size[0] * img2.size[1])))


def imageUnion(problemImageC, problemImageF, solutionImage1):

    problemImageC = problemImageC.convert("1")
    problemImageF = problemImageF.convert("1")
    solved = ImageChops.logical_and(problemImageC, problemImageF)

    solved = solved.convert("RGBA")
    solved.show();

    print(calc_root_mean_square_diff(solved, solutionImage1))

def imageSubtraction(probImage, probImage2):
    probImage = probImage.convert("1")
    probImage2 = probImage2.convert("1")

    solved = ImageChops.subtract_modulo(probImage, probImage2)
    solved.convert("RGBA")
    solved.show();




def calculate_intersectional_pixel_ratio(img1, img2):
    img1Array = np.array(img1)
    img2Array = np.array(img2)

    i = 0;
    j=0;
    intersection = 0;
    whitePixelArray = np.array([255,255,255,255])
    darkPixelCounter = 0;
    #each row
    for i in range(0, img1Array.__len__()):
        #each pix
        for j in range(0, img1Array[i].__len__()):
            if(not np.array_equal(img1Array[i][j], whitePixelArray)):
                darkPixelCounter +=1
                if np.array_equal(img1Array[i][j], img2Array[i][j]):
                    intersection+=1
            if(not np.array_equal(img2Array[i][j], whitePixelArray)):
                darkPixelCounter+=1
    return float((float(intersection*2))/float(darkPixelCounter))





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




ratio1 = calculate_dark_pixel_ratio_of_image(problemImageG)
ratio2 = calculate_dark_pixel_ratio_of_image(problemImageH)
ratioC = calculate_dark_pixel_ratio_of_image(problemImageC)
ratioF = calculate_dark_pixel_ratio_of_image(problemImageF)
ratioA = calculate_dark_pixel_ratio_of_image(problemImageA)
ratioE = calculate_dark_pixel_ratio_of_image(problemImageE)

print('G ratio ' + str(ratio1))
print('H ratio ' + str(ratio2))
print('C ratio ' + str(ratioC))
print('F ratio ' + str(ratioF))
print('A ratio ' + str(ratioA))
print('E ratio ' + str(ratioE))


possibleSolution = abs(ratio1 - ratio2)


print('possible solution ' + str(possibleSolution));



#solution figure ratios

solutionImage1 = Image.open('Problems/Basic Problems D/Basic Problem D-04/1.png')
solutionImage2 = Image.open('Problems/Basic Problems D/Basic Problem D-04/2.png')
solutionImage3 = Image.open('Problems/Basic Problems D/Basic Problem D-04/3.png')
solutionImage4 = Image.open('Problems/Basic Problems D/Basic Problem D-04/4.png')
solutionImage5 = Image.open('Problems/Basic Problems D/Basic Problem D-04/5.png')
solutionImage6 = Image.open('Problems/Basic Problems D/Basic Problem D-04/6.png')
solutionImage7 = Image.open('Problems/Basic Problems D/Basic Problem D-04/7.png')
solutionImage8 = Image.open('Problems/Basic Problems D/Basic Problem D-04/8.png')

solutionRatio1 = calculate_dark_pixel_ratio_of_image(solutionImage1)
solutionRatio2 = calculate_dark_pixel_ratio_of_image(solutionImage2)
solutionRatio3 = calculate_dark_pixel_ratio_of_image(solutionImage3)
solutionRatio4 = calculate_dark_pixel_ratio_of_image(solutionImage4)
solutionRatio5 = calculate_dark_pixel_ratio_of_image(solutionImage5)
solutionRatio6 = calculate_dark_pixel_ratio_of_image(solutionImage6)
solutionRatio7 = calculate_dark_pixel_ratio_of_image(solutionImage7)
solutionRatio8 = calculate_dark_pixel_ratio_of_image(solutionImage8)

print('1 Ratio ' + str(solutionRatio1))
print('2 Ratio ' + str(solutionRatio2))
print('3 Ratio ' + str(solutionRatio3))
print('4 Ratio ' + str(solutionRatio4))
print('5 Ratio ' + str(solutionRatio5))
print('6 Ratio ' + str(solutionRatio6))
print('7 Ratio ' + str(solutionRatio7))
print('8 Ratio ' + str(solutionRatio8))


intersectionalPixelRatioForRow = calculate_intersectional_pixel_ratio(problemImageG, problemImageH)
intersectionalPixelRatioForColumn = calculate_intersectional_pixel_ratio(problemImageC, problemImageF)
intersectionalPixelRatioForDiag = calculate_intersectional_pixel_ratio(problemImageA, problemImageE);
intersectionalPixelRatioForH1 = calculate_intersectional_pixel_ratio(problemImageH, solutionImage1)
intersectionalPixelRatioForH2 = calculate_intersectional_pixel_ratio(problemImageH, solutionImage2)
intersectionalPixelRatioForH3 = calculate_intersectional_pixel_ratio(problemImageH, solutionImage3)
intersectionalPixelRatioForH4 = calculate_intersectional_pixel_ratio(problemImageH, solutionImage4)
intersectionalPixelRatioForH5 = calculate_intersectional_pixel_ratio(problemImageH, solutionImage5)
intersectionalPixelRatioForH6 = calculate_intersectional_pixel_ratio(problemImageH, solutionImage6)
intersectionalPixelRatioForH7 = calculate_intersectional_pixel_ratio(problemImageH, solutionImage7)
intersectionalPixelRatioForH8 = calculate_intersectional_pixel_ratio(problemImageH, solutionImage8)
print('Intersectional Pixel Ratio For Row ' + str(intersectionalPixelRatioForRow))
print('Intersectional Pixel Ratio For Column ' + str(intersectionalPixelRatioForColumn))
print('Intersectional Pixel Ratio For Diag ' + str(intersectionalPixelRatioForDiag))
print('Intersectional Pixel Ratio For H and 1 ' + str(intersectionalPixelRatioForH1))
print('Intersectional Pixel Ratio For H and 2 ' + str(intersectionalPixelRatioForH2))
print('Intersectional Pixel Ratio For H and 3 ' + str(intersectionalPixelRatioForH3))
print('Intersectional Pixel Ratio For H and 4 ' + str(intersectionalPixelRatioForH4))
print('Intersectional Pixel Ratio For H and 5 ' + str(intersectionalPixelRatioForH5))
print('Intersectional Pixel Ratio For H and 6 ' + str(intersectionalPixelRatioForH6))
print('Intersectional Pixel Ratio For H and 7 ' + str(intersectionalPixelRatioForH7))
print('Intersectional Pixel Ratio For H and 8 ' + str(intersectionalPixelRatioForH8))



rootmeandiff = calc_root_mean_square_diff(problemImageA, solutionImage4)
print('check the root mean diff ' + str(rootmeandiff))

def check_if_values_are_the_same(x,y,z):
    diffXY = x-y
    diffYZ = y-z

    if(abs(diffXY) < .001 and abs(diffYZ) < .001):
        print('These three are the same')
    else:
        print('These three are not the same')

def are_pixels_increasing_or_decreasing(x,y,z, a,b,c):
    if(x>y and y>z and a>b and b>c):
        return True
    else:
        return False





diff = calc_root_mean_square_diff(problemImageG, solutionImage3)
print('comparison ' +str(diff))




##mixed transpose
def mixed_transpose(img1, img2):
    tempImg = img1.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
    newImg1 = tempImg.transpose(Image.FLIP_TOP_BOTTOM)

    print(calc_root_mean_square_diff(tempImg, img2))

    if (calc_root_mean_square_diff(tempImg, img2) < 960):
        print('True')
    else:
        print('False')


def calculate_intersectional_pixel_ratio(img1, img2):
    img1Array = np.array(img1)
    img2Array = np.array(img2)

    i = 0;
    j=0;
    intersection = 0;
    whitePixelArray = np.array([255,255,255,255])
    darkPixelCounter = 0;
    #each row
    for i in range(0, img1Array.__len__()):
        #each pix
        for j in range(0, img1Array[i].__len__()):
            if(not np.array_equal(img1Array[i][j], whitePixelArray)):
                darkPixelCounter +=1
                if np.array_equal(img1Array[i][j], img2Array[i][j]):
                    intersection+=1
            if(not np.array_equal(img2Array[i][j], whitePixelArray)):
                darkPixelCounter+=1
    return float((float(intersection*2))/float(darkPixelCounter))

# calculate_intersectional_pixel_ratio(problemImage, problemImage)


#check_if_values_are_the_same(x,y,z)




