# Database Setup Guide

This guide explains how to set up and use the MySQL database with your GradeMate application.

## Database Schema

The application uses three main tables:

### 1. `pdfs` Table
- `pdf_id`: Primary key (auto-increment)
- `pdf_name`: Unique name of the PDF file
- `uploaded_at`: Timestamp when the PDF was uploaded

### 2. `questions` Table
- `question_id`: Primary key (auto-increment)
- `pdf_id`: Foreign key to pdfs table
- `main_no`: Main question number (1, 2, 3, etc.)
- `created_at`: Timestamp when the question was created

### 3. `answers` Table
- `answer_id`: Primary key (auto-increment)
- `question_id`: Foreign key to questions table
- `roman_text`: Roman numeral text (i, ii, iii, etc.)
- `part_no`: Numeric part number (1 for i, 2 for ii, etc.)
- `answer_text`: The actual answer text
- `created_at`: Timestamp when the answer was created

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create MySQL Database

Connect to your MySQL server and create the database:

```sql
CREATE DATABASE grademate;
```

### 3. Configure Database Connection

Create a `.env` file in the Backend directory with your database configuration:

```env
# Database Configuration
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=grademate
DATABASE_USER=your_username
DATABASE_PASSWORD=your_password

# Environment
ENVIRONMENT=development
```

### 4. Run Database Setup

```bash
python setup_database.py
```

This will create all the necessary tables with proper constraints and relationships.

## API Endpoints

### Upload Endpoints

- `POST /upload/answer-sheet` - Upload a single PDF
- `POST /upload/answer-sheet-batch` - Upload multiple PDFs
- `GET /upload/health` - Health check for upload service

### Data Retrieval Endpoints

- `GET /data/pdfs` - Get all PDFs (with pagination)
- `GET /data/pdfs/{pdf_id}` - Get a specific PDF with questions and answers
- `DELETE /data/pdfs/{pdf_id}` - Delete a PDF and all its data
- `GET /data/pdfs/{pdf_id}/questions` - Get all questions for a PDF
- `GET /data/questions/{question_id}` - Get a specific question with answers
- `DELETE /data/questions/{question_id}` - Delete a question and its answers
- `GET /data/questions/{question_id}/answers` - Get all answers for a question
- `GET /data/answers/{answer_id}` - Get a specific answer
- `DELETE /data/answers/{answer_id}` - Delete an answer
- `GET /data/search/pdf?name={pdf_name}` - Search for a PDF by name

## Data Flow

1. **Upload PDF**: When you upload a PDF, the system:
   - Extracts text from the PDF
   - Parses questions and answers
   - Saves the data to the database
   - Returns the extracted data and PDF ID

2. **Data Storage**: The parsed data is stored as:
   - One record in `pdfs` table
   - One record in `questions` table for each main question
   - One record in `answers` table for each Roman numeral subpart

3. **Data Retrieval**: You can retrieve data using the API endpoints to:
   - Get all PDFs
   - Get specific PDFs with all questions and answers
   - Get questions for a specific PDF
   - Get answers for a specific question

## Example Usage

### Upload a PDF
```bash
curl -X POST "http://localhost:8000/upload/answer-sheet" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample.pdf"
```

### Get all PDFs
```bash
curl -X GET "http://localhost:8000/data/pdfs"
```

### Get a specific PDF with all data
```bash
curl -X GET "http://localhost:8000/data/pdfs/1"
```

## Database Constraints

The database includes several constraints to ensure data integrity:

- **Unique constraints**: PDF names must be unique, question numbers must be unique per PDF
- **Foreign key constraints**: Proper relationships between tables with cascade delete
- **Check constraints**: Roman numerals must be valid (i-xx), part numbers must be 1-50
- **Data validation**: All required fields must be provided

## Troubleshooting

### Connection Issues
- Ensure MySQL is running
- Check database credentials in `.env` file
- Verify the database exists
- Check firewall settings

### Table Creation Issues
- Ensure the database user has CREATE TABLE permissions
- Check for existing tables that might conflict
- Review error logs for specific constraint violations

### Data Issues
- Check that Roman numerals are valid (i, ii, iii, etc.)
- Ensure question numbers are positive integers
- Verify answer text is not empty

## Development vs Production

### Development
- Set `ENVIRONMENT=development` in `.env`
- SQL queries are logged to console
- More verbose error messages

### Production
- Set `ENVIRONMENT=production` in `.env`
- SQL queries are not logged
- Optimized for performance
- Use connection pooling for better performance
