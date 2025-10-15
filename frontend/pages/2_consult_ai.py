# C:\MyIncaveProject\frontend\pages\2_consult_ai.py
import os
import streamlit as st
import requests

st.title("🤖 ปรึกษาผู้เชี่ยวชาญ AI")
st.write("พิมพ์คำถามเกี่ยวกับสุขภาพหรือผลิตภัณฑ์ของเราได้เลย")

# ✅ อ่านจาก ENV (สำหรับโปรดักชันบน Render) ถ้าไม่ตั้ง ใช้ค่า local สำหรับทดสอบ
SERVER_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api/consult")

# แสดงข้อมูลธาตุ ถ้ามี
if 'user_element' in st.session_state:
    st.info(f"AI พร้อมให้คำปรึกษาสำหรับ **ธาตุ{st.session_state['user_element']}** ของคุณแล้วค่ะ")

# ประวัติแชท
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "สวัสดีค่ะ มีอะไรให้ Incave AI ช่วยเหลือไหมคะ?"}
    ]

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("ถามอะไรดี?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.spinner('AI กำลังคิด...'):
            payload = {"question": prompt}
            if 'user_element' in st.session_state:
                payload["element"] = st.session_state["user_element"]

            r = requests.post(SERVER_URL, json=payload, timeout=30)
            if r.status_code == 200:
                data = r.json()
                ai_answer = data.get("answer", "ขออภัยค่ะ ไม่พบคำตอบจาก AI")
            else:
                ai_answer = f"ขออภัยค่ะ เซิร์ฟเวอร์ตอบผิดพลาด: {r.text}"
    except requests.exceptions.RequestException as e:
        ai_answer = f"เชื่อมต่อ Backend ไม่ได้: {e}"
    except Exception as e:
        ai_answer = f"ขออภัยค่ะ เกิดข้อผิดพลาดที่ไม่คาดคิด: {e}"

    st.session_state.messages.append({"role": "assistant", "content": ai_answer})
    with st.chat_message("assistant"):
        st.markdown(ai_answer)
