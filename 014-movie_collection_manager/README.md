:::writing{variant="document" id="73921" title="README.md"}
# 🎬 Movie Collection Manager

A clean and maintainable **REST API backend** for managing a personal movie collection.

Built with:

- ⚡ FastAPI
- 🐍 Python
- 🗄️ SQLAlchemy
- 🔄 Alembic
- 🔐 JWT Authentication
- 🧪 Pytest
- 📦 Repository Pattern
- 🏗️ Service Layer Architecture

---

## ✨ Features

- 🎬 Movie CRUD operations
- 🎭 Actor management
- 🎞️ Genre management
- ⭐ Movie reviews
- 👤 User authentication
- 🔑 JWT authorization
- 🛡️ Role-based access control
- 🔄 Database migrations with Alembic
- 🧪 Automated testing

---

# 🏗️ Project Architecture

The project follows a layered backend architecture:

```text
Client
  ↓
Router
  ↓
Schema
  ↓
Service
  ↓
Repository
  ↓
Model
  ↓
Database