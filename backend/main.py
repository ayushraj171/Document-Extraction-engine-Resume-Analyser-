from fastapi import FastAPI, UploadFile, File
import os
import shutil

from backend.extractor import extract_text
from backend.llm_service import extract_structured_data

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Resume Extractor Running"}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # extract text from PDF
    text = extract_text(file_path)

    # Gemini AI processing
    data = extract_structured_data(text)

    return {
        "message": "processed successfully",
        "filename": file.filename,
        "extracted_data": data
    }
