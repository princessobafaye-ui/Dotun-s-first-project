import json
import os
from datetime import datetime

# DATA STORAGE LOCATION
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_FOLDER, "students.json")


# ==========================================
# 1. STUDENT CLASS
# ==========================================

class Student:

    def __init__(self, student_id, full_name, class_form, gender, date_of_birth):

        self.student_id = student_id
        self.full_name = full_name
        self.class_form = class_form
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.scores = {}

        self.date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.result_date = "Not entered"

    def to_dictionary(self):

        return {
            "student_id": self.student_id,
            "full_name": self.full_name,
            "class_form": self.class_form,
            "gender": self.gender,
            "date_of_birth": self.date_of_birth,
            "scores": self.scores,
            "date_created": self.date_created,
            "result_date": self.result_date
        }

    @classmethod
    def from_dictionary(cls, data):

        student = cls(
            data["student_id"],
            data["full_name"],
            data["class_form"],
            data["gender"],
            data["date_of_birth"]
        )

        student.scores = data.get("scores", {})
        student.date_created = data.get("date_created", "")
        student.result_date = data.get("result_date", "Not entered")

        return student


# ==========================================
# 2. DATA STORAGE
# ==========================================

def save_students(students):

    os.makedirs(DATA_FOLDER, exist_ok=True)

    data = [student.to_dictionary() for student in students]

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print("\nData saved successfully.")

    except OSError as error:
        print(f"Could not save data: {error}")


def load_students():

    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return [Student.from_dictionary(item) for item in data]

    except (json.JSONDecodeError, OSError, KeyError, TypeError) as error:

        print(f"Could not load saved data: {error}")
        return []


# ==========================================
# 3. RESULT CALCULATIONS AND GRADING
# ==========================================

def calculate_total(scores):

    return sum(scores.values())


def calculate_average(scores):

    if not scores:
        return 0

    return calculate_total(scores) / len(scores)


def calculate_grade(average):

    if average >= 70:
        return "A"

    elif average >= 60:
        return "B"

    elif average >= 50:
        return "C"

    elif average >= 45:
        return "D"

    else:
        return "F"


# ==========================================
# 4. HELPER FUNCTIONS
# ==========================================

def find_student(students, student_id):

    for student in students:

        if student.student_id.lower() == student_id.lower():
            return student

    return None


def get_non_empty_input(prompt):

    while True:

        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty.")


def get_valid_score(prompt="Enter score (0-100): "):

    while True:

        try:

            score = float(input(prompt))

            if 0 <= score <= 100:
                return score

            print("Score must be between 0 and 100.")

        except ValueError:
            print("Please enter a valid number.")


def get_positive_integer(prompt, minimum=1):

    while True:

        try:

            number = int(input(prompt))

            if number >= minimum:
                return number

            print(f"Please enter a number of at least {minimum}.")

        except ValueError:
            print("Please enter a whole number.")


# ==========================================
# 5. ADD NEW STUDENT
# ==========================================

def add_student(students):

    print("\n========== ADD NEW STUDENT ==========")

    student_id = get_non_empty_input("Enter Student ID: ")

    if find_student(students, student_id):

        print("A student with this ID already exists.")
        return

    full_name = get_non_empty_input("Enter Full Name: ")
    class_form = get_non_empty_input("Enter Class/Form: ")
    gender = get_non_empty_input("Enter Gender: ")
    date_of_birth = get_non_empty_input("Enter Date of Birth: ")

    student = Student(
        student_id,
        full_name,
        class_form,
        gender,
        date_of_birth
    )

    students.append(student)

    print("\nStudent registered successfully.")

    save_students(students)


# ==========================================
# 6. VIEW ALL STUDENTS
# ==========================================

def view_all_students(students):

    if not students:

        print("\nNo students have been registered.")
        return

    print("\n================ ALL STUDENTS ================")

    for student in students:

        if student.scores:

            total = calculate_total(student.scores)
            average = calculate_average(student.scores)
            grade = calculate_grade(average)

            result = f"Total: {total:g} | Average: {average:.2f} | Grade: {grade}"

        else:

            result = "Results not entered"

        print(
            f"ID: {student.student_id} | "
            f"Name: {student.full_name} | "
            f"Class: {student.class_form} | "
            f"{result}"
        )


# ==========================================
# 7. SEARCH STUDENT
# ==========================================

def search_student(students):

    search_text = get_non_empty_input(
        "Enter Student ID or Name: "
    ).lower()

    matches = [

        student for student in students

        if search_text in student.student_id.lower()
        or search_text in student.full_name.lower()

    ]

    if not matches:

        print("\nStudent not found.")
        return

    for student in matches:

        print("\n--------------------------------")

        print(f"Student ID: {student.student_id}")
        print(f"Full Name: {student.full_name}")
        print(f"Class/Form: {student.class_form}")
        print(f"Gender: {student.gender}")
        print(f"Date of Birth: {student.date_of_birth}")

        print("--------------------------------")


# ==========================================
# 8. UPDATE STUDENT INFORMATION
# ==========================================

def update_student(students):

    student_id = get_non_empty_input("Enter Student ID: ")

    student = find_student(students, student_id)

    if student is None:

        print("Student not found.")
        return

    print("\nPress Enter to keep existing information.")

    new_name = input(
        f"Full Name [{student.full_name}]: "
    ).strip()

    new_class = input(
        f"Class/Form [{student.class_form}]: "
    ).strip()

    new_gender = input(
        f"Gender [{student.gender}]: "
    ).strip()

    new_dob = input(
        f"Date of Birth [{student.date_of_birth}]: "
    ).strip()

    if new_name:
        student.full_name = new_name

    if new_class:
        student.class_form = new_class

    if new_gender:
        student.gender = new_gender

    if new_dob:
        student.date_of_birth = new_dob

    print("\nStudent information updated.")

    save_students(students)


# ==========================================
# 9. DELETE STUDENT
# ==========================================

def delete_student(students):

    student_id = get_non_empty_input("Enter Student ID: ")

    student = find_student(students, student_id)

    if student is None:

        print("Student not found.")
        return

    confirm = input(
        f"Delete {student.full_name}? (Y/N): "
    ).strip().upper()

    if confirm == "Y":

        students.remove(student)

        print("Student record deleted.")

        save_students(students)

    else:

        print("Deletion cancelled.")


# ==========================================
# 10. ENTER STUDENT SCORES
# ==========================================

def enter_scores(students):

    student_id = get_non_empty_input("Enter Student ID: ")

    student = find_student(students, student_id)

    if student is None:

        print("Student not found.")
        return

    print(f"\nEntering scores for {student.full_name}")

    if not student.scores:

        number_of_subjects = get_positive_integer(
            "How many subjects? Enter at least 5: ",
            minimum=5
        )

    else:

        number_of_subjects = get_positive_integer(
            "How many additional subjects do you want to enter? ",
            minimum=1
        )

    for i in range(number_of_subjects):

        print(f"\nSubject {i + 1}")

        while True:

            subject = get_non_empty_input("Enter subject name: ")

            if subject in student.scores:

                print("This subject already exists. Enter another subject.")

            else:
                break

        score = get_valid_score()

        student.scores[subject] = score

    student.result_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\nScores recorded successfully.")

    save_students(students)


# ==========================================
# 11. UPDATE EXISTING SCORES
# ==========================================

def update_scores(students):

    student_id = get_non_empty_input("Enter Student ID: ")

    student = find_student(students, student_id)

    if student is None:

        print("Student not found.")
        return

    if not student.scores:

        print("No scores have been entered.")
        return

    subjects = list(student.scores.keys())

    print(f"\nScores for {student.full_name}:")

    for i, subject in enumerate(subjects, start=1):

        print(f"{i}. {subject}: {student.scores[subject]:g}")

    selection = get_positive_integer(
        "Choose the subject number to update: ",
        minimum=1
    )

    if selection > len(subjects):

        print("Invalid subject number.")
        return

    selected_subject = subjects[selection - 1]

    new_score = get_valid_score("Enter new score (0-100): ")

    student.scores[selected_subject] = new_score

    student.result_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("Score updated successfully.")

    save_students(students)


# ==========================================
# 12. DISPLAY STUDENT REPORT CARD
# ==========================================

def display_report_card(student):

    print("\n================ STUDENT REPORT CARD ================")

    print(f"Student ID: {student.student_id}")
    print(f"Full Name: {student.full_name}")
    print(f"Class/Form: {student.class_form}")
    print(f"Gender: {student.gender}")
    print(f"Date of Birth: {student.date_of_birth}")
    print(f"Result Date: {student.result_date}")

    print("-----------------------------------------------------")

    if not student.scores:

        print("No subject scores have been entered.")
        return

    print(f"{'SUBJECT':<28}{'SCORE':>10}{'GRADE':>10}")

    print("-" * 48)

    for subject, score in student.scores.items():

        grade = calculate_grade(score)

        print(f"{subject:<28}{score:>10.2f}{grade:>10}")

    total = calculate_total(student.scores)

    average = calculate_average(student.scores)

    overall_grade = calculate_grade(average)

    print("-" * 48)

    print(f"Total Score: {total:g}")
    print(f"Average: {average:.2f}")
    print(f"Overall Grade: {overall_grade}")

    print("======================================================")


def view_report_card(students):

    student_id = get_non_empty_input("Enter Student ID: ")

    student = find_student(students, student_id)

    if student is None:

        print("Student not found.")

    else:

        display_report_card(student)


# ==========================================
# 13. CLASS STATISTICS
# ==========================================

def display_class_statistics(students):

    all_scores = [

        score

        for student in students

        for score in student.scores.values()

    ]

    if not all_scores:

        print("No scores are available for statistics.")
        return

    class_average = sum(all_scores) / len(all_scores)

    students_with_results = len(
        [student for student in students if student.scores]
    )

    print("\n================ CLASS STATISTICS ================")

    print(f"Number of students with results: {students_with_results}")

    print(f"Highest Subject Score: {max(all_scores):.2f}")

    print(f"Lowest Subject Score: {min(all_scores):.2f}")

    print(f"Class Average: {class_average:.2f}")

    print("===================================================")


# ==========================================
# 14. SORT STUDENTS
# ==========================================

def sort_students(students):

    if not students:

        print("No students available.")
        return

    print("\n1. Sort by Average (Highest to Lowest)")
    print("2. Sort by Student Name (A-Z)")

    choice = input("Enter your choice: ").strip()

    if choice == "1":

        ordered_students = sorted(

            students,

            key=lambda student: calculate_average(student.scores),

            reverse=True

        )

        print("\nStudents Sorted by Average:")

        for student in ordered_students:

            if student.scores:

                average = calculate_average(student.scores)

                grade = calculate_grade(average)

                print(
                    f"{student.full_name} - "
                    f"Average: {average:.2f} - Grade: {grade}"
                )

            else:

                print(f"{student.full_name} - Results not entered")

    elif choice == "2":

        ordered_students = sorted(

            students,

            key=lambda student: student.full_name.lower()

        )

        print("\nStudents Sorted by Name:")

        for student in ordered_students:

            print(student.full_name)

    else:

        print("Invalid choice.")


# ==========================================
# 15. GENERATE TEXT REPORT
# ==========================================

def generate_text_report(students):

    filename = os.path.join(BASE_DIR, "student_report.txt")

    try:

        with open(filename, "w", encoding="utf-8") as file:

            file.write("STUDENT RESULT MANAGEMENT SYSTEM\n")

            file.write("=" * 55 + "\n\n")

            if not students:

                file.write("No students registered.\n")

            for student in students:

                file.write(f"Student ID: {student.student_id}\n")

                file.write(f"Full Name: {student.full_name}\n")

                file.write(f"Class/Form: {student.class_form}\n")

                file.write(f"Gender: {student.gender}\n")

                file.write(f"Date of Birth: {student.date_of_birth}\n")

                file.write(f"Result Date: {student.result_date}\n")

                file.write("\nSubject Results:\n")

                for subject, score in student.scores.items():

                    file.write(
                        f"{subject}: {score:g} "
                        f"({calculate_grade(score)})\n"
                    )

                if student.scores:

                    total = calculate_total(student.scores)

                    average = calculate_average(student.scores)

                    grade = calculate_grade(average)

                    file.write(f"Total: {total:g}\n")

                    file.write(f"Average: {average:.2f}\n")

                    file.write(f"Overall Grade: {grade}\n")

                else:

                    file.write("Results not entered.\n")

                file.write("-" * 55 + "\n")

        print(f"\nReport successfully saved as {filename}")

    except OSError as error:

        print(f"Could not generate report: {error}")


# ==========================================
# 16. MAIN PROGRAM / MENU
# ==========================================

def main():

    students = load_students()

    print("\n================================================")

    print("       STUDENT RESULT MANAGEMENT SYSTEM")

    print("================================================")

    print(f"Loaded {len(students)} student record(s).")

    while True:

        print("\n--------------- MAIN MENU ---------------")

        print("1. Add New Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student Information")
        print("5. Delete Student")
        print("6. Enter Scores")
        print("7. Update Scores")
        print("8. View Student Report Card")
        print("9. View Class Statistics")
        print("10. Sort Students")
        print("11. Generate Text Report")
        print("12. Save Data")
        print("0. Save and Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":

            add_student(students)

        elif choice == "2":

            view_all_students(students)

        elif choice == "3":

            search_student(students)

        elif choice == "4":

            update_student(students)

        elif choice == "5":

            delete_student(students)

        elif choice == "6":

            enter_scores(students)

        elif choice == "7":

            update_scores(students)

        elif choice == "8":

            view_report_card(students)

        elif choice == "9":

            display_class_statistics(students)

        elif choice == "10":

            sort_students(students)

        elif choice == "11":

            generate_text_report(students)

        elif choice == "12":

            save_students(students)

        elif choice == "0":

            save_students(students)

            print("\nThank you for using the Student Result Management System.")

            break

        else:

            print("\nInvalid choice. Please try again.")


# RUN THE PROGRAM

if __name__ == "__main__":

    main()