# Movie Collection Manager

A backend API for managing a personal movie collection.

The project is built with **FastAPI**, **Pydantic**, **SQLAlchemy**, and **Pytest**, following a layered architecture that separates API handling, validation, business logic, database operations, and persistence models.

---

## Tech Stack

* **FastAPI** — REST API framework
* **Pydantic** — request/response validation
* **SQLAlchemy** — ORM and database interaction
* **Pytest** — automated testing
* **SQLite** — development database
* **Git** — version control

---

## Architecture

The application follows a layered architecture:

```text
Client
  ↓
Router (FastAPI)
  ↓
Schema (Pydantic)
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

### Router

The Router is responsible for handling HTTP requests and responses.

For example:

```text
POST /movies/
GET /movies/1
PUT /movies/1
DELETE /movies/1
```

The Router should not contain business logic or database queries.

Its main responsibility is to receive the request and pass it to the appropriate service.

---

### Schema

Pydantic schemas are the **guard dog of the API input**.

They validate whether the request has the correct structure and data types.

For example:

```python
class MovieCreate(BaseModel):
    title: str
    description: str
    release_date: str
```

The schema can determine that:

```json
{
  "title": 123
}
```

is invalid because `title` is expected to be a string.

However, the schema does **not** know whether the movie already exists in the database.

That is the responsibility of the Service layer.

---

### Service

The Service layer contains the application's **business logic**.

The Service answers questions such as:

> Is this request allowed according to the rules of the application?

For example, a movie with a duplicate title should not be created.

```python
existing_movie = self.movie_repository.get_by_title(movie.title)

if existing_movie:
    raise MovieAlreadyExistsException("Movie already exists")
```

The Service layer is responsible for:

1. Business rules
2. Duplicate checks
3. Entity existence validation
4. Domain-related decisions
5. Application exceptions

In other words:

```text
Schema:
"Is this request structurally healthy?"

Service:
"Is this request allowed by the application's rules?"
```

---

### Repository

The Repository layer handles database operations.

The Service layer should **not need to know how SQLAlchemy works**.

For example, the Service can simply call:

```python
movie_repository.get_by_title("Inception")
```

without knowing how the database query is implemented.

The Repository translates that operation into SQLAlchemy:

```python
def get_by_title(self, title: str) -> Movie | None:
    return (
        self.db
        .query(Movie)
        .filter(Movie.title == title)
        .first()
    )
```

This separation gives us:

```text
Service
    ↓
get_by_title("Inception")
    ↓
Repository
    ↓
SQLAlchemy query
    ↓
Database
```

The Service therefore does not depend directly on SQLAlchemy implementation details.

---

## Domain Models

The project currently contains the following main entities:

```text
Movie
Actor
Genre
User
Review
```

### Movie

A movie contains information such as:

* movie ID
* title
* description
* release date

A movie can have multiple:

* Actors
* Genres
* Reviews

---

### Actor

An actor can participate in multiple movies.

This creates a **many-to-many relationship** between Movie and Actor.

```text
Movie ←→ Actor
```

---

### Genre

A movie can belong to multiple genres, and a genre can contain multiple movies.

Therefore:

```text
Movie ←→ Genre
```

is also a **many-to-many relationship**.

---

### Review

A review belongs to:

* one User
* one Movie

Therefore the relationships are:

```text
User 1 ──────── * Review
Movie 1 ─────── * Review
```

---

# Database Relationships

## Movie ↔ Genre

The Movie and Genre relationship is many-to-many.

Instead of storing multiple genre IDs directly inside the Movie table, an association table is used.

```text
movies
   │
   │
   └──── movie_genres ──── genres
```

The association table contains two foreign keys:

```text
movie_genres

movie_id
genre_id
```

Conceptually:

```text
Movie #1 ─── Genre #2
Movie #1 ─── Genre #4
Movie #3 ─── Genre #2
```

---

## Movie ↔ Actor

Movie and Actor also have a many-to-many relationship.

An association table is used:

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

SQLAlchemy manages these relationships through:

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

This allows relationship operations such as:

```python
movie.actors.append(actor)
movie.genres.append(genre)
```

without manually inserting rows into the association tables.

---

# Development Process

From now on, we will be engineering this project in a more structured way.

Instead of building everything at once, we will proceed **step by step**, and each important feature will be accompanied by tests.

Our goal is to build the application incrementally while keeping the architecture clean and making sure every layer behaves correctly.

---

## 1. Testing Framework

We created a testing framework for the Movie Collection Manager project using **Pytest**.

The goal is to test each model and API feature independently and verify the behavior of the application as development progresses.

The testing structure is organized around API tests such as:

```text
tests/
└── api_tests/
    ├── test_movie.py
    ├── test_actor.py
    ├── test_genre.py
    ├── test_review.py
    └── test_user.py
```

A shared `conftest.py` provides common testing fixtures such as the test client and test database session.

---

## 1.1 Genre Model Foundation

We initially created a basic `genre.py` model **without relationships**.

The reason was to make sure:

```python
Base.metadata.create_all()
```

could create the database schema correctly before introducing more complicated relationships.

The relationship was intentionally added later.

This incremental approach made it easier to identify database and model problems.

---

## 1.2 Movie Model Foundation

We followed the same approach with `movie.py`.

First, we created the basic Movie model without relationships.

Once the basic model and database creation were working correctly, we introduced relationships incrementally.

---

## 1.3 Movie ↔ Genre Relationship

After the basic Movie and Genre models were working, we introduced their relationship.

The relationship is:

```text
Movie ←→ Genre
```

and is implemented as a **many-to-many relationship**.

---

## 1.3.1 Movie-Genre Association Table

We created an association table:

```text
movie_genres
```

to establish the many-to-many relationship.

The table contains two foreign keys:

```text
movie_id → movies.movie_id
genre_id → genres.genre_id
```

Conceptually:

```text
movies
   │
   │ movie_id
   ▼
movie_genres
   ▲
   │ genre_id
   │
genres
```

This allows one Movie to have many Genres and one Genre to belong to many Movies.

---

## 1.4 Movie ↔ Actor Relationship

We then created `actor.py` and established the relationship between Movies and Actors.

The relationship is also:

```text
Movie ←→ Actor
```

and is implemented as many-to-many.

---

## 1.4.1 Movie-Actor Association Table

We created:

```text
movie_actors
```

with two foreign keys:

```text
movie_id → movies.movie_id
actor_id → actors.actor_id
```

This association table represents which actors participate in which movies.

---

## 1.4.2 Review Relationships

We defined the relationships between Review, User, and Movie.

A Review belongs to one User and one Movie:

```text
User
  │
  └─────── * Reviews
                │
                │
                ▼
              Movie
```

This means a user can create multiple reviews, while each review is associated with one movie.

---

# 1.5 Movie Repository

After establishing the initial models, we created the Movie Repository.

The repository is responsible for database operations such as:

```python
get_all()
get_by_id()
get_by_title()
create()
update()
delete()
```

The repository hides SQLAlchemy implementation details from the Service layer.

For example:

```python
movie_repository.get_by_title("Inception")
```

is enough for the Service.

The Service does not need to know that the Repository internally uses:

```python
session.query(Movie)
```

This separation makes the application easier to maintain and test.

---

# 1.6 Movie Service

After creating the Movie Repository, we created the Movie Service.

The Service sits between the Router and Repository:

```text
Router
   ↓
MovieService
   ↓
MovieRepository
```

The Service is responsible for business rules.

For example, when creating a movie:

```text
Client
   ↓
MovieCreate
   ↓
MovieService
   ↓
Does movie already exist?
   ↓
YES → MovieAlreadyExistsException
   ↓
NO
   ↓
MovieRepository.create()
```

This keeps business logic out of the Router and database logic out of the Service.

---

# Relationship API Development

After the basic CRUD operations and tests were completed, we started exposing relationships through API endpoints.

For example:

### Add Actor to Movie

```http
POST /movies/{movie_id}/actors/{actor_id}
```

### Get Movie Actors

```http
GET /movies/{movie_id}/actors
```

### Add Genre to Movie

```http
POST /movies/{movie_id}/genres/{genre_id}
```

### Get Movie Genres

```http
GET /movies/{movie_id}/genres
```

These endpoints use the same layered architecture:

```text
Router
   ↓
MovieService
   ↓
MovieRepository
ActorRepository
GenreRepository
   ↓
SQLAlchemy relationships
   ↓
Association tables
```

---

# Error Handling

The application uses custom exceptions instead of returning generic errors from the Service layer.

Examples include:

```text
MovieNotFoundException
ActorNotFoundException
GenreNotFoundException
UserNotFoundException
ReviewNotFoundException
```

Relationship-specific errors are also handled.

For example:

```text
ActorAlreadyAssociatedException
GenreAlreadyAssociatedException
```

A duplicate relationship results in:

```http
409 Conflict
```

while a missing entity results in:

```http
404 Not Found
```

This makes the API behavior predictable and meaningful.

---

# Testing Philosophy

Tests are written while features are being developed rather than waiting until the entire project is finished.

For example, when implementing Movie ↔ Actor:

```text
Create Movie
      ↓
Create Actor
      ↓
Add Actor to Movie
      ↓
Verify relationship
      ↓
Test missing Movie
      ↓
Test missing Actor
      ↓
Test duplicate relationship
```

This approach helps us catch problems close to where they are introduced.

The tests also document the expected behavior of the API.

---

# Engineering Principles

The project follows several important principles:

### Separation of concerns

Each layer has one primary responsibility.

```text
Schema     → API data validation
Router     → HTTP handling
Service    → Business logic
Repository → Database operations
Model      → Database structure and relationships
```

### Thin Routers

Routers should not contain business rules or raw database queries.

### Business logic in Services

Rules such as duplicate checks and entity existence validation belong in the Service layer.

### Database logic in Repositories

SQLAlchemy queries should remain inside Repositories.

### Incremental development

Models and relationships are introduced gradually instead of building the entire database structure at once.

### Test-driven verification

Each important feature is verified with Pytest tests.

---

# Project Goal

The long-term goal is to turn the Movie Collection Manager into a clean, maintainable backend application with:

* Well-defined domain models
* RESTful APIs
* Clear relationships between entities
* Layered architecture
* Custom exception handling
* Automated tests
* Clean database access
* Maintainable business logic

The project is being developed incrementally, with each new feature designed, implemented, tested, and verified before moving to the next stage.
