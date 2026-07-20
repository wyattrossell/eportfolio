#Program name:  Interger finder program
#Date / version / revision: 07/5/2026 / V1.0.0 /
#Programmer(s): Wyatt Rossell
#What the program does: This program will find the min, max and average number in a file containing numbers.  
#Variable: total, average, sum, min, max
#Expected inputs: Interger
#Outputs: output file containing min, max and average for all numbers in file. 
#Limitations: program requires intergers to function. 
#Dependencies: NA
#Included Classes and Functions: 
#Results of testing: see testing document.
#Other:

input_filename = "large.file.of.numbers.txt"
output_filename = "wyatt.rossell.input.file.analysis.txt"

numbers = []
range_counts = [0] * 10

total = 0
count = 0
minimum = 0
maximum = 0
first = True

count0=0
count1=0
count2=0
count3=0
count4=0
count5=0
count6=0
count7=0
count8=0
count9=0

with open(input_filename, "r") as input_file:
    for line in input_file:
        line = line.strip()
        if line == " ":
            continue
        number =int(line)
        total = total + number
        count += 1
        
        if first:
            minimum = number
            maximum = number
            first = False
        else:
            if number < minimum:
                minimum = number
            if number > maximum:
                maximum = number
        
        if number <= 9999:
            count0 += 1
        elif number <= 19999:
            count1 += 1
        elif number <= 29999:
            count2 += 1
        elif number <= 39999:
            count3 += 1
        elif number <= 49999:
            count4 += 1
        elif number <= 59999:
            count5 += 1
        elif number <= 69999:
            count6 += 1
        elif number <= 79999:
            count7 += 1
        elif number <= 89999:
            count8 += 1
        else:
            count9 += 1
            
average = total / count

with open(output_filename, "w") as output_file:
    output_file.write(f"Integers read: {count}\n")
    output_file.write(f"Minimum: {minimum}\n")
    output_file.write(f"Maximum: {maximum}\n")
    output_file.write(f"Average: {average}\n")
    output_file.write("\n")
    output_file.write("Count of integers in each range:\n")
    output_file.write(f"00000 - 09999: {count0}\n")
    output_file.write(f"10000 - 19999: {count1}\n")
    output_file.write(f"20000 - 29999: {count2}\n")
    output_file.write(f"30000 - 39999: {count3}\n")
    output_file.write(f"40000 - 49999: {count4}\n")
    output_file.write(f"50000 - 59999: {count5}\n")
    output_file.write(f"60000 - 69999: {count6}\n")
    output_file.write(f"70000 - 79999: {count7}\n")
    output_file.write(f"80000 - 89999: {count8}\n")
    output_file.write(f"90000 - 99999: {count9}\n")
    output_file.close()
    


print("Program complete, please see your folder for output file.")