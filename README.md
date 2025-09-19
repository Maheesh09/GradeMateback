# GradeMate Backend

This is the FastAPI backend for the GradeMate application, which handles PDF uploads and text extraction for answer sheets.

## Features

- PDF upload and processing
- Text extraction from answer sheets using PyMuPDF
- Question and answer parsing from structured PDFs
- RESTful API endpoints for all operations
- Database integration with SQLAlchemy

## Setup

### Prerequisites

- Python 3.8 or higher
- MySQL database (or compatible)

### Installation

1. **Install dependencies:**
   ```bash
   # Run the installation script
   install_dependencies.bat
   
   # Or manually:
   pip install -r requirements.txt
   ```

2. **Configure database:**
   - Update `app/config.py` with your database credentials
   - Or create a `.env` file with:
     ```
     DB_HOST=127.0.0.1
     DB_PORT=3306
     DB_USER=root
     DB_PASS=password
     DB_NAME=hackathon_db
     ```

3. **Start the server:**
   ```bash
   # Run the startup script
   start_server.bat
   
   # Or manually:
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Endpoints

### Upload Endpoints

- `POST /upload/answer-sheet` - Upload a single answer sheet PDF
- `POST /upload/answer-sheet-batch` - Upload multiple answer sheet PDFs
- `GET /upload/health` - Health check

### Other Endpoints

- `POST /students/` - Create a student
- `GET /students/` - Get all students
- `POST /papers/` - Create a paper
- `GET /papers/` - Get all papers
- `POST /questions/` - Create a question
- `GET /questions/` - Get questions
- `POST /schemes/` - Create a marking scheme
- `GET /schemes/` - Get marking schemes
- `POST /submissions/` - Create a submission
- `GET /submissions/` - Get submissions
- `POST /answers/` - Create an answer
- `GET /answers/` - Get answers

## PDF Processing

The system uses `extractInformation2.py` to process answer sheet PDFs. It expects PDFs with the following format:

```
1.
i. Answer text for part i
ii. Answer text for part ii
iii. Answer text for part iii
2.
i. Answer text for question 2 part i
...
```

The system will extract:
- Raw text from the PDF
- Structured questions and answers
- Question numbers and sub-parts

## Development

The backend uses:
- FastAPI for the web framework
- SQLAlchemy for database ORM
- PyMuPDF (fitz) for PDF processing
- Pydantic for data validation

## Testing

You can test the API using the interactive docs at `http://localhost:8000/docs` when the server is running.
