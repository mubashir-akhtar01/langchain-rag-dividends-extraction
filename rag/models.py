from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
import os

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

class Models:
    def __init__(self):
        # Google's Embeddings
        self.embeddings_google = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

        # Google's Gemini Model
        self.model_google = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)