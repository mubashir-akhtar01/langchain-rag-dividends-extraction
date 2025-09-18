from fastapi.responses import FileResponse
from fastapi import FastAPI
from routers import dividends
from dotenv import load_dotenv

app = FastAPI()
app.include_router(dividends.router)
load_dotenv()

@app.get("/")
async def root():
    return {"message": "Welcome to RAG Application"}

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("public/assets/ico/favicon.ico")