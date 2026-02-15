# Interview Performance Analyzer Backend

This is a production-style backend for an Interview Performance Analyzer, built with Python, FastAPI, and SQLAlchemy.

## 📂 Project Structure

- **`app/`**: The core application logic.
  - **`api/`**: Contains API routes (endpoints). This is where requests enter the system.
  - **`services/`**: Contains business logic. This handles complex operations and interacts with the database.
  - **`models/`**: Defines the database models using SQLAlchemy.
  - **`schemas/`**: Defines Pydantic models for data validation (request/response schemas).
  - **`utils/`**: Helper functions used throughout the application.
  - **`database.py`**: Handles database connection and session management.
  - **`main.py`**: Initializes the FastAPI application and includes routers.
  - **`config.py`**: Manages configuration and environment variables.

## 🚀 Getting Started

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Server:**
    Navigate to the `backend` folder and run:
    ```bash
    uvicorn app.main:app --reload
    ```

3.  **Explore the API:**
    Open your browser and visit: `http://127.0.0.1:8000/docs` to see the interactive Swagger UI.

## 🔄 How Requests Flow

1.  **Request**: Ideally, a client (frontend) sends an HTTP request (e.g., `POST /api/v1/interviews/example`).
2.  **Route (`api/`)**: The request hits the router defined in `app/api/interviews.py`.
    -   The schema (`schemas/interview.py`) validates the request data.
    -   A database session is injected (`Depends(get_db)`).
3.  **Service (`services/`)**: The route calls a service function (e.g., `interview_service.create_interview`).
    -   This keeps the logic separated from the HTTP handling.
4.  **Database (`models/`)**: The service interacts with the database using the SQLAlchemy model (`models/interview.py`).
5.  **Response**: The service returns data to the route, which returns it to the client, validated again by the response schema.

## 🛠 Tech Stack

-   **FastAPI**: Modern, fast web framework for building APIs with Python.
-   **SQLAlchemy**: The Python SQL Toolkit and Object Relational Mapper.
-   **Pydantic**: Data validation and settings management using Python type hinting.
-   **Uvicorn**: Lightning-fast ASGI server implementation.
