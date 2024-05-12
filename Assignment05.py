# ------------------------------------------------------------------------------------------ #
# Title: Assignment05
# Desc: This assignment demonstrates using conditional logic and looping
# Change Log: (Who, When, What)
#   Patrick Moynihan, 2024-05-10, Created Script
# ------------------------------------------------------------------------------------------ #
from typing import IO
import json

# Define the Data Constants

MENU: str = '''
------ Course Registration Program ------
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"
KEYS: list = ["FirstName", "LastName", "CourseName"]

# Define the Data Variables

student_first_name: str = ''  # Holds the first name of a student entered by the user.
student_last_name: str = ''  # Holds the last name of a student entered by the user.
course_name: str = ''  # Holds the name of a course entered by the user.
json_data: str = ''  # Holds combined string data separated by a comma.
file: IO  # Holds a reference to an opened file.
menu_choice: str = ''  # Hold the choice made by the user.
student_data: dict = {}  # Dictionary of data for a single student
students: list = []  # List of data for all students
saved: bool = True # Tracks whether newly added data has been saved

# Load existing data from enrollment JSON file into a list of dictionaries

print(f">>> Loading data from {FILE_NAME}")
try:
    file = open(FILE_NAME, "r")
    students = json.load(file)
    file.close()
    print(f">>> Loaded {len(students)} records.")

    for index, item in enumerate(students):
        # Check to see if the keys we are expecting exist in the data
        if not all(key in item for key in KEYS):
            raise Exception(f">>> Missing expected key at index {index}. Please check {FILE_NAME} for errors try again.")

# Let the user know we couldn't find the file
except FileNotFoundError:
    print(f">>> {FILE_NAME} not found. A new file will be created.")

# Let the user know some other problem occurred when loading the file
except Exception as e:
    print(e)
    exit()

# If the file is still open for some reason, close it
finally:
    if not file.closed:
        print(">>> Closing file.")
        file.close()


# Present and Process the data

while True:
    # Present the menu of choices
    print(MENU)
    menu_choice = input("Enter your choice: ")

    if menu_choice == '1':
        # Input user data, allow only alpha characters
        while True:
            try:
                student_first_name = input("Enter student's first name: ")
                if not student_first_name.isalpha():
                    raise ValueError(f">>> Please use only letters. Try again.\n")
                else:
                    break
            except ValueError as e:
                print(e)

        while True:
            try:
                student_last_name = input("Enter student's last name: ")
                if not student_last_name.isalpha():
                    raise ValueError(">>> Please use only letters. Try again.\n")
                else:
                    break
            except ValueError as e:
                print(e)

        course_name = input("Enter the course name: ")

        # Create dictionary using captured data
        student_data = {"FirstName":student_first_name,"LastName":student_last_name,"CourseName":course_name}

        # Append student data to students list
        students.append(student_data)
        print(f">>> Registered {student_first_name} {student_last_name} for {course_name}.\n")
        saved = False  # Set the saved flag to false, so we can remind user to save
        continue

    elif menu_choice == '2':
        # Display the data in a human-friendly format
        print(">>> The current data is:\n")
        print("First Name          Last Name           Course Name         ")
        print("------------------------------------------------------------")
        for item in students:
            print(f"{item['FirstName'][:20]:<20}{item['LastName'][:20]:<20}{item['CourseName'][:20]:<20}")
        print("------------------------------------------------------------")
        continue

    elif menu_choice == '3':
        # Save the data to a file
        try:
            file = open(FILE_NAME, 'w')
            json.dump(students, file, indent=4)
            file.close()
            saved = True
            print(f">>> Wrote registration data to filename {FILE_NAME}\n")

            # Print JSON data to terminal
            json_data = json.dumps(students, indent=4)
            print(json_data)

        except Exception as e:
            print(">>> There was an error writing the registration data.")
            print(f">>> {e}", e.__doc__)
        finally:
            file.close()

        continue

    elif menu_choice == '4':
        # Exit if data has already been saved or was unmodified (i.e. saved = undefined)
        if (saved is False):
            exit_confirm = input(">>> File not saved. Are you sure you want to exit? (Y/N): ")
            if exit_confirm.capitalize() == 'Y':
                print(">>> Have a nice day!\n")
                break
            else:
                continue
        else:
            print(">>> Have a nice day!\n")
            break

    else:
        print("Please only choose option 1, 2, 3, or 4.")
