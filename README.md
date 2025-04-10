# URL Shortener

A lightweight URL shortener service built with FastAPI and SQLite, featuring automatic URL expiration and a simple management interface.

This project was Vibe-coded into existence using AI, Copilot and Claude :)

## Features

- Create shortened URLs with optional custom codes
- Automatic URL expiration system
- Page title fetching
- Click tracking
- No authentication required
- Simple management interface
- Docker support

## Tech Stack

- FastAPI
- SQLite
- Bulma CSS
- Alpine.js

## Quick Start

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

4. Visit http://localhost:8000

## Docker Deployment

Build and run with Docker:

```bash
docker build -t url-shortener .
docker run -p 8000:8000 url-shortener
```

## License

MIT