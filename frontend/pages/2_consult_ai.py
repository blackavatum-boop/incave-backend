# C:\my-incave-project\frontend\pages\2_consult_ai.py
import streamlit as st
import requests

st.title("🤖 ปรึกษาผู้เชี่ยวชาญ AI")
st.write("พิมพ์คำถามเกี่ยวกับสุขภาพหรือผลิตภัณฑ์ของเราได้เลย")

# ⭐ URL ที่ถูกต้อง ชี้ไปที่ Backend Service ใหม่บน Render
SERVER_URL = "https://incave-backend-python.onrender.com/api/consult"

# แสดงธาตุของผู้ใช้ ถ้ามีข้อมูล
if 'user_element' in st.session_state:
    element = st.session_state['user_element']
    st.info(f"AI พร้อมให้คำปรึกษาสำหรับ **ธาตุ{element}** ของคุณแล้วค่ะ")

# Khởi tạo lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "สวัสดีค่ะ มีอะไรให้ Incave AI ช่วยเหลือไหมคะ?"}
    ]

# แสดงข้อความแชทเก่า
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# รับ Input ใหม่จากผู้ใช้
if prompt := st.chat_input("ถามอะไรดี?"):
    # แสดงข้อความใหม่ของผู้ใช้
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ส่ง Request ไปยัง Backend และจัดการคำตอบ
    try:
        with st.spinner('AI กำลังคิด...'):
            payload = {"question": prompt}
            if 'user_element' in st.session_state:
                payload['element'] = st.session_state['user_element']

            response = requests.post(SERVER_URL, json=payload)

            # ตรวจสอบว่า Backend ตอบกลับมาสำเร็จหรือไม่
            if response.status_code == 200:
                ai_answer = response.json().get("answer", "ขออภัยค่ะ ไม่ได้รับคำตอบที่ถูกต้อง")
            else:
                # ถ้าเซิร์ฟเวอร์ตอบกลับมาเป็น Error ให้แสดงข้อความ Error นั้น
                ai_answer = f"ขออภัยค่ะ เกิดข้อผิดพลาดจากเซิร์ฟเวอร์: {response.text}"

    except requests.exceptions.RequestException as e:
        ai_answer = f"เชื่อมต่อกับเซิร์ฟเวอร์หลังบ้าน (Backend) ไม่ได้ครับ: {e}"
    except Exception as e:
        ai_answer = f"ขออภัยค่ะ เกิดข้อผิดพลาดที่ไม่คาดคิด: {e}"

    # แสดงคำตอบของ AI
    st.session_state.messages.append({"role": "assistant", "content": ai_answer})
    with st.chat_message("assistant"):
        st.markdown(ai_answer)