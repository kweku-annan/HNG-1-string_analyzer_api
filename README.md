# String Analyzer API

A RESTful API service that analyzes strings and stores their computed properties. Built with Flask and SQLAlchemy.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running Locally](#running-locally)
- [API Documentation](#api-documentation)
- [Environment Variables](#environment-variables)
- [Testing the API](#testing-the-api)
- [Deployment](#deployment)
- [Error Handling](#error-handling)

## Features

- Analyze strings and compute various properties:
  - Length
  - Palindrome detection (case-insensitive)
  - Unique character count
  - Word count
  - SHA-256 hash
  - Character frequency mapping
- Store analyzed strings in a SQLite database
- Retrieve strings with advanced filtering options
- Natural language query support
- Full CRUD operations (Create, Read, Delete)

## Technologies Used

- **Python 3.8+**
- **Flask** - Web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Database (file-based, no separate server required)

## Project Structure
```
string-analyzer-api/
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (optional)
├── .gitignore                     # Git ignore file
├── README.md                      # Project documentation
│
├── app/
│   ├── __init__.py
│   │
│   ├── models/
│   │   └── string_analyzer.py     # StringAnalyzer database model
│   │
│   ├── schemas/
│   │   └── dbStorage.py           # Database operations (CRUD)
│   │
│   ├── utils/
│   │   └── string_analyzer.py     # String analysis utility functions
│   │
│   ├── routes/
│   │   └── string_routes.py       # API endpoints/routes
│   │
│   └── storage.py                 # Storage instance initialization
│
└── string_analyzer.db             # SQLite database file (auto-generated)
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository:**
```bash
   git clone https://github.com/kweku-annan/HNG-1-string_analyzer_api
   cd HNG-1-string_analyzer_api
```

2. **Create a virtual environment:**
```bash
   python -m venv venv
```

3. **Activate the virtual environment:**
   
   **On macOS/Linux:**
```bash
   source venv/bin/activate
```
   
   **On Windows:**
```bash
   venv\Scripts\activate
```

4. **Install dependencies:**
```bash
   pip install -r requirements.txt
```

## Running Locally

1. **Ensure virtual environment is activated**

2. **Run the Flask application:**
```bash
   python app.py
```

3. **The API will be available at:**
```
   http://localhost:5000
```

4. **Test the home endpoint:**
```bash
   curl http://localhost:5000/
```

## API Documentation

### Base URL
```
http://localhost:5000  (local development)
```

---

### 1. Create/Analyze String

**Endpoint:** `POST /strings`

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "value": "string to analyze"
}
```

**Success Response (201 Created):**
```json
{
  "id": "94b4087035c47dc5ec70499327758a792a6a4db132313a67143ec61dc489c33f",
  "value": "string to analyze",
  "properties": {
    "length": 17,
    "is_palindrome": false,
    "unique_characters": 13,
    "word_count": 3,
    "sha256_hash": "94b4087035c47dc5ec70499327758a792a6a4db132313a67143ec61dc489c33f",
    "character_frequency_map": {
      "s": 1,
      "t": 2,
      "r": 1,
      "i": 1,
      "n": 2,
      "g": 1,
      " ": 2,
      "o": 1,
      "a": 2,
      "l": 1,
      "y": 1,
      "z": 1,
      "e": 1
    }
  },
  "created_at": "2025-10-22T13:03:03Z"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid request body or missing "value" field
- `409 Conflict` - String already exists in the system
- `422 Unprocessable Entity` - Invalid data type for "value" (must be string)

---

### 2. Get Specific String

**Endpoint:** `GET /strings/{string_value}`

**Example:**
```bash
curl http://localhost:5000/strings/hello
```

**Success Response (200 OK):**
```json
{
  "id": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
  "value": "hello",
  "properties": {
    "length": 5,
    "is_palindrome": false,
    "unique_characters": 4,
    "word_count": 1,
    "sha256_hash": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
    "character_frequency_map": {
      "h": 1,
      "e": 1,
      "l": 2,
      "o": 1
    }
  },
  "created_at": "2025-10-22T13:05:00Z"
}
```

**Error Response:**
- `404 Not Found` - String does not exist in the system

---

### 3. Get All Strings with Filtering

**Endpoint:** `GET /strings`

**Query Parameters:**
- `is_palindrome` (boolean) - Filter by palindrome status (true/false)
- `min_length` (integer) - Minimum string length
- `max_length` (integer) - Maximum string length
- `word_count` (integer) - Exact word count
- `contains_character` (string) - Single character to search for

**Examples:**
```bash
# Get all palindromes
curl "http://localhost:5000/strings?is_palindrome=true"

# Get strings between 5 and 20 characters
curl "http://localhost:5000/strings?min_length=5&max_length=20"

# Get single-word strings containing 'a'
curl "http://localhost:5000/strings?word_count=1&contains_character=a"
```

**Success Response (200 OK):**
```json
{
  "data": [
    {
      "id": "hash1",
      "value": "racecar",
      "properties": { /* ... */ },
      "created_at": "2025-10-22T13:05:00Z"
    }
  ],
  "count": 1,
  "filters_applied": {
    "is_palindrome": true
  }
}
```

**Error Response:**
- `400 Bad Request` - Invalid query parameter values or types

---

### 4. Natural Language Filtering

**Endpoint:** `GET /strings/filter-by-natural-language`

**Query Parameters:**
- `query` (string) - Natural language query

**Supported Query Patterns:**
- "all single word palindromic strings"
- "strings longer than 10 characters"
- "palindromic strings that contain the first vowel"
- "strings containing the letter z"

**Example:**
```bash
curl "http://localhost:5000/strings/filter-by-natural-language?query=single%20word%20palindromic%20strings"
```

**Success Response (200 OK):**
```json
{
  "data": [
    {
      "id": "hash1",
      "value": "racecar",
      "properties": { /* ... */ },
      "created_at": "2025-10-22T13:05:00Z"
    }
  ],
  "count": 1,
  "interpreted_query": {
    "original": "single word palindromic strings",
    "parsed_filters": {
      "word_count": 1,
      "is_palindrome": true
    }
  }
}
```

**Error Responses:**
- `400 Bad Request` - Unable to parse natural language query
- `422 Unprocessable Entity` - Query parsed but resulted in conflicting filters

---

### 5. Delete String

**Endpoint:** `DELETE /strings/{string_value}`

**Example:**
```bash
curl -X DELETE http://localhost:5000/strings/hello
```

**Success Response:**
- `204 No Content` - String successfully deleted (empty response body)

**Error Response:**
- `404 Not Found` - String does not exist in the system

---

## Environment Variables

Currently, the application uses default settings and doesn't require environment variables. However, you can optionally create a `.env` file for future configuration:
```env
# Example .env file (optional)
FLASK_ENV=development
DATABASE_URL=sqlite:///string_analyzer.db
PORT=5000
```

**Note:** If you add environment variables, install `python-dotenv`:
```bash
pip install python-dotenv
```

And load them in `app.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Testing the API

### Using curl

**Create a string:**
```bash
curl -X POST http://localhost:5000/strings \
  -H "Content-Type: application/json" \
  -d '{"value": "hello world"}'
```

**Get a string:**
```bash
curl http://localhost:5000/strings/hello%20world
```

**Get all strings:**
```bash
curl http://localhost:5000/strings
```

**Delete a string:**
```bash
curl -X DELETE http://localhost:5000/strings/hello%20world
```

### Using Postman

1. Import the endpoints into Postman
2. Set `Content-Type: application/json` header for POST requests
3. Use the examples provided in the API Documentation section

### Using Python requests
```python
import requests

# Create a string
response = requests.post(
    'http://localhost:5000/strings',
    json={'value': 'hello world'}
)
print(response.json())

# Get a string
response = requests.get('http://localhost:5000/strings/hello%20world')
print(response.json())
```

## Deployment

### Deployment Options

This application can be deployed to:
- **Railway** (Recommended)
- **Heroku**
- **AWS (EC2, Elastic Beanstalk, Lambda)**
- **PythonAnywhere**
- **DigitalOcean App Platform**

### General Deployment Steps

1. **Ensure all dependencies are in requirements.txt**
2. **Set up your deployment platform account**
3. **Connect your GitHub repository**
4. **Configure build settings:**
   - Build command: `pip install -r requirements.txt`
   - Start command: `python app.py` or use gunicorn
5. **Deploy!**

### Using Gunicorn (Production)

For production deployments, use Gunicorn instead of Flask's development server:

1. **Add to requirements.txt:**
```
   gunicorn==21.2.0
```

2. **Create a `Procfile` (for Heroku/Railway):**
```
   web: gunicorn app:app
```

3. **Or run manually:**
```bash
   gunicorn --bind 0.0.0.0:5000 app:app
```

### Database Considerations

- **SQLite** works for development and small deployments
- For production with high traffic, consider migrating to **PostgreSQL**
- Some platforms (like Heroku) have ephemeral filesystems - SQLite data may be lost on restart
- For persistent storage, use a managed database service

## Error Handling

The API returns appropriate HTTP status codes and error messages:

### Status Codes

- `200 OK` - Successful GET request
- `201 Created` - Successful POST request (resource created)
- `204 No Content` - Successful DELETE request
- `400 Bad Request` - Invalid request format or parameters
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource already exists
- `422 Unprocessable Entity` - Valid format but invalid data

### Error Response Format
```json
{
  "error": "Description of what went wrong"
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is part of the Backend Wizards Stage 1 Task.

## Author

[Your Name]  
[Your Email]  
[Your GitHub Profile]

## Acknowledgments

- Backend Wizards Program
- Flask Documentation
- SQLAlchemy Documentation