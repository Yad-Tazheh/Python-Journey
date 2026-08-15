# Python Journey

A collection of Python projects built while learning and practicing Python.

The projects are numbered in the order they were developed.

## Structure

```text
Python-Journey/
│
├── 001-.../
├── 002-.../
├── ...
├── 014-movie_collection_manager/
│
└── README.md
```

Each project has its own purpose and may use different technologies and architectures.

## Main Project Structure

The larger projects may contain folders such as:

```text
models/        → Database models
schemas/       → Data validation
repositories/  → Database operations
services/      → Business logic
routers/       → API endpoints
exceptions/    → Custom exceptions
database/      → Database configuration
tests/         → Automated tests
alembic/       → Database migrations
```

## Current Project

### `014-movie_collection_manager`

A FastAPI backend for managing movies, actors, genres, users, and reviews.

Technologies include:

* FastAPI
* SQLAlchemy
* Pydantic
* Alembic
* SQLite
* Pytest

The project follows a layered architecture:

```text
Router
   ↓
Schema
   ↓
Service
   ↓
Repository
   ↓
Database
```

Each project contains its own README with more details.
