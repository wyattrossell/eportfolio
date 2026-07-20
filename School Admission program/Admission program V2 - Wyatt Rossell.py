#Program name:  Admission for college's admission office (updated)
#Date / version / revision: 06/27/2026 / V2.0.0 /
#Programmer(s): Wyatt Rossell
#What the program does: This program allow for a user to enter their name, gpa, and test score to determine if they will be accepted or not.
#Variable: name, gpa, test_score
#Expected inputs: string, float, integar
#Outputs: acceptance message
#Limitations: This program does not allow gpa passed one decimal point.
#Dependencies: None
#Included Classes and Functions: none
#Results of testing: see testing document.
#Other: Program utilitzes functions which are called in the main line logic.

gpa_req = 3.0
low_test = 60
high_test = 80

def get_name(prompt="Enter your name: "):
    while True:
        name = input(prompt).strip()
        if name != " ":
            return name
        else:
            print("Invalid input. Name cannot be empty.")

def get_result(full_name):
    while True:
        try:
            gpa = float(input("Please enter your GPA: "))
            if 0 <= gpa <= 4.0:
                break
        except ValueError:
            print("Please enter a your GPA. It should be between 0.0 and 4.0")
        
    while True:
        try:
            score = int(input("Please enter you test score: "))
            if 0 <= score <= 100:
               break
        except ValueError:
            print("Please enter your test score. This should be a whole number: ")
        
    if gpa >= gpa_req and score >= low_test:
        print(full_name + ", Congradulations you have been accepted!")
    elif gpa < gpa_req and score >= high_test:
        print(full_name + ", Congradulations you have been accepted!")
    else:
        print(full_name+ ", Sorry, you have been rejected.")


def main():
    print("Hello, and welcome to my college's admission program. You will be asked to enter your name, GPA, and test results to determine admission to the program.")
    print("or type stop if you are done entering students.")
    while input != "stop" or "Stop":
        full_name = get_name()
        get_result(full_name)
    
main()
