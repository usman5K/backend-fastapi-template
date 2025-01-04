
# Backend FastAPI Template

A scalable and modular FastAPI backend template designed to accelerate project development with best practices and robust architecture. This repository empowers Python developers by providing a comprehensive foundation for building backend applications.

---

## Technology Stack and Features

## Technology Stack and Features

- ⚡ **FastAPI**: A high-performance API framework that allows for rapid development of web applications.
- 🧰 **SQLAlchemy**: A powerful ORM for seamless database interactions, simplifying database operations in Python.
- 🔄 **Alembic**: Simplified database migrations to manage schema changes effectively.
- 🔑 **JWT Authentication**: Secure user authentication via JSON Web Tokens, ensuring safe access to resources.
- 🔍 **Pydantic**: Flexible data validation and settings management for robust data handling.
- 🛠️ **Environment Configuration**: Easy configuration with `.env` files for managing environment variables.
- 📦 **Dependency Injection**: Modular and clean code with FastAPI’s dependency injection system.
- 🌐 **CORS Support**: Configurable Cross-Origin Resource Sharing to manage cross-origin requests.
- 🔒 **Password Hashing**: Secure password handling with Passlib for user authentication.
- 📝 **Logging**: Comprehensive logging setup for better observability and debugging.
- 🐋 **Docker Compose**: Simplifies development and production environments using containerization.
- ✅ **Tests with Pytest**: An efficient testing framework for ensuring code reliability.
- ✨ **Code Linting**: Integrated with `ruff` for enforcing Python code style, catching potential errors, and maintaining a consistent codebase.
- 🚦 **Pre-commit Hooks**: Automated checks with `pre-commit` to run `ruff`, enforce coding standards, and format code before commits, ensuring a clean and consistent codebase.

---

## Project Structure

```
FastAPIBackendTemplate/
├── alembic.ini              # Alembic configuration for database migrations
├── docker-compose.yml       # Docker Compose setup for containerized environments
├── Dockerfile               # Dockerfile for containerizing the application
├── .dockerignore            # Dockerignore file for ignoring certain files while creating docker image
├── poetry.lock              # Dependency lock file
├── pyproject.toml           # Project metadata and dependencies
├── pytest.ini               # Pytest configuration
├── .pre-commit-config.yaml  # Pre-commit hooks configuration
├── .env.template            # Environment variable template
├── .gitignore               # Git ignored files configuration
├── app/                     # Main application folder
│   ├── __init__.py          # Package initialization
│   ├── main.py              # Application entry point
│   ├── utils.py             # Utility functions
│   ├── api/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── deps.py          # Dependencies for endpoints
│   │   ├── v1_router.py     # Router for versioned API
│   │   └── v1/              # Version 1 specific endpoints
│   │       ├── __init__.py
│   │       ├── auth.py      # Authentication endpoints
│   │       └── user.py      # User management endpoints
│   ├── core/                # Core application components
│   │   ├── __init__.py
│   │   ├── config.py        # Configuration management
│   │   ├── logger.py        # Logging setup
│   │   └── security.py      # Security-related utilities
│   ├── crud/                # CRUD operations
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication-related CRUD
│   │   └── user.py          # User-related CRUD
│   ├── db/                  # Database configurations
│   │   ├── __init__.py
│   │   ├── base_class.py    # Base ORM class
│   │   └── session.py       # Database session management
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── user.py          # User model definition
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── common.py        # Shared schemas
│   │   └── user.py          # User-specific schemas
│   ├── services/            # Business logic
│   │   └── __init__.py
│   └── alembic/             # Alembic migration scripts
│       ├── env.py
│       ├── README
│       ├── script.py.mako
│       └── versions/        # Individual migration versions
├── scripts/                 # Helper scripts
│   └── start-backend.sh     # Backend startup script
├── tests/                   # Test cases
│   ├── __init__.py
│   ├── conftest.py          # Test configuration
│   └── test_user.py         # User tests
└── ReadME.md                # Project documentation
```

---

## Prerequisites

- Python 3.12 or higher
- PostgreSQL
- Docker (optional, for containerized deployment)

---

## Installation

### 1. Clone the Repository
```bash
  git clone https://github.com/usman5K/backend-fastapi-template.git
  cd backend-fastapi-template
```

### 2. Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies:

```bash
  python -m venv venv
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
Use Poetry to manage project dependencies:
```bash
  pip install poetry
  poetry install
```

### 4. Set Up Environment Variables
Copy the `.env.template` file to `.env` and configure your environment variables:

```console
   DATABASE_URL=postgresql://user:password@localhost/dbname
   SECRET_KEY=your_secret_key
   ,,,
```

Ensure PostgreSQL is running and accessible with the provided credentials.

### 5. Run Database Migrations
Apply migrations using Alembic:
```bash
  alembic upgrade head
```

### 6. Start the Application
Run the FastAPI application with Uvicorn:
```bash
   uvicorn app.main:app --reload
```

#### The application will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Usage

- **Interactive API Documentation**:
  - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
  - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

![Swagger UI Documentation](./static/img.png)

- **User Management**:
  - Endpoints for user registration, login, profile management, and password reset.

- **Authentication**:
  - Protect endpoints with JWT-based authentication.

- **Testing**:
  - Write and execute tests using the `tests/` directory.
  - Run tests with Pytest:
    ```bash
      pytest
    ```

---
## Developer Guidance: How to Utilize This Template
### 1. Create a New Repository
- Create a new repository on GitHub where you will store your project. This will be your personal repository.

### 2. Clone the Template Repository
- Clone the template repository to your local machine:
    ```bash
    git clone https://github.com/usman5K/backend-fastapi-template.git
    cd backend-fastapi-template
    ```

### 3. Initialize Your New Repository
- Remove the current remote reference (which points to the original template repository) to prevent accidental pushes:
    ```bash
    git remote remove origin
    ```

- Initialize your new repository as the origin:
    ```bash
    git remote add origin https://github.com/your_username/your_repository.git
    ```

### 4. Push to Your New Repository
- Push the content of the template repository to your new private repository:
    ```bash
    git push -u origin main
    ```

### 5. Customize and Develop
- Now, you can start customizing the template by modifying models, schemas, and endpoints as per your project requirements.

### 6. Commit Your Changes
- Stage and commit your changes:
    ```bash
    git add .
    git commit -m "Initial setup and customization"
    ```

### 7. Push Changes
- Push your changes to your repository:
    ```bash
    git push origin main
    ```

### 8. Testing and Validation
- Write tests for new features and ensure that existing tests pass:
    ```bash
    pytest
    ```

### 9. Containerize Your Application
- Use the provided Docker setup to containerize your application for deployment across environments.

---
## Contributing

Contributions are welcome!

To contribute:
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to your fork:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

Refer to the [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed contribution guidelines.

---

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

---

## Contact

For any inquiries, feel free to contact:

**Usman Khan**  
Email: [work.usmankhan@gmail.com](mailto:work.usmankhan@gmail.com)

You can also connect with me on [LinkedIn](https://www.linkedin.com/in/usmankhan43).