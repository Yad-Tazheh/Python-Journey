# 📋 Task Manager (SQLAlchemy ORM Edition)

A Python Task Management System built with **SQLAlchemy ORM** and **PostgreSQL**.

This branch is a complete migration of the original SQLite implementation to SQLAlchemy ORM, focusing on object-oriented database design, relationships, and clean architecture.

---

## 🚀 Technologies

* Python 3
* PostgreSQL
* SQLAlchemy 2.0 (ORM)
* pytest

---

## 📂 Project Structure

```text
TaskManager/
│
├── database/
│   ├── base.py
│   └── database.py
│
├── models/
│   ├── association.py
│   ├── project.py
│   ├── task.py
│   └── user.py
│
├── tests/
│   ├── conftest.py
│   └── database_test.py
│
└── main.py
```

---

## 🧩 Database Models

### User

Represents a system user.

**Fields**

* user_id
* name
* email
* role

**Relationships**

* One-to-Many → Tasks
* Many-to-Many → Projects

---

### Task

Represents a task inside a project.

**Fields**

* task_id
* title
* description
* status
* priority
* created_at
* due_date

**Relationships**

* Many-to-One → User
* Many-to-One → Project

---

### Project

Represents a project.

**Fields**

* project_id
* name

**Relationships**

* One-to-Many → Tasks
* Many-to-Many → Users

---

### Association Table

`project_users`

Implements the Many-to-Many relationship between Users and Projects.

---

## 🗃 Database Relationships

```text
User
│
├── 1 ------ * Task
│
└── * ------ * Project


Project
│
├── 1 ------ * Task
│
└── * ------ * User
```

---

## ✅ Implemented Features

* SQLAlchemy ORM models
* PostgreSQL integration
* User CRUD
* Task CRUD
* Project CRUD
* User ↔ Task relationship
* Project ↔ Task relationship
* Project ↔ User many-to-many relationship
* Automated ORM relationship management
* Unit tests with pytest

---

## 🧪 Running Tests

```bash
pytest
```

---

## 📌 Current Status

This branch contains the SQLAlchemy ORM implementation.

Future improvements include:

* Repository Pattern
* Cascade behaviors
* Lazy vs Eager Loading
* Alembic Migrations
* Service Layer
* Generic Repository
