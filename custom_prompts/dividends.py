from langchain_core.prompts import PromptTemplate


def dividends_prompt():
    """"
    Returns a custom prompt template with system instructions.
    """
    template = """
    Extract Subsequent Events, Dividend Reinvestment paragraphs to find the relevant data and return in JSON format with the following keys:
    "dividend_price" (float)
    "declaration_date" (string or null, format: 'Month DD, YYYY')
    "record_date" (string, format: 'Month DD, YYYY', required)
    "payment_date" (string, format: 'Month DD, YYYY', required)
    "ex_date" (string, format: 'Month DD, YYYY', required)
    
    Ensure that:
    1. ex_date will be one day less from record_date
    2. Ensure **correct mapping of declaration, payment, and record dates**.
    
    Context: {context}
    Question: {question}
    Answer:
    """

    return PromptTemplate(template=template, input_variables=["context", "question"])