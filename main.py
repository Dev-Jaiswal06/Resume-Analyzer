from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import io
from utils import extract_keywords, rate_resume
from transformers import pipeline

app = FastAPI()

# Allow frontend (React) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Summarizer model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

@app.post("/upload_resume/")
async def upload_resume(file: UploadFile):
    content = await file.read()
    text = ""
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    keywords = extract_keywords(text)
    score = rate_resume(text)
    summary = summarizer(text[:1000], max_length=50, min_length=10, do_sample=False)

    return {
        "extracted_text": text[:500],   # first 500 chars only
        "keywords": keywords,
        "resume_score": score,
        "summary": summary[0]["summary_text"]
    }
