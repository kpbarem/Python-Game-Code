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
        if self.is_two_by_two_problem:
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
        #return random.randint(1,7)# print random number between 1 and 6
            #self.additionalAnalysis(problem_figures)
        #return -1

    def get_problem_images(self, problem):
        problem_figures = []
        file_names = ['A.png', 'B.png', 'C.png']
        for figure in problem.figures:
            thisFigure = problem.figures[figure]
            fileName = thisFigure.visualFilename
            #if file name is one of the problem file names
            if fileName[-5:] in file_names:
                problem_figures.append(thisFigure)
        return problem_figures

    def get_solution_images(self, problem):
        solution_figures = []
        file_names = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png']
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
