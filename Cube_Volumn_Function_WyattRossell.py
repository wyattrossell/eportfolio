#Program name:  Cube Volumn Function
#Date / version / revision: 06/27/2026 / V1.0.0 /
#Programmer(s): Wyatt Rossell
#What the program does: Calculates the volumn of a cube.
#Variable: volumn, lenght, width, height
#Expected inputs: float, integer
#Outputs: reads back the entered data and the calculation of the volumn. 
#Limitations: program requires real numbers to be used for inputs. 
#Dependencies: math
#Included Classes and Functions: postive_int, main
#Results of testing: program will check for positive intergers and reject negative and non number inputs. 
#Other: 

import math


def total_volumn():
    length = positive_int("Please enter the lenght: ")
    width = positive_int("Please enter the width: ")
    height = positive_int("Please enter the height: ")
    volumn = length * width * height    
    print(f"You entered: {length}, {width}, {height}, ")
    print(f"which makes the volumn of the cube: {volumn}")    

def positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Please enter a positive number:")
        except ValueError:
            print("Invalid input. Please enter a number: ")
            
def main():
    print("Welcome to the cube volumn calcuator ")
    print("This program will take the lenght, width, and height ")
    print("and give you the volumn of the cube.")
    
    
main()

total_volumn()