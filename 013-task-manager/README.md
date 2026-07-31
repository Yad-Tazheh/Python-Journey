# 📋 Task Manager

A simple Object-Oriented Task Management System built with Python.

---

## 📖 Project Overview

A **Project** contains a collection of **Users** and **Tasks**.

Users can be added to a project, tasks can be created, and each task can be assigned to one user.

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

## 🧩 Classes

### User

Represents a member of the project.

**Attributes**

* `name`
* `user_id`
* `email`
* `role`

  * `ADMIN`
  * `USER`
  * `MANAGER`
* `tasks`

Example:

```text
Ali
Role: ADMIN

Reza
Role: USER
```

---

### Task

Represents a single task inside a project.

**Attributes**

* `title`
* `description`
* `task_id`
* `status`

  * `TODO`
  * `PENDING`
  * `IN_PROGRESS`
  * `DONE`
  * `CANCELED`
* `priority`

  * `LOW`
  * `MEDIUM`
  * `HIGH`
* `assigned_user`
* `created_at`
* `due_date`

---

### Project

Represents a project that contains users and tasks.

**Attributes**

* `name`
* `project_id`
* `users`
* `tasks`

Example:

```text
Website Project

Users
- Ali
- Reza

Tasks
- Create Database
- Design Login Page
- Deploy Server
```

---

## ⚙️ Main Capabilities

* Create a project
* Add users
* Add tasks
* Assign tasks to users
* Change task status
* Change user roles
* Remove users
* Remove tasks
* Display project summary
* Save project data to JSON
* Load project data from JSON
* Restore relationships after loading
