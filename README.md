# JWT Authentication API (FastAPI)

A backend authentication system built using FastAPI and JWT.

## Features

- User registration API
- Secure password hashing using bcrypt
- Login API with JWT token generation
- Protected API routes
- Token verification middleware

## Tech Stack

- Python
- FastAPI
- JWT (python-jose)
- Passlib (bcrypt)

## How to Run

Install dependencies:

pip install -r requirements.txt

Run server:

uvicorn main:app --reload

Open API docs:

http://127.0.0.1:8000/docs
