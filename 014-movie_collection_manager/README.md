# Movie Collection Manager

A backend REST API for managing a personal movie collection.

The project is built with **FastAPI**, **Pydantic**, **SQLAlchemy**, **Alembic**, **SQLite**, and **Pytest**. It follows a layered architecture that separates HTTP handling, validation, business logic, database operations, and persistence models.

---

## Tech Stack

* **FastAPI** — REST API framework
* **Pydantic** — request/response validation
* **SQLAlchemy** — ORM and database interaction
* **Alembic** — database schema migrations
* **SQLite** — development and test database
* **Pytest** — automated testing
* **python-dotenv** — environment configuration
* **Git** — version control

---

# Architecture

The application follows a layered architecture:

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
SQLAlchemy Model
  ↓
Database
```

Each layer has a specific responsibility.

## Router

Routers handle HTTP requests and responses.

Examples:

```text
GET    /movies/
POST   /movies/
GET    /movies/{movie_id}
PUT    /movies/{movie_id}
DELETE /movies/{movie_id}
```

Routers should remain thin and should not contain business rules or raw database queries.

---

## Schema

Pydantic schemas validate API input and define API responses.

For example:

```python
class MovieCreate(BaseModel):
    title: str
    description: str
    release_date: str
```

Schemas answer:

> Is the incoming data structurally valid?

They do not decide whether a movie already exists or whether a relationship is allowed.

That responsibility belongs to the Service layer.

---

## Service

The Service layer contains business logic.

For example:

```python
existing_movie = self.movie_repository.get_by_title(movie.title)

if existing_movie:
    raise MovieAlreadyExistsException("Movie already exists")
```

Services are responsible for:

* Business rules
* Duplicate checks
* Entity existence validation
* Relationship validation
* Application-specific exceptions

In simple terms:

```text
Schema:
"Is the request structurally valid?"

Service:
"Is the request allowed?"

Repository:
"How do I access the database?"
```

---

## Repository

Repositories contain database operations.

For example:

```python
def get_by_title(self, title: str):
    return (
        self.db
        .query(Movie)
        .filter(Movie.title == title)
        .first()
    )
```

The Service does not need to know how SQLAlchemy queries are implemented.

It can simply call:

```python
movie_repository.get_by_title("Inception")
```

This keeps database implementation details isolated from business logic.

---

# Domain Models

The application currently contains five main entities:

```text
Movie
Actor
Genre
User
Review
```

## Movie

A movie contains:

* Movie ID
* Title
* Description
* Release date

A movie can have multiple actors, genres, and reviews.

## Actor

An actor can participate in multiple movies.

```text
Movie ←→ Actor
```

This is implemented as a many-to-many relationship.

## Genre

A movie can have multiple genres, and a genre can contain multiple movies.

```text
Movie ←→ Genre
```

This is also a many-to-many relationship.

## User

A user can create multiple reviews.

```text
User 1 ──────── * Review
```

## Review

Each review belongs to one user and one movie.

```text
User
  │
  └────── * Reviews
              │
              │
              ▼
            Movie
```

---

# Database Relationships

## Movie ↔ Actor

Movie and Actor have a many-to-many relationship.

The relationship is represented through:

```text
movie_actors
```

with:

```text
movie_id
actor_id
```

Conceptually:

```text
Movie #1 ─── Actor #3
Movie #1 ─── Actor #7
Movie #2 ─── Actor #3
```

---

## Movie ↔ Genre

Movie and Genre also have a many-to-many relationship.

The association table is:

```text
movie_genres
```

with:

```text
movie_id
genre_id
```

Conceptually:

```text
Movie #1 ─── Genre #2
Movie #1 ─── Genre #4
Movie #3 ─── Genre #2
```

SQLAlchemy manages these relationships through relationship definitions such as:

```python
actors = relationship(
    secondary="movie_actors",
    back_populates="movies",
)
```

and:

```python
genres = relationship(
    secondary="movie_genres",
    back_populates="movies",
)
```

This allows operations such as:

```python
movie.actors.append(actor)
movie.genres.append(genre)
```

without manually inserting rows into the association tables.

---

# Database Migrations

The project uses **Alembic** to manage database schema migrations.

Instead of deleting and recreating the database whenever a model changes, Alembic tracks changes to the database schema through migration files.

The general workflow is:

```text
SQLAlchemy Models
       ↓
Alembic
       ↓
Migration
       ↓
Database Schema
```

## Create a Migration

After changing a SQLAlchemy model:

```bash
alembic revision --autogenerate -m "describe the change"
```

## Apply Migrations

```bash
alembic upgrade head
```

## Check Current Migration

```bash
alembic current
```

## View Migration History

```bash
alembic history
```

Alembic allows the database schema to evolve together with the application while keeping schema changes version-controlled.

---

# API Endpoints

The API is organized around the main domain entities.

## Movies

```text
GET    /movies/
POST   /movies/
GET    /movies/{movie_id}
PUT    /movies/{movie_id}
DELETE /movies/{movie_id}

GET    /movies/title/{title}

POST   /movies/{movie_id}/actors/{actor_id}
GET    /movies/{movie_id}/actors

POST   /movies/{movie_id}/genres/{genre_id}
GET    /movies/{movie_id}/genres
```

## Actors

```text
GET    /actors/
POST   /actors/
GET    /actors/{actor_id}
PUT    /actors/{actor_id}
DELETE /actors/{actor_id}

GET    /actors/name/{name}

POST   /actors/{actor_id}/movies/{movie_id}
GET    /actors/{actor_id}/movies
```

## Genres

```text
GET    /genres/
POST   /genres/
GET    /genres/{genre_id}
PUT    /genres/{genre_id}
DELETE /genres/{genre_id}

GET    /genres/name/{name}

POST   /genres/{genre_id}/movies/{movie_id}
GET    /genres/{genre_id}/movies
```

## Users

```text
GET    /users/
POST   /users/
GET    /users/{user_id}
PUT    /users/{user_id}
DELETE /users/{user_id}
```

## Reviews

```text
GET    /reviews/
POST   /reviews/
GET    /reviews/{review_id}
PUT    /reviews/{review_id}
DELETE /reviews/{review_id}

GET    /reviews/user/{user_id}
GET    /reviews/movie/{movie_id}
```

---

# Error Handling

The application uses custom exceptions for expected application errors.

Examples:

```text
MovieNotFoundException
MovieAlreadyExistsException
MovieAlreadyAssociatedException

ActorNotFoundException
ActorAlreadyExistsException
ActorAlreadyAssociatedException

GenreNotFoundException
GenreAlreadyExistsException
GenreAlreadyAssociatedException

UserNotFoundException
UserAlreadyExistsException

ReviewNotFoundException
```

These exceptions are handled by FastAPI exception handlers.

Typical responses include:

```text
404 Not Found
```

when an entity does not exist, and:

```text
409 Conflict
```

when an entity or relationship already exists.

For example:

```json
{
    "detail": "Movie already exists"
}
```

This keeps API error responses consistent and predictable.

---

# Dependency Injection

FastAPI dependency injection is used to construct database sessions, repositories, and services.

The dependency flow is:

```text
Request
  ↓
FastAPI Dependency
  ↓
Database Session
  ↓
Repository
  ↓
Service
  ↓
Router
```

For example, the Movie Service receives:

```text
MovieRepository
ActorRepository
GenreRepository
```

This allows the Router to depend on the Service instead of directly creating repositories or database sessions.

It also makes the application easier to test because dependencies can be overridden in tests.

---

# Testing

The project uses **Pytest** for automated testing.

Tests are organized by responsibility:

```text
tests/
├── api_tests/
├── schema_tests/
└── service_tests/
```

### API Tests

API tests verify HTTP behavior, status codes, request validation, responses, and endpoint behavior.

### Schema Tests

Schema tests verify Pydantic validation and serialization.

### Service Tests

Service tests verify business logic independently from the HTTP layer.

Examples include:

```text
Create movie
Duplicate movie
Get movie
Update movie
Delete movie

Create actor
Associate actor with movie
Duplicate actor relationship

Create genre
Associate genre with movie
Duplicate genre relationship

Create user
Duplicate user
Update user
Delete user

Create review
Get reviews by user
Get reviews by movie
Update review
Delete review
```

The tests use fixtures for database sessions, services, models, and API clients.

The test database is isolated from the development database.

---

# Development Process

The project has been developed incrementally.

The main progression was:

```text
Models
  ↓
Database
  ↓
Repositories
  ↓
Services
  ↓
Routers
  ↓
Schemas
  ↓
Exception Handling
  ↓
Relationships
  ↓
API Tests
  ↓
Service Tests
  ↓
Schema Tests
  ↓
Alembic Migrations
```

This approach makes it easier to identify problems close to where they are introduced.

---

# Testing Philosophy

Important features are tested as they are implemented.

For example, when implementing Movie ↔ Actor:

```text
Create Movie
      ↓
Create Actor
      ↓
Associate Actor with Movie
      ↓
Verify relationship
      ↓
Test missing Movie
      ↓
Test missing Actor
      ↓
Test duplicate relationship
```

Tests therefore serve two purposes:

1. Detect regressions.
2. Document expected application behavior.

---

# Engineering Principles

## Separation of Concerns

Each layer has a clear responsibility:

```text
Schema
  → API validation

Router
  → HTTP handling

Service
  → Business logic

Repository
  → Database operations

Model
  → Database structure and relationships
```

## Thin Routers

Routers should not contain business rules or raw SQLAlchemy queries.

## Business Logic in Services

Rules such as duplicate checks, existence checks, and relationship validation belong in Services.

## Database Logic in Repositories

SQLAlchemy queries belong in Repositories.

## Dependency Injection

Dependencies are constructed through FastAPI's dependency system rather than manually inside every endpoint.

## Database Migrations

Schema changes are managed through Alembic instead of manually recreating the database.

## Incremental Development

Features and relationships are introduced step by step.

## Automated Testing

Important application behavior is verified with Pytest.

---

# Running the Project

## Install Dependencies

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

---

## Run Database Migrations

Before starting the application:

```bash
alembic upgrade head
```

---

## Start the API

Run the development server with:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI's interactive documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

# Running Tests

Run the complete test suite:

```bash
python -m pytest -q
```

Run only API tests:

```bash
python -m pytest tests/api_tests -q
```

Run only schema tests:

```bash
python -m pytest tests/schema_tests -q
```

Run only service tests:

```bash
python -m pytest tests/service_tests -q
```

The test environment uses a separate configuration/database so tests do not modify the development database.

---

# Project Goal

The long-term goal is to build a clean and maintainable backend application with:

* Well-defined domain models
* RESTful APIs
* Clear entity relationships
* Layered architecture
* Dependency injection
* Repository pattern
* Service-layer business logic
* Custom exception handling
* Alembic database migrations
* Automated tests
* Clean database access
* Maintainable code structure

The project is developed incrementally:

```text
Design
  ↓
Implement
  ↓
Test
  ↓
Refactor
  ↓
Verify
  ↓
Next Feature
```

The focus is not only on making the API work, but on understanding **why the application is structured this way** and how each architectural decision improves maintainability, testing, and future development.
