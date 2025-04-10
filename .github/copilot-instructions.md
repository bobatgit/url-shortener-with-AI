# URL Shortener Application Developer Documentation

This documentation outlines the steps and best practices to build a simple URL shortener application. The app allows users to create, manage, and delete shortened URLs with an automatic expiry feature and configurable global presets. The application is designed to be lightweight, with all data stored in a single SQLite database.

## Architecture Overview

The URL shortener application is a lightweight web app with a clean separation between frontend and backend components. Users can create shortened URLs, manage them through a simple interface, and benefit from automatic expiry functionality.

### Key Features

- URL shortening with customizable short codes
- Redirection from short URLs to original URLs
- Management interface for adding, editing, and removing URLs
- Automatic URL expiration based on configurable timeframes
- Global preset configurations applied to new URL entries
- No authentication required - simplified management interface


## Tech Stack

### Backend

- **FastAPI**: Modern, high-performance Python web framework for building APIs
- **SQLite**: Serverless, self-contained SQL database engine for persistent storage
- **Pydantic**: Data validation and settings management using Python type annotations
- **Uvicorn**: ASGI server implementation for running the FastAPI application


### Frontend

- **Bulma**: Lightweight, responsive CSS framework based on Flexbox
- **Alpine.js**: Minimal JavaScript framework for adding interactive behavior directly in HTML markup
- **HTML/CSS**: Standard markup and styling languages for web interfaces


### Deployment

- **Docker**: Containerization platform for packaging the application and its dependencies


## Project Setup

### Directory Structure

```
url-shortener/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Application configuration
│   ├── models.py            # Database models
│   ├── database.py          # Database connection and utilities
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── shortener.py     # URL shortening and redirect endpoints
│   │   └── management.py    # URL management endpoints
│   └── utils/
│       ├── __init__.py
│       └── url_utils.py     # URL generation and validation utilities
├── static/
│   ├── css/
│   │   └── styles.css       # Custom styles beyond Bulma
│   └── js/
│       └── app.js           # Alpine.js component definitions
├── templates/
│   ├── base.html            # Base template with common elements
│   ├── index.html           # Homepage with shortening form
│   └── manage.html          # URL management interface
├── tests/
│   ├── __init__.py
│   ├── test_api.py          # API endpoint tests
│   └── test_utils.py        # Utility function tests
├── data/
│   └── urls.db              # SQLite database file
├── .dockerignore
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```


## Database Schema

The SQLite database will contain two main tables:

### 1. URLs Table

```sql
CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    short_code TEXT UNIQUE NOT NULL,
    original_url TEXT NOT NULL,
    title TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    click_count INTEGER DEFAULT 0,
    is_custom BOOLEAN DEFAULT 0
);

CREATE INDEX idx_short_code ON urls(short_code);
CREATE INDEX idx_expires_at ON urls(expires_at);
```


### 2. Settings Table

```sql
CREATE TABLE settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_name TEXT UNIQUE NOT NULL,
    setting_value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default settings
INSERT INTO settings (setting_name, setting_value) VALUES ('default_expiry_days', '30');
INSERT INTO settings (setting_name, setting_value) VALUES ('short_code_length', '6');
INSERT INTO settings (setting_name, setting_value) VALUES ('allow_custom_urls', 'true');
```


## Docker Configuration

### Dockerfile

```dockerfile
# Use Python slim image as base image for minimal footprint.
FROM python:3.11-slim

# Set working directory inside the container.
WORKDIR /app

# Environment variables to optimize Python runtime.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATABASE_PATH=sqlite:///./data/urls.db

# Copy dependency requirements file.
COPY requirements.txt .

# Install required Python packages.
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code into the container.
COPY . .

# Expose the port on which the FastAPI app will run.
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```


### requirements.txt

```plaintext
fastapi==0.103.1
uvicorn==0.23.2
jinja2==3.1.2
aiofiles==23.1.0
python-multipart==0.0.6
pydantic==2.3.0
```


## Best Practices and Style Guidelines

### Backend (Python/FastAPI)

1. **Code Organization**
    - Follow the separation of concerns principle by separating database, models, and routes.
    - Use utility modules for reusable functionality.
    - Implement dependency injection for database connections.
2. **API Design**
    - Use semantic HTTP methods (GET, POST, PUT, DELETE).
    - Return appropriate HTTP status codes.
    - Implement proper error handling with descriptive messages.
    - Use Pydantic models for request and response validation.
3. **Database**
    - Use context managers for database connections to ensure proper cleanup.
    - Implement indexes on frequently queried columns (short_code, expires_at).
    - Use parameterized queries to prevent SQL injection.
    - Keep database schema simple but include necessary constraints.
4. **URL Shortening Logic**
    - Generate short codes that are URL-safe (alphanumeric, no special characters).
    - Validate input URLs.
    - Check for uniqueness of short codes.
    - Implement a robust expiration mechanism.

### Frontend (HTML/Bulma/Alpine.js)

1. **HTML Structure**
    - Use semantic HTML elements.
    - Separate content, presentation, and behavior.
    - Ensure good accessibility practices (labels, ARIA attributes).
2. **Bulma CSS Framework**
    - Follow Bulma's component structure and naming conventions.
    - Use Bulma's responsive grid system for layouts.
    - Utilize Bulma's form components for consistent styling.
3. **Alpine.js Best Practices**
    - Keep component logic simple and focused.
    - Use x-data for component initialization.
    - Prefer declarative directives over imperative JavaScript.
    - Break complex components into smaller, reusable parts.
4. **User Experience**
    - Provide feedback for user actions (loading indicators, success/error messages).
    - Implement form validation.
    - Ensure responsive design for mobile users.
    - Use clear, concise labels and instructions.

### Deployment Best Practices

1. **Docker Best Practices**
    - Use lightweight base images to reduce container size.
    - Minimize image layers by combining related commands in the Dockerfile.
    - Set appropriate environment variables in the Dockerfile or runtime environment.
2. **Security Considerations**
    - Avoid running containers as root; use a non-root user where possible.
    - Properly handle sensitive information like environment variables or API keys.
3. **Performance Optimization**
    - Optimize static file serving by using a CDN or reverse proxy if scaling up is required in production environments.

