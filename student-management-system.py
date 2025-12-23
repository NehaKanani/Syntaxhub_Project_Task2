import csv
import os

FILE_NAME = "students.csv"


class Student:
    def __init__(self, student_id, name, grade):
        self.student_id = student_id
        self.name = name
        self.grade = grade

    def to_list(self):
        return [self.student_id, self.name, self.grade]


class StudentManager:
    def __init__(self, file_name):
        self.file_name = file_name
        self.students = {}
        self.load_students()

    def load_students(self):
        if not os.path.exists(self.file_name):
            return

        with open(self.file_name, "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                student = Student(row[0], row[1], row[2])
                self.students[student.student_id] = student

    def save_students(self):
        with open(self.file_name, "w", newline="") as file:
            writer = csv.writer(file)
            for student in self.students.values():
                writer.writerow(student.to_list())

    def add_student(self, student_id, name, grade):
        if student_id in self.students:
            print("Error: Student ID already exists.")
            return
        self.students[student_id] = Student(student_id, name, grade)
        self.save_students()
        print("Student added successfully.")

    def update_student(self, student_id, name, grade):
        if student_id not in self.students:
            print("Error: Student not found.")
            return
        self.students[student_id].name = name
        self.students[student_id].grade = grade
        self.save_students()
        print("Student updated successfully.")

    def delete_student(self, student_id):
        if student_id not in self.students:
            print("Error: Student not found.")
            return
        del self.students[student_id]
        self.save_students()
        print("Student deleted successfully.")

    def list_students(self):
        if not self.students:
            print("No student records available.")
            return

        print("\n{:<10} {:<20} {:<10}".format("ID", "Name", "Grade"))
        print("-" * 40)
        for s in self.students.values():
            print("{:<10} {:<20} {:<10}".format(s.student_id, s.name, s.grade))


def main():
    manager = StudentManager(FILE_NAME)

    while True:
        print("\nStudent Management System")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. List Students")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            sid = input("Enter ID: ")
            name = input("Enter Name: ")
            grade = input("Enter Grade: ")
            manager.add_student(sid, name, grade)

        elif choice == "2":
            sid = input("Enter ID to update: ")
            name = input("Enter New Name: ")
            grade = input("Enter New Grade: ")
            manager.update_student(sid, name, grade)

        elif choice == "3":
            sid = input("Enter ID to delete: ")
            manager.delete_student(sid)

        elif choice == "4":
            manager.list_students()

        elif choice == "5":
            print("Exiting application.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
