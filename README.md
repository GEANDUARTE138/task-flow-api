
# Task Flow API Documentation

## 1. Introduction

The Task Flow API is designed to manage projects, activities, and customers within a task flow management system. It allows for creating, updating, and managing entities such as customers, projects, and activities. Each entity has a status that tracks its lifecycle, and relationships between entities are clearly defined, making it easy to track dependencies.

This API is developed using Python 3.12, FastAPI, SQLAlchemy for ORM, and MySQL for database management. It follows the best practices of clean code and a service-oriented architecture.

## 2. Entity Relationship Diagram (ERD)
_Include the EER diagram image here once generated._

## 3. Project Setup and Local Execution

To set up and run this project locally, follow these steps:

### 3.1 Prerequisites
- Python 3.12
- Poetry (for dependency management)
- MySQL (database)
- Docker (optional, but recommended)

### 3.2 Setup Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd task-flow-api
   ```

2. **Install dependencies using Poetry:**
   ```bash
   poetry install
   ```

3. **Set up environment variables:**
   Rename `local.env` to `.env` and update the following variables if necessary:
   - `API_KEY`: Your API key for securing endpoints.
   - `DB_USER`: Database username
   - `DB_PASSWORD`: Database password
   - `DB_HOST`: Database host (default: localhost)
   - `DB_PORT`: Database port (default: 3306)
   - `DB_NAME`: Name of the MySQL database

4. **Run the MySQL database using Docker (optional but recommended):**
   ```bash
   docker-compose up
   ```

5. **Apply database migrations:**
   ```bash
   poetry run alembic upgrade head
   ```

6. **Run the FastAPI application:**
   ```bash
   poetry run uvicorn src.app:app --reload
   ```

7. **Access the API documentation:**
   Open your browser at `http://127.0.0.1:8000/docs` to view the Swagger documentation.
