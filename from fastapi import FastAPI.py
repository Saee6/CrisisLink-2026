from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import json
import os

app = FastAPI(title="CrisisLink AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


GEMINI_KEY = os.environ.get("GEMINI_KEY", "AIzaSyA6hM3FH3TvxW7SrjJvPtTGEtlnh1omFUg")
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

class EmergencyInput(BaseModel):
    type: str
    room: str
    description: str

@app.get("/")
def root():
    return {"status": "CrisisLink API running", "version": "1.5"}

@app.post("/classify")
async def classify_emergency(data: EmergencyInput):
    prompt = f"""You are an AI emergency coordinator for a hotel.
Classify this emergency. Return ONLY valid JSON, no markdown.

Emergency type: {data.type}
Location: {data.room}
Description: {data.description}

Return exactly this structure:
{{
  "severity": "critical",
  "category": "Fire",
  "protocol": "Step 1: Evacuate all guests from the affected floor\\nStep 2: Call fire department 101 with exact location\\nStep 3: Activate fire alarm manually if not triggered\\nStep 4: Account for all guests at assembly point",
  "brief": "Fire emergency at {data.room}. Evacuation in progress."
}}

Rules:
severity: critical, high, or medium
category: single word
protocol: exactly 4 steps starting with Step N:
brief: one sentence for emergency services"""
