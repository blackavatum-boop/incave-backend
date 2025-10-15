import os
import google.generativeai as genai
from dotenv import load_dotenv
import logging

# ตั้งค่าการแสดงผล Log เพื่อให้เห็นข้อมูลละเอียด
logging.basicConfig(level=logging.INFO)

print("--- เริ่มการทดสอบ API ---")

try:
    # 1. โหลด API Key จากไฟล์ .env
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("หา GEMINI_API_KEY ในไฟล์ .env ไม่เจอ!")
    
    print("พบ API Key เรียบร้อย")

    # 2. ตั้งค่า Library ด้วย API Key
    genai.configure(api_key=api_key)
    print("ตั้งค่า Library สำเร็จ")

    # 3. เลือกโมเดล (ตามคำแนะนำในเช็กลิสต์สำหรับ API Key)
    # เราจะใช้ชื่อที่สั้นและเป็นมาตรฐานที่สุด
    model_name = 'gemini-1.5-flash-latest'
    print(f"กำลังจะเรียกใช้โมเดล: '{model_name}'")

    model = genai.GenerativeModel(model_name)

    # 4. ทดลองส่งคำถามง่ายๆ
    print("กำลังส่งคำถาม 'สวัสดี' ไปยัง AI...")
    response = model.generate_content("สวัสดี")

    # 5. แสดงผลลัพธ์
    print("\n--- ✅ ได้รับคำตอบจาก AI สำเร็จ! ---")
    print(response.text)
    print("------------------------------------")

except Exception as e:
    print(f"\n--- ❌ เกิดข้อผิดพลาด! ---")
    print(f"ประเภท Error: {type(e).__name__}")
    print(f"รายละเอียด: {e}")
    print("--------------------------")