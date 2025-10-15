# C:\MyIncaveProject\backend\main.py
# 🌟 Final Version v7.0: เพิ่ม Debug Endpoint เพื่อพิสูจน์เวอร์ชัน

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import requests 
import json

load_dotenv()

app = FastAPI(
    title="Incave AI Backend",
    description="API สำหรับให้บริการปรึกษาด้วย AI",
    version="7.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("ไม่พบ GEMINI_API_KEY ในไฟล์ .env")

# --- ⭐ โค้ดส่วนที่สำคัญที่สุด ⭐ ---
# กำหนด URL ของโมเดลเวอร์ชันใหม่ล่าสุดไว้ที่นี่
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
MODEL_NAME = "gemini-1.5-flash-latest"
# --------------------------------

class ConsultRequest(BaseModel):
    question: str
    element: Optional[str] = "ไม่ระบุ"

class ConsultResponse(BaseModel):
    answer: str

@app.post("/api/consult", response_model=ConsultResponse)
async def handle_consultation(request: ConsultRequest):
    prompt = f"""
        คุณคือ "Incave AI" ... (ข้อความเหมือนเดิม)
    """
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        response_json = response.json()
        
        if "candidates" in response_json and len(response_json["candidates"]) > 0:
            ai_answer = response_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            ai_answer = "ขออภัยค่ะ AI ไม่สามารถสร้างคำตอบได้ในขณะนี้ โปรดลองอีกครั้ง"
        return ConsultResponse(answer=ai_answer)
    except Exception as e:
        # ... (ส่วนจัดการ Error เหมือนเดิม)
        raise HTTPException(status_code=500, detail=f"เกิดข้อผิดพลาดจาก Google AI API: {str(e)}")

# --- ⭐ เพิ่มโค้ด Debug Endpoint ตามเช็กลิสต์ ⭐ ---
@app.get("/__debug")
def debug():
    return {
        "version": "7.0.0", 
        "model": MODEL_NAME, 
        "api_url_prefix": API_URL.split("?")[0]
    }
# -----------------------------------------------

@app.get("/")
def read_root():
    return {"message": "Incave AI Backend (v7.0.0) is running!"}