

operations_menu = """
1 Add Student
2 Show Students
3 Find Student
4 Delete Student
5 Update Grade
6 Show Average Grade
7 Exit
"""


class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def __str__(self):
        return f"Name: {self.name} | Grade: {self.grade}"

class StudentManager:
    def __init__(self):
        self.students = []

    def add_student(self, name, grade):
        for student in self.students:
            if student.name == name:
                print("Student already exists.")
                return

        self.students.append(Student(name, grade))

    def show_students(self):
        if not self.students:
            print("No students.")
            return

        for student in self.students:
            print(student)

    def find_student(self, name):
        for student in self.students:
            if student.name == name:
                return student

        return None

    def delete_student(self, name):
        student = self.find_student(name)
        if student:
            self.students.remove(student)
            print("Student deleted.")
        else:
            print("Student not found.")

    def update_grade(self, name, grade):
        student = self.find_student(name)
        if student:
            student.grade = grade
        else:
            print("Student not found.")

    def average_grade(self):
        if not self.students:
            return 0
        total = 0
        for student in self.students:
            total += int(student.grade)
        return total / len(self.students)
def main():
    manager = StudentManager()
    while True:
        print(operations_menu)
        choice = int(input('enter your choice: '))
        if choice == 1:
            name = input('enter the student name: ')
            grade = int(input('enter the student grade: '))
            while grade < 0 or grade > 20:
                grade = int(input(('enter a valid grade: ')))
            manager.add_student(name,grade)

        if choice == 2:
            manager.show_students()
        if choice == 3:
            name = input('enter student name: ')
            print(manager.find_student(name))
        if choice == 4:
            name = input('enter the student name: ')
            manager.delete_student(name)

        if choice == 5:
            name = input('enter student name: ')
            grade = input('enter the student grade: ')
            manager.update_grade(name, grade)
        if choice == 6:
            print(manager.average_grade())
        
        if choice == 7:
            break




if __name__ == '__main__':
    main()

