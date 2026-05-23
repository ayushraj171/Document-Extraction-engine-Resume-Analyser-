from fastapi import FastAPI, UploadFile, File
import os
import shutil

from extractor import extract_text
from llm_service import extract_structured_data

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Resume Extractor Running 🚀"}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(file_path)

    data = extract_structured_data(text)

    return {
        "message": "processed successfully",
        "filename": file.filename,
        "extracted_data": data
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))

    uvicorn.run(app, host="0.0.0.0", port=port)
