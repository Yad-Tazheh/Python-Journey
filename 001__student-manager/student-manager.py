


# must have add,show,find,exit operatins on objects called students 

operations_menu = """
1. add students
2. show students
3. find student 
4. exit program
"""

# parallel lists 
students = []
grades = []
choice = 0


while True:
    print(operations_menu)
    choice = int(input("enter your choice: "))

    if choice == 1:
        #        students.append(input("enter the student name: ")) 
#        grades.append(input("enter the student's grade: "))
        student_name = input('enter the student name: ')
        if student_name in students:
            print('entered student exists in the list!')
            continue
        else:
            students.append(student_name)
            grades.append(int(input("enter the student's grade: ")))
    elif choice == 2:
        #        for i in range(0,len(students)):
        #            print(f'name: {students[i]}')
        #            print(f'grade: {grades[i]}\n')
        #
        for student in students:
            print(f'name: {student}')
            print(f'grade: {grades[students.index(student)]}\n')

#        for index, student in enumerate(students,start=1):
#            print(index,student,f'\ngrade: {grades[students.index(student)]}')
    elif choice == 3:
        search_student = input('enter the student name: ')
        if search_student in students:
            print(f'\nname: {search_student}\ngrade: {grades[students.index(search_student)]}')
        else:
            print('given student is not in the list')
    elif choice == 4:
        break
    else:
        print('enter a valid option')








    



