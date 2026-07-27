


operations_maneu = """
1 Add Student
2 Show Students
3 Find Student
4 Delete Student
5 Update Grade
6 Show Average Grade
7 Exit
"""

## no repeats
## grade between 0 20

students = {}
choice = 0


while True:
    print(operations_maneu)
    choice = int(input('enter your choice: '))

    if choice == 1:
        student_name = input("enter student's name: ")
        if student_name in students:
            print('student is already in the list')
        else:
            student_grade = int(input("enter student's grade: "))
            while student_grade <0 or student_grade > 20:
                print('grade must be between 0 and 20\n')
                student_grade = int(input("enter student's grade: "))
            students[student_name] = student_grade

    elif choice == 2:
        for key, value in students.items():
            print(key,value)

    elif choice == 3:
        name_search = input("enter the student's name: ")
        if name_search in students.keys():
            print(f'{name_search} {students.get(name_search)}')
        else:
            print('\ngiven student is not in the list')

    elif choice == 4:
        name_search = input("enter the student's name: ")
        if name_search in students.keys():
            del students[name_search]
            print(f'student {name_search} deleted! ')
        else:
            print("\n given student is not in the list")

    elif choice == 5:
        name_search = input("enter the student's name: ")
        if name_search in students.keys():
            grade_update = int(input("enter the grade: "))
            students[name_search] = grade_update
        else:
            print('student is not in the list')

    elif choice == 6:
        if len(students) == 0:
            print('there are no students in the list')
            break
        else:
            grades_sum = 0
            for value in students.values():
                grades_sum += value
            avg_grades = grades_sum / len(students)
            print(f'average grades of the students: {avg_grades}')

    elif choice == 7:
        break
    else:
        print('enter a valid choice')


