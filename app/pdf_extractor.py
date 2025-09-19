import fitz  # PyMuPDF
import re
from typing import Dict, Any

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from PDF file using PyMuPDF
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text += page.get_text()
            if page_num < len(doc) - 1:  # Add newline between pages
                text += "\n"
        
        doc.close()
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def parse_questions_from_text(text: str) -> Dict[str, Dict[str, str]]:
    """
    Parse questions and answers from extracted text
    Expected format:
    1.
    i. Answer text for part i
    ii. Answer text for part ii
    2.
    i. Answer text for question 2 part i
    """
    lines = text.split('\n')
    questions = {}
    current_question = None
    current_part = None
    current_text = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for question number (e.g., "1.", "2.", etc.)
        question_match = re.match(r'^(\d+)\.\s*$', line)
        if question_match:
            # Save previous question if exists
            if current_question and current_part:
                questions[current_question][current_part] = '\n'.join(current_text).strip()
            
            # Start new question
            current_question = question_match.group(1)
            questions[current_question] = {}
            current_part = None
            current_text = []
            continue
        
        # Check for part (e.g., "i.", "ii.", "iii.", etc.)
        part_match = re.match(r'^([ivxlcdm]+)\.\s*(.*)$', line, re.IGNORECASE)
        if part_match:
            # Save previous part if exists
            if current_question and current_part:
                questions[current_question][current_part] = '\n'.join(current_text).strip()
            
            # Start new part
            current_part = part_match.group(1).lower()
            current_text = [part_match.group(2)] if part_match.group(2).strip() else []
            continue
        
        # Regular text line - add to current part
        if current_question and current_part is not None:
            current_text.append(line)
    
    # Save last part
    if current_question and current_part:
        questions[current_question][current_part] = '\n'.join(current_text).strip()
    
    return questions

def process_pdf(pdf_path: str) -> Dict[str, Any]:
    """
    Main function to process PDF and extract questions/answers
    """
    try:
        # Extract text from PDF
        extracted_text = extract_text_from_pdf(pdf_path)
        
        # Parse questions and answers
        parsed_questions = parse_questions_from_text(extracted_text)
        
        return {
            "success": True,
            "extracted_text": extracted_text,
            "parsed_questions": parsed_questions,
            "question_count": len(parsed_questions)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "extracted_text": "",
            "parsed_questions": {},
            "question_count": 0
        }
