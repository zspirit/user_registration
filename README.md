# FastAPI User Authentication System

A modular FastAPI project with user authentication and management features. The architecture separates concerns into **routes**, **services**, and **repositories**, making the project maintainable, scalable, and easy to test.

## Project Structure

```
Project Root
│
├── main.py                  # Entry point, initializes FastAPI app
├── config.py                # App-wide configuration (DB, settings)
├── repository.py            # Optional: shared repository layer (DB connections)
│
└── app/
    ├── auth/                # Authentication module
    │   ├── dependencies.py  # DI for auth services
    │   ├── exceptions.py    # Auth-specific exceptions
    │   ├── model.py         # DB models for auth (tokens, etc.)
    │   ├── repository.py    # DB access for auth
    │   ├── route.py         # API endpoints for login, logout, refresh
    │   ├── service.py       # Business logic for auth
    │   └── utils.py         # Helpers: password hashing, JWT, etc.
    │
    └── users/               # User management module
        ├── dependencies.py  # DI for user services
        ├── exceptions.py    # User-specific exceptions
        ├── model.py         # User DB models
        ├── repository.py    # CRUD operations on users
        ├── route.py         # API endpoints: create, update, get users
        └── service.py       # Business logic for users
```

## Interaction Flow

1. **Client → Route Layer**
   API requests hit `auth/route.py` or `users/route.py`.

2. **Route Layer → Service Layer**
   Routes call respective `service.py` methods containing business logic.

3. **Service Layer → Repository Layer**
   `service.py` interacts with `repository.py` for database operations.

4. **Repository Layer → Database**
   Performs CRUD operations via ORM (SQLAlchemy, Tortoise, etc.).

## Auth Utilities

* Password hashing
* JWT token creation and verification
* Token refresh and invalidation

## Dependencies

* Provides shared resources via FastAPI Dependency Injection:

  * Database session
  * Current authenticated user
  * Auth services

## Getting Started

### Requirements

* Python 3.11+
* FastAPI
* Pydantic
* Passlib (for password hashing)
* PyJWT (for token handling)

check the requirements.txt
```bash
requirements.txt
```

### Installation

```bash
git clone git@github.com:zspirit/user_registration.git
cd user_registration
pip install -r requirements.txt
```

### Run the Application

```bash
uvicorn app.main:app --reload
```
using docker 
```bash
docker-compose build --no-cache
docker-compose run --rm test
docker-compose up
```

The API will be available at `http://127.0.0.1:8000`.
docs are available at `http://localhost:8000/docs`
test report is avaible at `http://localhost:8000/report/report.html`

## This project leverages AI assistance for

* Generating this `README.md` file and files structure.
* Helping to write and adapt tests
* Adapting code to pass specific tests efficiently.

## Future Improvements

* Integrate a full ORM such as **SQLAlchemy** or **SQLModel** for more robust database management.
* Add endpoints for user actions such as:

  * Reset password
  * Update user data
  * Forgot password flow
  * Expose a User CRUD 
  * Deploy containers in a cloud like AWS EC2, DigitalOcean...
