# C:\MyIncaveProject\backend\main.py
# 🌟 Final Version: ใช้ requests เรียก API โดยตรงเพื่อแก้ปัญหา v1beta

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import requests 
import json

# โหลดค่าจากไฟล์ .env
load_dotenv()

# --- 1. ตั้งค่า FastAPI App ---
app = FastAPI(
    title="Incave AI Backend",
    description="API สำหรับให้บริการปรึกษาด้วย AI",
    version="5.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. ดึง API Key ---
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("ไม่พบ GEMINI_API_KEY ในไฟล์ .env")

# --- 3. Pydantic Models ---
class ConsultRequest(BaseModel):
    question: str
    element: Optional[str] = "ไม่ระบุ"

class ConsultResponse(BaseModel):
    answer: str

# --- 4. API Endpoint ---
@app.post("/api/consult", response_model=ConsultResponse)
async def handle_consultation(request: ConsultRequest):
    
    # ใช้ URL ที่เป็นเวอร์ชัน v1 และโมเดล gemini-pro ที่เป็นมาตรฐาน
    api_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"
    
    prompt = f"""
        คุณคือ "Incave AI" ผู้เชี่ยวชาญด้านสุขภาพองค์รวมและการแพทย์แผนไทย
        ผู้ใช้กำลังถามคำถามเกี่ยวกับสุขภาพ: "{request.question}"
        ข้อมูลเพิ่มเติม: ธาตุเจ้าเรือนคือ "{request.element}"
        โปรดให้คำตอบที่เป็นประโยชน์ สุภาพ และแนะนำผลิตภัณฑ์ของ Incave ถ้าเป็นไปได้
    """
    
    headers = {"Content-Type": "application/json"}
    
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }

    try:
        # ยิง Request ไปที่ Google API โดยตรง
        response = requests.post(api_url, headers=headers, data=json.dumps(data))
        response.raise_for_status() # ตรวจสอบว่ามี HTTP Error หรือไม่

        response_json = response.json()
        
        # ตรวจสอบว่ามีคำตอบกลับมาจริงหรือไม่ ก่อนที่จะดึงข้อมูล
        if "candidates" in response_json and len(response_json["candidates"]) > 0:
            ai_answer = response_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            ai_answer = "ขออภัยค่ะ AI ไม่สามารถสร้างคำตอบได้ในขณะนี้"

        return ConsultResponse(answer=ai_answer)
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response body: {response.text}")
        raise HTTPException(status_code=response.status_code, detail=f"เกิดข้อผิดพลาดจาก Google AI API: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- 5. Endpoint พื้นฐาน ---
@app.get("/")
def read_root():
    return {"message": "Incave AI Backend (v5.0) is running!"}