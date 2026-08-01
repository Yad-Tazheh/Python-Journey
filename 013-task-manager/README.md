# 📋 Task Manager

A simple **Task Management System** built with **Python**, following **Object-Oriented Programming (OOP)** principles and using **SQLite** as the database.

This project was created as a learning project to practice:

- Object-Oriented Design
- SQLite
- Database Relationships
- CRUD Operations
- Unit Testing with pytest

---

# 🚀 Features

- Create projects
- Create users
- Create tasks
- Assign tasks to users
- Assign tasks to projects
- Add users to projects
- Change task status
- Delete users
- Delete tasks
- Retrieve all tasks of a user
- Retrieve all tasks of a project
- Retrieve all members of a project
- Automatic relationship management
- Unit tests using **pytest**

---

# 📦 Project Structure

```text
Task Manager
│
├── database/
│   └── db_manager.py
│
├── models/
│   ├── user.py
│   ├── task.py
│   └── project.py
│
├── tests/
│   ├── database_test.py
│   └── ...
│
└── main.py
```

---

# 🧩 Domain Model

```text
Project
│
├── Users
│     ├── Ali
│     ├── Reza
│     └── ...
│
└── Tasks
      ├── Create Database
      ├── Design Login Page
      └── Deploy Server
```

---

# 👤 User

Represents a member of a project.

### Attributes

- `user_id`
- `name`
- `email`
- `role`

Possible roles:

- ADMIN
- USER
- MANAGER

---

# ✅ Task

Represents a task inside a project.

### Attributes

- `task_id`
- `title`
- `description`
- `status`
- `priority`
- `assigned_user`
- `project_id`
- `created_at`
- `due_date`

### Status

- TODO
- PENDING
- IN_PROGRESS
- DONE
- CANCELED

### Priority

- LOW
- MEDIUM
- HIGH

---

# 📁 Project

Represents a project.

### Attributes

- `project_id`
- `name`

Projects are connected to:

- Multiple Users
- Multiple Tasks

---

# 🗄 Database Schema

## users

```text
user_id (PK)
name
email
role
```

---

## projects

```text
project_id (PK)
name
```

---

## tasks

```text
task_id (PK)
title
description
status
priority
created_at
due_date

project_id (FK)
assigned_user_id (FK)
```

---

## project_users

```text
project_id (FK)
user_id (FK)

PRIMARY KEY(project_id, user_id)
```

---

# 🔗 Relationships

```text
Project
    │
    ├──────────────┐
    │              │
    ▼              ▼
  Tasks        project_users
                    │
                    ▼
                  Users

Task
 │
 └────────────► Assigned User
```

### Relationship Types

- Project → Tasks (**One-to-Many**)
- User → Tasks (**One-to-Many**)
- Project ↔ Users (**Many-to-Many**)

---

# 🧪 Testing

Run all tests:

```bash
pytest
```

Run only database tests:

```bash
pytest tests/database_test.py
```

---

# 🛠 Technologies

- Python 3
- SQLite3
- pytest
- Git
- Object-Oriented Programming (OOP)

---

# 📚 What I Learned

During this project I practiced:

- Object-Oriented Design
- Class Relationships
- Enums
- UUIDs
- SQLite CRUD Operations
- Primary Keys
- Foreign Keys
- One-to-Many Relationships
- Many-to-Many Relationships
- SQL JOIN
- Data Validation
- Unit Testing with pytest
- Git Version Control

---

# 📄 License

This project is created for learning purposes.