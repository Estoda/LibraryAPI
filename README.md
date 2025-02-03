# Library API

This is a **Library API** built with Django and Django REST Framework (DRF). The API allows users to register, log in, and perform CRUD operations on library resources such as books. JWT authentication is used for secure login and API requests.

## Features

- **User Authentication**: Users can register and log in using JWT tokens.
- **Book Management**: Users can perform CRUD operations (Create, Read, Update, Delete) on books.
- **JWT Authentication**: JWT tokens is supported for API authentication.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [License](#license)

## Installation

Follow these steps to get the project up and running.

### 1. Clone the repository

```bash
git clone https://github.com/Estoda/LibraryAPI
cd LibraryAPI
```

### 2. Set up a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Migrate the database

```bash
python manage.py migrate
```

### 5. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

## Usage

The API can be accessed at http://localhost:8000/.

You can use tools like Postman or curl to test the API endpoints.

## API Endpoints

### 1. Register a new user

- POST /api/register/
- Request Body:

```bash
{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "password123"
}
```

- Response:

```bash
{
    "message": "Registration Successful",
    "user":
    {
        "username": "newuser",
        "email": "newuser@example.com"
    }
}
```

### 2. Login

- POST /api/login/
- Request Body:

```bash
{
    "username": "newuser",
    "password": "password123"
}
```

- Response:

```bash
{
    "id": 1,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "9780743273565"
}
```

### 3. Logout

- POST /api/logout/
- Request Body: None

- Response: 200 OK

### 4. CRUD Operations on Books (Example endpoints)

- POST /api/books/
- Request Body:

```bash
{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "9780743273565"
}
```

- Response:

```bash
{
    "id": 1,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "9780743273565"
}
```

- list all books

* GET /api/books/
* Response:

```bash
[
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "isbn": "9780743273565"
    },
    ...
]
```
