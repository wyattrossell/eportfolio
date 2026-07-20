#Program name:  Square root calculator
#Date / version / revision: 06/04/2026 / V1.0.0 / 
#Programmer(s): Wyatt Rossell
#What the program does: This program take a user inputed number and displays the square root of the number.
#Variable names, types, and definitions: num, integer, is the variable defined by user input. sqrt_value, in the square root of the varialbe num, takes the num variable and square roots it. 
#Expected inputs: integer
#Outputs: square root of expected input. 
#Limitations: This program will not accept fractions or number with decimel places. (float)
#Dependencies: math module.
#ncluded Classes and Functions: from math sqrt
#Results of testing: program works well with integers. program breaks when fractions or decimal number are inputed. 
#Other: This is my first calculator in python. yeah. excitement!!! 

import math

#from math import sqrt

#prompt user for an integer
num = int(input("Enter an integer: "))

#calculate square root as a float

sqrt_value = math.sqrt(num)
#sqrt_value = sqrt(num)

#print the raw float
print('Square root (float):', sqrt_value)

#skip two lines
print('\n\n')

#print the float rounded to 2 decemal places
print('Square root (rounded to 2 decimal placed): {:.2f}'.format(sqrt_value))
