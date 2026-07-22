"""
Student Grade Management System
--------------------------------
CloudExify Python Internship - Month 1 Project 2

A command line application to manage student records: add students,
record subject-wise grades, view a formatted table, generate a class
report with rankings, search/edit/delete records, and save/load data
using CSV files.

Author: (Basit Ali)
"""

import csv
import os

# CONFIGURATION

DATA_FILE = "students.csv"
PASS_MARK = 50          # Minimum average required to pass
DEFAULT_SUBJECTS = ["Math", "Physics", "English", "Computer", "Urdu"]

ATTENDANCE_WARNING = 75   # Bonus: below this % attendance, flag the student

# Global state
students = []           # list of dicts -> {"id": int, "name": str, "grades": {subject: grade}, "attendance": float}
subjects = DEFAULT_SUBJECTS.copy()   # bonus: subjects can be customized by the user
next_id = 1

# HELPER FUNCTIONS

def generate_id():
    """Return a fresh unique id and bump the counter."""
    global next_id
    new_id = next_id
    next_id += 1
    return new_id


def calculate_average(grades):
    """Average of a grades dict. Returns 0 if there are no grades."""
    if not grades:
        return 0.0
    return sum(grades.values()) / len(grades)


def grade_to_letter(mark):
    """Bonus: convert a numeric mark into a letter grade."""
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    elif mark >= PASS_MARK:
        return "E"
    else:
        return "F"


def find_student_by_name(name):
    """Case-insensitive search, returns the student dict or None."""
    for student in students:
        if student["name"].lower() == name.lower():
            return student
    return None


def find_student_by_id(student_id):
    for student in students:
        if student["id"] == student_id:
            return student
    return None


def ranked_students():
    """Return students sorted by average grade, highest first."""
    return sorted(students, key=lambda s: calculate_average(s["grades"]), reverse=True)


def get_valid_grade(prompt):
    """Keep asking until the user gives a number between 0 and 100."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            print("  -> Please enter a valid number.")
            continue
        if 0 <= value <= 100:
            return value
        print("  -> Grade must be between 0 and 100.")

# CORE FEATURES

def add_student():
    print("\n--- ADD NEW STUDENT ---")
    name = input("Student Name: ").strip()

    if not name:
        print("Name cannot be empty!")
        return

    if find_student_by_name(name):
        print(f"Student '{name}' already exists!")
        return

    grades = {}
    print(f"Enter grades for {name}:")
    for subject in subjects:
        grades[subject] = get_valid_grade(f"  {subject}: ")

    attendance = get_valid_grade("  Attendance % (0-100): ")

    student = {"id": generate_id(), "name": name, "grades": grades, "attendance": attendance}
    students.append(student)

    avg = calculate_average(grades)
    status = "PASS" if avg >= PASS_MARK else "FAIL"
    print(f"\nAdded {name} | Average: {avg:.1f} ({grade_to_letter(avg)}) | {status} | Attendance: {attendance:.1f}%")


def view_all_students():
    if not students:
        print("\nNo students yet!")
        return

    print("\n--- ALL STUDENTS ---")
    header = f"{'ID':<5}{'Name':<20}"
    for subject in subjects:
        header += f"{subject[:6]:<8}"
    header += f"{'Avg':<8}{'Grade':<7}{'Status':<8}{'Attend'}"
    print(header)
    print("-" * len(header))

    for student in students:
        avg = calculate_average(student["grades"])
        status = "PASS" if avg >= PASS_MARK else "FAIL"
        attendance = student.get("attendance", 0)
        row = f"{student['id']:<5}{student['name']:<20}"
        for subject in subjects:
            mark = student["grades"].get(subject, 0)
            row += f"{mark:<8.1f}"
        row += f"{avg:<8.1f}{grade_to_letter(avg):<7}{status:<8}{attendance:.1f}%"
        if attendance < ATTENDANCE_WARNING:
            row += "  (Low!)"
        print(row)


def class_report():
    if not students:
        print("\nNo students to report!")
        return

    averages = [calculate_average(s["grades"]) for s in students]
    class_avg = sum(averages) / len(averages)
    passed = sum(1 for avg in averages if avg >= PASS_MARK)
    failed = len(students) - passed

    print("\n=== CLASS REPORT ===")
    print(f"Total Students  : {len(students)}")
    print(f"Class Average   : {class_avg:.2f}")
    print(f"Highest Average : {max(averages):.2f}")
    print(f"Lowest Average  : {min(averages):.2f}")
    print(f"Passed          : {passed}")
    print(f"Failed          : {failed}")

    # Bonus: attendance overview
    attendances = [s.get("attendance", 0) for s in students]
    low_attendance = [s["name"] for s in students if s.get("attendance", 0) < ATTENDANCE_WARNING]
    print(f"Avg Attendance  : {sum(attendances) / len(attendances):.1f}%")
    if low_attendance:
        print(f"Low Attendance  : {', '.join(low_attendance)} (below {ATTENDANCE_WARNING}%)")

    # Bonus: subject-wise class average
    print("\n--- SUBJECT-WISE CLASS AVERAGE ---")
    for subject in subjects:
        subject_marks = [s["grades"].get(subject, 0) for s in students]
        print(f"  {subject:<12}: {sum(subject_marks) / len(subject_marks):.2f}")

    print("\n--- RANKINGS ---")
    medals = {1: "1st", 2: "2nd", 3: "3rd"}
    for rank, student in enumerate(ranked_students(), start=1):
        avg = calculate_average(student["grades"])
        tag = medals.get(rank, f"{rank}th")
        print(f"  {tag:<5} {student['name']:<20} {avg:.2f} ({grade_to_letter(avg)})")


def generate_report_card():
    """Dedicated feature: generate a report card by Student ID or Name."""
    if not students:
        print("\nNo students yet!")
        return

    print("\n--- GENERATE REPORT CARD ---")
    identifier = input("Enter Student ID or Name: ").strip()

    student = None
    if identifier.isdigit():
        student = find_student_by_id(int(identifier))
    if not student:
        student = find_student_by_name(identifier)

    if not student:
        print(f"No student found matching '{identifier}'.")
        return

    show_report_card(student)


def search_student():
    if not students:
        print("\nNo students yet!")
        return

    print("\n--- SEARCH STUDENT ---")
    name = input("Enter name to search: ").strip()
    student = find_student_by_name(name)

    if not student:
        print(f"No student found with the name '{name}'.")
        return

    show_report_card(student)


def show_report_card(student):
    """Bonus: display a detailed report card for one student, with rank."""
    avg = calculate_average(student["grades"])
    rank_list = ranked_students()
    position = next(i for i, s in enumerate(rank_list, start=1) if s["id"] == student["id"])

    attendance = student.get("attendance", 0)
    print(f"\n--- REPORT CARD: {student['name']} (ID {student['id']}) ---")
    for subject, mark in student["grades"].items():
        print(f"  {subject:<12}: {mark:.1f}  ({grade_to_letter(mark)})")
    print(f"  {'Average':<12}: {avg:.2f}  ({grade_to_letter(avg)})")
    print(f"  Status : {'PASS' if avg >= PASS_MARK else 'FAIL'}")
    print(f"  Class Rank : {position} out of {len(students)}")
    print(f"  Attendance : {attendance:.1f}%" + ("  -- Warning: below required attendance!" if attendance < ATTENDANCE_WARNING else ""))


def edit_grades():
    if not students:
        print("\nNo students yet!")
        return

    print("\n--- EDIT GRADES ---")
    view_all_students()

    try:
        student_id = int(input("\nEnter Student ID to edit: ").strip())
    except ValueError:
        print("Please enter a valid numeric ID.")
        return

    student = find_student_by_id(student_id)
    if not student:
        print(f"No student found with ID {student_id}.")
        return

    print(f"\nCurrent grades for {student['name']}:")
    for subject, mark in student["grades"].items():
        print(f"  {subject}: {mark}")
    print(f"  Attendance: {student.get('attendance', 0):.1f}%")

    field = input("Which subject (or 'attendance') do you want to update? ").strip()

    if field.lower() == "attendance":
        new_value = get_valid_grade("New attendance % (0-100): ")
        student["attendance"] = new_value
        print(f"Updated attendance for {student['name']} to {new_value:.1f}%.")
        return

    match = next((s for s in subjects if s.lower() == field.lower()), None)
    if not match:
        print(f"'{field}' is not a tracked subject.")
        return

    new_grade = get_valid_grade(f"New grade for {match}: ")
    student["grades"][match] = new_grade
    print(f"Updated {match} for {student['name']} to {new_grade:.1f}.")


def delete_student():
    if not students:
        print("\nNo students yet!")
        return

    print("\n--- DELETE STUDENT ---")
    try:
        student_id = int(input("Enter Student ID to delete: ").strip())
    except ValueError:
        print("Please enter a valid numeric ID.")
        return

    student = find_student_by_id(student_id)
    if not student:
        print(f"No student found with ID {student_id}.")
        return

    confirm = input(f"Are you sure you want to delete {student['name']}? (y/n): ").strip().lower()
    if confirm == "y":
        students.remove(student)
        print(f"{student['name']} removed from records.")
    else:
        print("Deletion cancelled.")

# BONUS FEATURES

def manage_subjects():
    """Bonus: allow custom subjects instead of a fixed list."""
    print("\n--- MANAGE SUBJECTS ---")
    print(f"Current subjects: {', '.join(subjects)}")
    print("1. Add a subject")
    print("2. Remove a subject")
    print("3. Back")
    choice = input("Choice: ").strip()

    if choice == "1":
        new_subject = input("New subject name: ").strip()
        if not new_subject:
            print("Subject name cannot be empty.")
        elif new_subject in subjects:
            print("Subject already exists.")
        else:
            subjects.append(new_subject)
            # Existing students get a default 0 for the new subject
            for student in students:
                student["grades"][new_subject] = 0.0
            print(f"'{new_subject}' added. Existing students set to 0 for it (edit to update).")
    elif choice == "2":
        remove_subject = input("Subject to remove: ").strip()
        match = next((s for s in subjects if s.lower() == remove_subject.lower()), None)
        if not match:
            print("Subject not found.")
        elif len(subjects) == 1:
            print("Cannot remove the last remaining subject.")
        else:
            subjects.remove(match)
            for student in students:
                student["grades"].pop(match, None)
            print(f"'{match}' removed.")
    else:
        return


def export_report_txt():
    """Bonus: export the class report as a plain text file."""
    if not students:
        print("\nNo students to export!")
        return

    filename = "class_report.txt"
    averages = [calculate_average(s["grades"]) for s in students]
    class_avg = sum(averages) / len(averages)

    with open(filename, "w") as f:
        f.write("=== CLASS REPORT ===\n")
        f.write(f"Total Students  : {len(students)}\n")
        f.write(f"Class Average   : {class_avg:.2f}\n")
        f.write(f"Highest Average : {max(averages):.2f}\n")
        f.write(f"Lowest Average  : {min(averages):.2f}\n")
        attendances = [s.get("attendance", 0) for s in students]
        f.write(f"Avg Attendance  : {sum(attendances) / len(attendances):.1f}%\n\n")
        f.write("--- RANKINGS ---\n")
        for rank, student in enumerate(ranked_students(), start=1):
            avg = calculate_average(student["grades"])
            f.write(f"{rank}. {student['name']:<20} {avg:.2f} ({grade_to_letter(avg)})\n")

    print(f"Report exported to {filename}")

# CSV SAVE / LOAD

def save_to_csv():
    with open(DATA_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name"] + subjects + ["Attendance"])
        for student in students:
            row = [student["id"], student["name"]]
            row += [student["grades"].get(subject, 0) for subject in subjects]
            row.append(student.get("attendance", 0))
            writer.writerow(row)
    print(f"Saved {len(students)} students to {DATA_FILE}")


def load_from_csv():
    global next_id, subjects

    if not os.path.exists(DATA_FILE):
        return

    with open(DATA_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        # Everything except ID, Name and Attendance is treated as a subject column
        loaded_subjects = [col for col in reader.fieldnames if col not in ("ID", "Name", "Attendance")]
        if loaded_subjects:
            subjects = loaded_subjects

        for row in reader:
            grades = {subject: float(row[subject]) for subject in subjects}
            attendance = float(row["Attendance"]) if "Attendance" in row and row["Attendance"] != "" else 0.0
            student = {"id": int(row["ID"]), "name": row["Name"], "grades": grades, "attendance": attendance}
            students.append(student)
            next_id = max(next_id, student["id"] + 1)

    if students:
        print(f"Loaded {len(students)} students from {DATA_FILE}")

# MAIN MENU

MENU = """
========================================
   STUDENT GRADE MANAGEMENT SYSTEM
========================================
1. Add Student
2. View All Students
3. Class Report (with rankings)
4. Search Student
5. Generate Individual Report Card
6. Edit Grades
7. Delete Student
8. Manage Subjects
9. Export Report as Text File
10. Save to CSV
0. Exit
"""


def main():
    load_from_csv()

    actions = {
        "1": add_student,
        "2": view_all_students,
        "3": class_report,
        "4": search_student,
        "5": generate_report_card,
        "6": edit_grades,
        "7": delete_student,
        "8": manage_subjects,
        "9": export_report_txt,
        "10": save_to_csv,
    }

    while True:
        print(MENU)
        choice = input("Enter your choice: ").strip()

        if choice == "0":
            save_to_csv()
            print("Goodbye!")
            break

        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
