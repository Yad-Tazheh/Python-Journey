user exists
project ( set of {task} )
be yek proje bayad beshe user ezafe kard va task va task haro be user ha assign kard

class User:
 attrib:
    - name
    - user_id
    - email
    - tasks
    - role

Ali | admin
Reza | member

class Task:
attrib:
    - title
    - description
    - task_id
    - status
            IN_PROGRESS
            DONE
            CANCELED
    - priority
            LOW
            MEDIUM
            HIGH
    - assigned_user
    - created_at
    - due_date

class Project
    attrib:
        - name
        - project_id
        - members
        - taskS


Website Project
Tasks:
    Create database
    Design login page
    Deploy server
