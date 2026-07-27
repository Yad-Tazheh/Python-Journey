


operations_maneu = """
1 Add Student
2 Show Students
3 Find Student
4 Delete Student
5 Update Grade
6 Show Average Grade
7 Exit
"""

students = {}


def add_student(name,grade):
    students[name] = grade

def show_students():
    for key, value in students.items():
        print(key,value)
 
def find_student(name):
    if name in students:
        print(f'{name} {students.get(name)}')
    else:
        print(f'[-] student {name} is not in the list')

def del_student(name):
    if name in students.keys():
        del students[name]
        print(f'[-] student {name} deleted!')
    else:
        print(f'[-] student {name} does not exists!')

   
def update_grade(name,grade):
    if name in students:
        students[name] = grade
        
def avg_grade(students):
    if len(students) == 0:
        return 0
    else:
        avg_sum = 0
        for value in students:
           avg_sum += value 
        avg = avg_sum / len(students)
        return avg

def main():
    while True:
        print(operations_maneu)
        choice = int(input('enter your choice: '))

        if choice == 1:
            name = input('enter the students name: ')
            if name in students:
                print(f'[-] student {name} is already in the list')
            else:
                grade = int(input('enter the grade: '))
                while grade < 0 or grade > 20:
                    print('[-] enter a valid grade (0-20) ')
                    grade = int(input('enter the student grade: '))
                add_student(name,grade)


                



