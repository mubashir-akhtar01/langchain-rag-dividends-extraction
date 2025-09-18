from fastapi import APIRouter, HTTPException, UploadFile
from starlette import status
#from rag import vector_store, chat, ingest
#from custom_prompts import dividends as custom_prompts
from utils import helper
import json
import re
import pymupdf as fitz  # PyMuPDF
import google.generativeai as genai

router = APIRouter()

@router.post('/dividends/{cik}', status_code=status.HTTP_200_OK)
async def dividends(cik, file: UploadFile | None = None):

    helper.pdf_file_validation(file)
    file_location = helper.save_file(file)

    keywords = [
        "Subsequent Events",
        "Recent Developments",
        "Distributions and Distribution",
        "Dividend Reinvestment",
        "Distribution Declarations",
        "Distributions"
    ]

    extracted_data = extract_sections_by_keywords(file_location, keywords)
    llm = genai.GenerativeModel('gemini-2.0-flash')

    results = []
    for section_name, content in extracted_data.items():
        prompt = f"""
                From the following text in the section titled '{section_name}' extract  the relevant data and return in JSON format with the following keys:
                "dividend_price" (float)
                "declaration_date" (string or null, format: 'YYYY-MM-DD')
                "record_date" (string, format: 'YYYY-MM-DD', required)
                "payment_date" (string, format: 'YYYY-MM-DD', required)
                "ex_date" (string, format: 'YYYY-MM-DD', required)
                "class" (string, None, format: 'Class A')
                "dividend_type" (string, default: 'regular')

                Ensure that:
                1. ex_date will be one day less from record_date
                2. Ensure **correct mapping of declaration, payment, and record dates**.
                3. for dividend_type there are two possibilities either it is regular or it is special and following are the cases to identify special
                    a. you can find either some notes in the data like "special distribution or additional or supplemental" or you can find some special character in declaration date 
                    b. you can find more than one records with same record date
                    c. there may be unusual difference in the amounts of previous records, when the amount is unusually change than its special 
                4. if more than one class having same record_date, payment_date, declaration_date and dividend_price so create 2 datasets of each class
                """

        prompt += f"\n\nText:\n{content}\n\nJSON Output:"
        try:
            response = llm.generate_content(prompt)
            json_output = response.text.strip()
            try:
                parsed_data = helper.sanitize_llm_json(json_output)
                results.append(parsed_data)
            except json.JSONDecodeError:
                print(f"Error decoding JSON for section '{section_name}': {json_output}")
                raise HTTPException(status_code=400, detail="Error decoding JSON")
            except ValueError as ve:
                print(f"Error formatting date for section '{section_name}': {ve}")
                raise HTTPException(status_code=400, detail="Error formatting date")

        except Exception as e:
            print(f"Error processing section '{section_name}': {e}")
            raise HTTPException(status_code=400, detail=f"Error processing section '{section_name}': {e}")

    print(results)
    data = sanitize_dividends_data(results)
    return {"data": data}

def extract_sections_by_keywords(pdf_path, keywords):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    # Normalize the whitespace
    normalized_text = re.sub(r'\s+', ' ', full_text).strip()

    results = {}

    for keyword in keywords:
        # Search for keyword case-insensitively
        match = re.search(re.escape(keyword), normalized_text, re.IGNORECASE)
        if match:
            start_index = match.start()
            chunk_text = normalized_text[start_index:]
            words = chunk_text.split()
            section_words = words[:1000]
            results[keyword] = " ".join(section_words)

    page_numbers = []

    required_columns = ["Payment Date", "Declaration Date"]

    for page_num, page in enumerate(doc, start=1):
        try:
            text = page.get_text()
            if text:
                if all(re.search(re.escape(k), text, re.IGNORECASE) for k in required_columns):
                    page_numbers.append(page_num)

        except Exception as e:
            print(f"Skipped page {page_num} due to error: {e}")

    if page_numbers:
        text = ""
        for page_number in page_numbers:
            data = doc.load_page(page_number-1)
            text += data.get_text()

        if text:
            normalized_text = re.sub(r'\s+', ' ', text).strip()
            results["Tables Data"] = normalized_text

    return results

def is_probable_heading(line):
    # Heuristics: short, no punctuation, capitalized, etc.
    return (
            3 < len(line.strip()) <= 30
            and len(line.strip().split()) <= 3
            and line.strip()[0].isupper()
            and not line.strip().endswith(('.', ':'))
    )

def sanitize_dividends_data(json_data):

    # check if the json data have nested list
    merged_list = []
    for item in json_data:
        if isinstance(item, dict):
            merged_list.append(item)
        elif isinstance(item, list):
            merged_list.extend(item)

    # remove records which have no declaration_date
    data = [item for item in merged_list if item.get("declaration_date") is not None]

    data = [item for item in data if item.get("dividend_price") is not None]

    # remove duplicates records
    unique_data = [dict(t) for t in {tuple(sorted(d.items())) for d in data}]
    return unique_data