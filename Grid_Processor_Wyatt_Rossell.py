#Program name:  Grid Processor
#Date / version / revision: 06/20/2026 / V1.0.0 /
#Programmer(s): Wyatt Rossell
#What the program does: Generates a grid that is 10 number across and 10 number tall of random numbers. 
#Variable: total, row, rows, column, columns, average, difference. 
#Expected inputs: string, float, integar
#Outputs: acceptance message
#Limitations: program requires real numbers to be used for inputs. 
#Dependencies: random, math
#Included Classes and Functions: none
#Results of testing: see testing document.
#Other: Program uses while loops in order to interate the grid patterns. 

import random
import math

#prompt to get first input from user for rows and columns desired. 
rows=int(input("Please enter the number of rows you would like: "))
columns=int(input("Please enter the number of columns you would like: "))

#making sure to set varables to zero so we interate correctly during the while loop. 
total=0
row=0

#while loop for the first grid.
while row<rows:
    column=0
    while column<columns:
        grid1=random.randint(0, 99)
        print(grid1, end=" ")
        total = total + grid1
        column=column +1
    print()
    row = row + 1

#total and average of all numbers.
average = total / (rows * columns)
print()
print("Total:", total)
print("Average:", average)

#while loop for second grid with 49.5 average
row=0
while row<rows:
    column=0
    while column<columns:
        grid2 = random.randint(0, 99)
        difference = 49.5 - grid2
        print(difference, end=" ")
        column = column + 1
    print()
    row = row + 1
    
    