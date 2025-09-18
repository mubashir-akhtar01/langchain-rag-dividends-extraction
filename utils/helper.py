import os
import re
import shutil
import json
from fastapi import HTTPException

UPLOAD_DIR = "uploads"

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

def sanitize_filename(file_path):
    """
    Convert file name to a clean document ID
    :param file_path:
    :return sanitized filename:
    """
    file_name = os.path.basename(file_path)
    base_name = os.path.splitext(file_name)[0] # remove pdf extension
    base_name = re.sub(r'[^\w\s-]', '', base_name)  # Remove special characters (^, commas, etc.)
    base_name = base_name.replace(' ', '_') # Replace spaces with underscores
    return base_name.lower() # Convert to lowercase for consistency

def save_file(file):
    """
    Save file to disk
    :param file:
    :return file location:
    """
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)  # Save file to disk
    return file_location

def sanitize_llm_json(data):
    """
    Sanitize json data
    :param data:
    :return json sanitized data:
    """
    fallback = {}

    try:
        # Look for full JSON object or array anywhere in the string
        json_candidates = re.findall(r'(\{.*?\}|\[.*?\])', data, re.DOTALL)

        for candidate in json_candidates:
            try:
                parsed = json.loads(candidate)
                return parsed
            except json.JSONDecodeError:
                continue

        raise HTTPException(status_code=400, detail="No valid JSON found in input")

    except Exception as e:
        print(f"sanitize_llm_json failed: {str(e)}")
        print(f"Raw input:\n{data[:300]}...\n")
        return fallback

def pdf_file_validation(file):

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only pdf files are supported")