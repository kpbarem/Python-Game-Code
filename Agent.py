# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image
from PIL import ImageChops
import math, operator
import random
import numpy as np

import numpy


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self, problem):
        problem_figures = self.get_problem_images(problem)
        solution_figures = self.get_solution_images(problem)
        if self.is_two_by_two_problem(problem):
            if(self.check_all_equal(problem_figures)):
                solution_figure_file_num = self.find_matching_solution_figure(problem_figures[0], solution_figures)
                if solution_figure_file_num:
                    return int(solution_figure_file_num)
            if(self.check_if_a_b_equal(problem_figures)):
                for figure in problem_figures:
                    fileName = figure.visualFilename
                    if ('C.png' in fileName):
                        solution_figure_file_num = self.find_matching_solution_figure(figure, solution_figures)
                        if solution_figure_file_num:
                            return int(solution_figure_file_num)

            if(self.check_if_a_c_equal(problem_figures)):
                for figure in problem_figures:
                    fileName = figure.visualFilename
                    if('B.png' in fileName):
                        solution_figure_file_num = self.find_matching_solution_figure(figure, solution_figures)
                        if(solution_figure_file_num):
                            return int(solution_figure_file_num)

            if(self.check_y_axis_change(problem_figures)):
                for figure in problem_figures:
                    fileName = figure.visualFilename
                    if('C.png' in fileName):
                        solution_figure_file_num = self.find_matching_y_axis_flipped_solution_figure(figure, solution_figures)
                        if(solution_figure_file_num):
                            return int(solution_figure_file_num)
                        else:
                            #checked for mixed transpose
                            solution_figure_file_num =self.find_matching_x_axis_flipped_solution_figure(figure, solution_figures)
                            if(solution_figure_file_num):
                                return int(solution_figure_file_num)

            if(self.check_x_axis_change(problem_figures)):
                for figure in problem_figures:
                    fileName = figure.visualFilename
                    if('B.png' in fileName):
                        solution_figure_file_num = self.find_matching_x_axis_flipped_solution_figure(figure, solution_figures)
                        if(solution_figure_file_num):
                            return int(solution_figure_file_num)
                        else:
                            #checked for mix transpose
                            solution_figure_file_num = self.find_matching_y_axis_flipped_solution_figure(figure, solution_figures)
                            if(solution_figure_file_num):
                                return int(solution_figure_file_num)
        #check percentage difference in dark pixel ratio
            solution_figure_file_num = self.find_dark_pixel_solution(problem_figures, solution_figures)
            return int(solution_figure_file_num)
        elif('Problems D' in problem.problemSetName):
            answer_val = self.solve_D_Problems(problem_figures, solution_figures)
            return int(answer_val)
        elif('Problems E' in problem.problemSetName):
            answer_val = self.solve_E_Problems(problem_figures, solution_figures)
            return int(answer_val)
        answer_val = self.find_solution_for_3by3(problem_figures, solution_figures)
        return int(answer_val)
        #return -1

    def get_problem_images(self, problem):
        problem_figures = []
        file_names = ['A.png', 'B.png', 'C.png', 'D.png', 'E.png', 'F.png', 'G.png', 'H.png']
        for figure in problem.figures:
            thisFigure = problem.figures[figure]
            fileName = thisFigure.visualFilename
            #if file name is one of the problem file names
            if fileName[-5:] in file_names:
                problem_figures.append(thisFigure)
        return problem_figures

    def get_solution_images(self, problem):
        solution_figures = []
        file_names = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png']
        for figure in problem.figures:
            thisFigure = problem.figures[figure]
            fileName = thisFigure.visualFilename
            #if file name is one of the solution file names
            if fileName[-5:] in file_names:
                solution_figures.append(thisFigure)
        return solution_figures

    def is_two_by_two_problem(self, problem):
        return len(problem.figures) == 9

    def high_level_analysis(self, problem):
        problem_figures = self.get_problem_images(problem)
        solution_figures = self.get_solution_images(problem)


    def check_all_equal(self, problem_figures):
        #open visual file name for each
        img1 = Image.open(problem_figures[0].visualFilename)
        img2 = Image.open(problem_figures[1].visualFilename)
        img3 = Image.open(problem_figures[2].visualFilename)
        #check if all are equal
        #reference sum of squares - http://effbot.org/zone/pil-comparing-images.htm
        if (self.calc_root_mean_square_diff(img1, img2) < 960) & (self.calc_root_mean_square_diff(img2, img3) < 960):
            return True
        else:
            return False

    def check_if_a_b_equal(self, problem_figures):
        a_b_img_dict = {}
        for figure in problem_figures:
            fileName = figure.visualFilename
            if ('A.png' in fileName) or ('B.png' in fileName):
                img = Image.open(fileName)
                a_b_img_dict[fileName[-5]] = img
        if(self.calc_root_mean_square_diff(a_b_img_dict['A'], a_b_img_dict['B']) < 960):
            return True
        else:
            return False

    def check_if_a_c_equal(self, problem_figures):
        a_c_img_dict = {}
        for figure in problem_figures:
            fileName = figure.visualFilename
            if('A.png' in fileName) or ('C.png' in fileName):
                img = Image.open(fileName)
                a_c_img_dict[fileName[-5]] = img
        if(self.calc_root_mean_square_diff(a_c_img_dict['A'], a_c_img_dict['C']) < 960):
            return True
        else:
            return False

    def check_y_axis_change(self, problem_figures):
        a_b_img_dict = {}
        for figure in problem_figures:
            fileName = figure.visualFilename
            if('A.png' in fileName) or ('B.png' in fileName):
                img = Image.open(fileName)
                a_b_img_dict[fileName[-5]] = img
        if (self.calc_root_mean_square_diff(a_b_img_dict['A'].transpose(Image.FLIP_LEFT_RIGHT), a_b_img_dict['B']) < 960):
            return True
        else:
            return False


    def check_x_axis_change(self, problem_figures):
        a_c_img_dict = {}
        for figure in problem_figures:
            fileName = figure.visualFilename
            if('A.png' in fileName) or ('C.png' in fileName):
                img = Image.open(fileName)
                a_c_img_dict[fileName[-5]] = img
        if(self.calc_root_mean_square_diff(a_c_img_dict['A'].transpose(Image.FLIP_TOP_BOTTOM), a_c_img_dict['C']) < 960):
            return True
        else:
            return False

    def find_matching_solution_figure(self, problem_figure, solution_figures):
        prob_image = Image.open(problem_figure.visualFilename)
        for figure in solution_figures:
            figure_image = Image.open(figure.visualFilename)
            if(self.calc_root_mean_square_diff(prob_image, figure_image) < 960):
                return figure.visualFilename[-5]


    def find_matching_y_axis_flipped_solution_figure(self, problem_figure, solution_figures):
        prob_image = Image.open(problem_figure.visualFilename).transpose(Image.FLIP_LEFT_RIGHT)
        for figure in solution_figures:
            figure_image = Image.open(figure.visualFilename)
            if(self.calc_root_mean_square_diff(prob_image, figure_image) < 960 ):
                return figure.visualFilename[-5]

    def find_matching_x_axis_flipped_solution_figure(self, problem_figure, solution_figures):
        prob_image = Image.open(problem_figure.visualFilename).transpose(Image.FLIP_TOP_BOTTOM)
        for figure in solution_figures:
            figure_image = Image.open(figure.visualFilename)
            if(self.calc_root_mean_square_diff(prob_image, figure_image) < 960 ):
                return figure.visualFilename[-5]

    def calc_root_mean_square_diff(self, img1, img2):
        hist = ImageChops.difference(img1, img2).histogram()
        return math.sqrt((sum(y*(x**2) for x, y in enumerate(hist)))/(float(img1.size[0] * img2.size[1])))

    def calculate_dark_pixel_ratio_of_image(self, img):
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

    def find_dark_pixel_solution(self, problem_figures, solution_figures):
        # reference Joyner paper http://www.davidjoyner.net/blog/wp-content/uploads/2015/05/JoynerBedwellGrahamLemmonMartinezGoel-ICCC2015-Distribution.pdf
        #reference Python image recognition videos https://www.youtube.com/watch?v=ry9AzwTMwJQ
        for figure in problem_figures:
            fileName = figure.visualFilename
            if('A.png' in fileName):
                aImg = Image.open(fileName)
            elif('B.png' in fileName):
                bImg = Image.open(fileName)
            elif('C.png' in fileName):
                cImg = Image.open(fileName)
        a_ratio = self.calculate_dark_pixel_ratio_of_image(aImg)
        b_ratio = self.calculate_dark_pixel_ratio_of_image(bImg)
        c_ratio = self.calculate_dark_pixel_ratio_of_image(cImg)
        a_b_difference = a_ratio - b_ratio
        c_to_solution_differences = []
        solutionDict = {}
        for solution in solution_figures:
            solutionImage = Image.open(solution.visualFilename)
            difference = c_ratio - self.calculate_dark_pixel_ratio_of_image(solutionImage)
            c_to_solution_differences.append(difference)
            solutionDict[difference] = solution.visualFilename[-5]
        #find the closest one to a_b_difference
        minDifferce =  min(c_to_solution_differences, key=lambda x:abs(x-a_b_difference))
        return solutionDict[minDifferce]

    def find_solution_for_3by3(self, problem_figures, solution_figures):

        for figure in problem_figures:
            fileName = figure.visualFilename
            if('A.png' in fileName):
                aImg = Image.open(fileName)
            elif('B.png' in fileName):
                bImg = Image.open(fileName)
            elif('C.png' in fileName):
                cImg = Image.open(fileName)
            elif('D.png' in fileName):
                dImg = Image.open(fileName)
            elif('E.png' in fileName):
                eImg = Image.open(fileName)
            elif('F.png' in fileName):
                fImg = Image.open(fileName)
            elif('G.png' in fileName):
                gImg = Image.open(fileName)
            elif('H.png' in fileName):
                hImg = Image.open(fileName)



        #get dark pixel ratio for every image
        a_ratio = self.calculate_dark_pixel_ratio_of_image(aImg)
        b_ratio = self.calculate_dark_pixel_ratio_of_image(bImg)
        c_ratio = self.calculate_dark_pixel_ratio_of_image(cImg)
        d_ratio = self.calculate_dark_pixel_ratio_of_image(dImg)
        e_ratio = self.calculate_dark_pixel_ratio_of_image(eImg)
        f_ratio = self.calculate_dark_pixel_ratio_of_image(fImg)
        g_ratio = self.calculate_dark_pixel_ratio_of_image(gImg)
        h_ratio = self.calculate_dark_pixel_ratio_of_image(hImg)

        row1Same = self.check_same_dark_pixel_ratio_in_row(a_ratio, b_ratio, c_ratio)
        row2Same = self.check_same_dark_pixel_ratio_in_row(d_ratio, e_ratio, f_ratio)

        solution_dark_pixel_ratio_dict = self.get_ratios_for_solution_figures(solution_figures)
        #if row 1 and 2 are the same then find a solution for row 3
        if(row1Same & row2Same):
            ans = self.get_solution_with_same_dark_pixel_ratio(h_ratio, solution_dark_pixel_ratio_dict);
            if(ans):
                return int(ans)

        #check for incrementing dark pixel ratio
        if(self.are_pixels_increasing_or_decreasing(a_ratio, b_ratio, c_ratio, d_ratio, e_ratio, f_ratio)):
            ans = self.get_incrementing_solution(g_ratio, h_ratio, solution_dark_pixel_ratio_dict)
            if(ans):
                return int(ans)

        if(self.are_pixels_increasing_or_decreasing(c_ratio, b_ratio, a_ratio, f_ratio, e_ratio, d_ratio)):
            ans = self.get_decrementing_solution(g_ratio, h_ratio, solution_dark_pixel_ratio_dict)
            if(ans):
                return int(ans)

        ans = self.check_diag_mixed_transpose(aImg, solution_figures )
        if(ans):
            return int(ans)

        # ans = self.calculate_average_DPR(a_ratio, b_ratio, c_ratio, d_ratio, e_ratio, f_ratio, g_ratio, h_ratio, solution_dark_pixel_ratio_dict)
        ipr_ratio = self.calculate_intersectional_pixel_ratio(gImg, hImg)
        ans = self.find_closest_ipr_ratio(ipr_ratio, hImg, solution_figures)
        return int(ans)

        return ans


    def check_same_dark_pixel_ratio_in_row(self, item_1, item_2, item_3):
        diffItem1And2 = item_1 - item_2
        diffItem2And3 = item_2 - item_3
        #essentially no difference
        if(abs(diffItem1And2) < .001 and abs(diffItem2And3) < .001):
            return True
        else:
            return False

    def get_solution_with_same_dark_pixel_ratio(self, prob_ratio, solution_dark_pixel_ratio_dict):
        for key,solRatio in solution_dark_pixel_ratio_dict.items():
            diffProbRatioAndSolRatio = prob_ratio - solRatio
            if(abs(diffProbRatioAndSolRatio)<.001):
                return key


    def get_ratios_for_solution_figures(self, solution_figures):


        solution_dark_pixel_ratio_dict = {}
        for figure in solution_figures:
            fileName = figure.visualFilename
            if('1.png' in fileName):
                oneImg = Image.open(fileName)
                one_ratio = self.calculate_dark_pixel_ratio_of_image(oneImg)
                solution_dark_pixel_ratio_dict[fileName[-5]] = one_ratio
            elif('2.png' in fileName):
                twoImg = Image.open(fileName)
                two_ratio = self.calculate_dark_pixel_ratio_of_image(twoImg)
                solution_dark_pixel_ratio_dict[fileName[-5]] = two_ratio
            elif('3.png' in fileName):
                threeImg = Image.open(fileName)
                three_ratio = self.calculate_dark_pixel_ratio_of_image(threeImg)
                solution_dark_pixel_ratio_dict[fileName[-5]] = three_ratio
            elif('4.png' in fileName):
                fourImg = Image.open(fileName)
                four_ratio = self.calculate_dark_pixel_ratio_of_image(fourImg)
                solution_dark_pixel_ratio_dict[fileName[-5]] = four_ratio
            elif('5.png' in fileName):
                fiveImg = Image.open(fileName)
                five_ratio = self.calculate_dark_pixel_ratio_of_image(fiveImg)
                solution_dark_pixel_ratio_dict[fileName[-5]] = five_ratio
            elif('6.png' in fileName):
                sixImg = Image.open(fileName)
                six_ratio = self.calculate_dark_pixel_ratio_of_image(sixImg)
                solution_dark_pixel_ratio_dict[fileName[-5]] = six_ratio
            elif('7.png' in fileName):
                sevenImg = Image.open(fileName)
                seven_ratio = self.calculate_dark_pixel_ratio_of_image(sevenImg)
                solution_dark_pixel_ratio_dict[fileName[-5]] = seven_ratio
            elif('8.png' in fileName):
                eightImg = Image.open(fileName)
                eight_ratio = self.calculate_dark_pixel_ratio_of_image(eightImg)
                solution_dark_pixel_ratio_dict[fileName[-5]] = eight_ratio

        return solution_dark_pixel_ratio_dict


    def are_pixels_increasing_or_decreasing(self, x,y,z, a,b,c):
        if(x<y and y<z and a<b and b<c):
            return True
        else:
            return False


    def get_incrementing_solution(self, g_ratio, h_ratio, solution_dark_pixel_ratio_dict):
        diffGH = g_ratio - h_ratio
        expectedRatio = h_ratio + abs(diffGH)

        minDiff = 1000000000
        minKey = ""
        for key, solRatio in solution_dark_pixel_ratio_dict.items():
            diff = abs(solRatio-expectedRatio)
            if(diff < minDiff):
                minDiff = diff
                minKey = key
        return minKey
    
    def get_decrementing_solution(self, g_ratio, h_ratio, solution_dark_pixel_ratio_dict):
        diffGH = g_ratio - h_ratio
        expectedRatio = h_ratio - abs(diffGH)
        
        #find the closest value to this 
        minDiff = 1000000000
        minKey = ""
        for key, solRatio in solution_dark_pixel_ratio_dict.items():
            diff = abs(solRatio-expectedRatio)
            if(diff < minDiff):
                minDiff = diff
                minKey = key
        return minKey


    def calculate_average_DPR(self, a_ratio, b_ratio, c_ratio, d_ratio, e_ratio, f_ratio, g_ratio, h_ratio, solution_dark_pixel_ratio_dict):
        expectedRatio = (a_ratio + b_ratio + c_ratio + d_ratio + e_ratio + f_ratio + g_ratio + h_ratio)/8

        #find the closest value to the average
        minDiff = 1000000000
        minKey = ""
        for key, solRatio in solution_dark_pixel_ratio_dict.items():
            diff = abs(solRatio-expectedRatio)
            if(diff < minDiff):
                minDiff = diff
                minKey = key
        return minKey

    def check_diag_mixed_transpose(self, aImg, solution_figures):
        prob_image = aImg.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
        for figure in solution_figures:
            figure_image = Image.open(figure.visualFilename)
            if(self.calc_root_mean_square_diff(prob_image, figure_image) < 960 ):
                return figure.visualFilename[-5]

    def calculate_intersectional_pixel_ratio(self, img1, img2):
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

    def find_closest_ipr_ratio(self,ipr_ratio, hImg, solution_figures):
        minDiff = 1000000.00

        for figure in solution_figures:
            solutionIPR = self.calculate_intersectional_pixel_ratio(Image.open(figure.visualFilename), hImg)
            solDiff = abs(solutionIPR - ipr_ratio)
            if solDiff < minDiff:
                minDiff = solDiff
                ans = figure.visualFilename[-5]

        return ans;


    #trying various solutions that work on D problem figures
    def solve_D_Problems(self, problem_figures, solution_figures):


        #check diaganol similarity
        if(self.checkDiaganolSimilarity(problem_figures)):
            for problem in problem_figures:
                fileName = problem.visualFilename
                if('A.png' in fileName):
                    ans = self.find_matching_solution_figure(problem, solution_figures)
                    if(ans):
                        return int(ans)


        for figure in problem_figures:
            fileName = figure.visualFilename
            if('A.png' in fileName):
                aImg = Image.open(fileName)
            elif('B.png' in fileName):
                bImg = Image.open(fileName)
            elif('C.png' in fileName):
                cImg = Image.open(fileName)
            elif('D.png' in fileName):
                dImg = Image.open(fileName)
            elif('E.png' in fileName):
                eImg = Image.open(fileName)
            elif('F.png' in fileName):
                fImg = Image.open(fileName)
            elif('G.png' in fileName):
                gImg = Image.open(fileName)
            elif('H.png' in fileName):
                hImg = Image.open(fileName)

        #check if dark pixel ratio the same across row
        aDPRatio = self.calculate_dark_pixel_ratio_of_image(aImg)
        bDPRatio = self.calculate_dark_pixel_ratio_of_image(bImg)
        cDPRatio = self.calculate_dark_pixel_ratio_of_image(cImg)
        if((aDPRatio == bDPRatio) and (bDPRatio == cDPRatio)):
            hDPRatio = self.calculate_dark_pixel_ratio_of_image(hImg)
            solution_dark_pixel_ratio_dict = self.get_ratios_for_solution_figures(solution_figures);
            ans = self.get_solution_with_same_dark_pixel_ratio(hDPRatio, solution_dark_pixel_ratio_dict);
            if(ans):
                return int(ans)


        #check if row DPR is the same
        firstRowRatioTotal = aDPRatio + bDPRatio + cDPRatio
        dDPRatio = self.calculate_dark_pixel_ratio_of_image(dImg)
        eDPRatio = self.calculate_dark_pixel_ratio_of_image(eImg)
        fDPRatio = self.calculate_dark_pixel_ratio_of_image(fImg)
        secondRowRatioTotal = dDPRatio + eDPRatio + fDPRatio
        if(firstRowRatioTotal == secondRowRatioTotal):
            gDPRatio = self.calculate_dark_pixel_ratio_of_image(gImg)
            hDPRatio = self.calculate_dark_pixel_ratio_of_image(hImg)
            solution_dark_pixel_ratio_dict = self.get_ratios_for_solution_figures(solution_figures);
            answerRatio = firstRowRatioTotal - (gDPRatio + hDPRatio)
            ans = self.get_solution_with_closest_dark_pixel_ratio(answerRatio, solution_dark_pixel_ratio_dict)
            if(ans):
                return int(ans)

        gDPRatio = self.calculate_dark_pixel_ratio_of_image(gImg)
        hDPRatio = self.calculate_dark_pixel_ratio_of_image(hImg)

        problemDPRatiosArray = [aDPRatio, bDPRatio, cDPRatio, eDPRatio, fDPRatio, gDPRatio, hDPRatio]
        problem_images_array = [aImg, bImg, cImg, dImg, eImg, fImg, gImg, hImg]


        if(self.check_if_all_images_unique_using_RMS(problem_images_array)):
            final_solution_figures = self.removeDuplicateSolutionImages(problem_figures, solution_figures)
            solution_dark_pixel_ratio_dict = self.get_ratios_for_solution_figures(final_solution_figures)
            avgRatio = (gDPRatio + hDPRatio)/2
            ans = self.getMinDiffDPR(avgRatio, solution_dark_pixel_ratio_dict)
            if(ans):
                return int(ans)


        return -1

    def get_solution_with_closest_dark_pixel_ratio(self, problemRatio, solution_dark_pixel_ratio_dict):
        minDiff = 1000000;
        for key, solRatio in solution_dark_pixel_ratio_dict.items():
            diff = abs(solRatio-problemRatio)
            if(diff < minDiff):
                minDiff = diff
                minKey = key
        return minKey

    def checkIfAllImagesUnique(self, problemDPRatiosArray):
        if(len(problemDPRatiosArray)  > len(set(problemDPRatiosArray))):
            return False
        else:
            return True

    def removeDuplicateSolutionImages(self, problem_figures, solution_figures):
        duplicate = False;
        final_solution_figures = [];
        for solution_figure in solution_figures:
            duplicate = False;
            solution_img = Image.open(solution_figure.visualFilename);
            for problem_figure in problem_figures:
                problem_img = Image.open(problem_figure.visualFilename);
                if(self.calc_root_mean_square_diff(problem_img, solution_img) < 963):
                    duplicate = True
            if(not(duplicate)):
                final_solution_figures.append(solution_figure)
        return final_solution_figures;

    def getMinDiffDPR(self, avgRatio, solution_dark_pixel_ratio_dict):
        minDiff = 1000000000
        minKey = ""
        for key, solRatio in solution_dark_pixel_ratio_dict.items():
            diff = abs(solRatio-avgRatio)
            if(diff < minDiff):
                minDiff = diff
                minKey = key
        return minKey

    def checkDiaganolSimilarity(self, problem_figures):
        for problem in problem_figures:
            fileName = problem.visualFilename
            if 'A.png' in fileName:
                aImg = Image.open(fileName)
            elif 'E.png' in fileName:
                eImg = Image.open(fileName)
        if(self.calc_root_mean_square_diff(aImg,eImg) < 965):
            return True;

    def solve_E_Problems(self, problem_figures, solution_figures):
        for problem_figure in problem_figures:
            fileName = problem_figure.visualFilename
            if('A.png' in fileName):
                aImg = Image.open(fileName)
            elif('B.png' in fileName):
                bImg = Image.open(fileName)
            elif('C.png' in fileName):
                cImg = Image.open(fileName)
            elif('D.png' in fileName):
                dImg = Image.open(fileName)
            elif('E.png' in fileName):
                eImg = Image.open(fileName)
            elif('F.png' in fileName):
                fImg = Image.open(fileName)
            elif('G.png' in fileName):
                gImg = Image.open(fileName)
            elif('H.png' in fileName):
                hImg = Image.open(fileName)

        rowUnionFirstRowImage = self.getUnionFigure(aImg, bImg)
        if(self.calc_root_mean_square_diff(rowUnionFirstRowImage, cImg) < 963):
            rowUnionImage = self.getUnionFigure(gImg, hImg)
            ans = self.find_matching_solution_image(rowUnionImage, solution_figures)
            if(ans):
                return int(ans)

        dprRatioA = self.calculate_dark_pixel_ratio_of_image(aImg)
        dprRatioB = self.calculate_dark_pixel_ratio_of_image(bImg)
        dprRatioC = self.calculate_dark_pixel_ratio_of_image(cImg)
        dprRatioD = self.calculate_dark_pixel_ratio_of_image(dImg)
        dprRatioE = self.calculate_dark_pixel_ratio_of_image(eImg)
        dprRatioF = self.calculate_dark_pixel_ratio_of_image(fImg)
        dprRatioG = self.calculate_dark_pixel_ratio_of_image(gImg)
        dprRatioH = self.calculate_dark_pixel_ratio_of_image(hImg)

        problemDPRRatiosArray = [dprRatioA, dprRatioB, dprRatioC, dprRatioD, dprRatioE, dprRatioF, dprRatioG, dprRatioH]
        problemImages = [aImg, bImg, cImg, dImg, eImg, fImg, gImg, hImg]
        if(self.check_if_all_images_unique_using_RMS(problemImages)):
            #reduce solution set
            solution_figures = self.removeDuplicateSolutionImages(problem_figures, solution_figures)

        #check subtraction DPR
        subtractedRowDPR = abs(dprRatioG - dprRatioH)
        solution_dark_pixel_ratio_dict = self.get_ratios_for_solution_figures(solution_figures)
        ans = self.getMinDiffDPR(subtractedRowDPR, solution_dark_pixel_ratio_dict)
        if(ans):
            return int(ans)
        else:
            return -1


    def getUnionFigure(self, gImg, hImg):
        gImg = gImg.convert("1")
        hImg = hImg.convert("1")
        rowUnionImage = ImageChops.logical_and(gImg, hImg)
        rowUnionImage = rowUnionImage.convert("RGBA")
        return rowUnionImage

    def find_matching_solution_image(self, candidateImage, solution_figures):
        for figure in solution_figures:
            figure_image = Image.open(figure.visualFilename)
            if(self.calc_root_mean_square_diff(candidateImage, figure_image) < 963):
                return figure.visualFilename[-5]

    def check_if_all_images_unique_using_RMS(self, problem_images):
        duplicates = 0;
        dupicateValuesBool = False;
        for image in problem_images:
            for innerImage in problem_images:
                if(self.calc_root_mean_square_diff(image, innerImage) < 963):
                    duplicates = duplicates+1
            if duplicates > 1:
                duplicateValuesBool = True;
                break;
        return duplicateValuesBool
