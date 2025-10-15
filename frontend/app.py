# C:\incave\app.py
import streamlit as st

st.set_page_config(layout="wide")

st.title("ถ้ำมนุษย์ AI: ค้นหาธาตุเจ้าเรือนของคุณ 🌿")
st.write("กลับสู่พื้นฐานแห่งธรรมชาติ เพื่อเข้าใจร่างกายของคุณอย่างแท้จริง")

# --- โค้ดสำหรับเพิ่มลิงก์ไปหน้าแชทโดยตรง ---
st.page_link("pages/consult_ai.py", label="หรือ คลิกที่นี่เพื่อปรึกษา AI โดยตรง", icon="💬")
st.markdown("---") 
# ------------------------------------------

@st.cache_data
def get_quiz_data():
    questions = [
        {"question": "1. ลักษณะรูปร่างโดยรวมของคุณ", "options": {"A": "ผอม แห้ง กล้ามเนื้อไม่แน่น", "B": "สมส่วน แข็งแรง มีกล้ามเนื้อ", "C": "อ้วนง่าย ตัวใหญ่ หนักแน่น", "D": "ผิวแดง ขี้ร้อน มีเหงื่อบ่อย"}},
        {"question": "2. พฤติกรรมการกินของคุณ", "options": {"A": "ชอบอาหารรสจัด เผ็ด เค็ม", "B": "กินง่าย อยู่ง่าย ไม่เลือกมาก", "C": "ชอบอาหารมัน หวาน แป้ง", "D": "หิวบ่อย ถ้าไม่กินจะหงุดหงิด"}},
        {"question": "3. ลักษณะการนอน", "options": {"A": "หลับยาก หลับไม่ลึก", "B": "นอนนาน ตื่นยาก", "C": "ง่วงง่าย นอนบ่อย", "D": "ตื่นกลางดึก รู้สึกร้อน"}},
        {"question": "4. ความชอบต่ออากาศ", "options": {"A": "ชอบลมพัด อากาศถ่ายเท", "B": "ชอบเย็นสบาย ไม่ร้อนไม่หนาว", "C": "แพ้ความเย็น หนาวง่าย", "D": "ร้อนบ่อย เหงื่อออกง่าย"}},
        {"question": "5. การเคลื่อนไหว", "options": {"A": "เคลื่อนไหวไว ชอบเดินเร็ว", "B": "ช้าแต่มั่นคง ไม่รีบร้อน", "C": "ขี้เกียจ เคลื่อนไหว้น้อย", "D": "กระสับกระส่าย ขยันแต่หงุดหงิด"}},
        {"question": "6. สภาพจิตใจ/อารมณ์", "options": {"A": "คิดมาก หวั่นไหวง่าย", "B": "มั่นคง เยือกเย็น ใจดี", "C": "อ่อนไหว ขี้น้อยใจ", "D": "ขี้หงุดหงิด อารมณ์ร้อน"}},
        {"question": "7. อาการเจ็บป่วยที่เกิดบ่อย", "options": {"A": "ปวดเมื่อย ลมในตัวเยอะ", "B": "ปวดกล้ามเนื้อหนักๆ", "C": "บวมน้ำ ปัสสาวะบ่อย", "D": "เป็นไข้ ตัวร้อน ปวดหัวบ่อย"}}
    ]
    element_map = {'A': 'ลม', 'B': 'ดิน', 'C': 'น้ำ', 'D': 'ไฟ'}
    results_guide = {
        'ลม': {'description': 'พลังแห่งการเคลื่อนไหว ร่างกายไว อ่อนไหวง่าย ความคิดเยอะ', 'behavior': 'ควรทำสมาธิ เดินป่า หรือฟังเสียงธรรมชาติ', 'herbs': 'เช่น ขิง, พริกไทย, กระชาย'},
        'ดิน': {'description': 'พลังแห่งความมั่นคง แข็งแรง ทนทาน แต่เคลื่อนไหวช้า', 'behavior': 'ควรออกกำลังกายแบบกระตุ้น เช่น วิ่งจ็อกกิ้ง', 'herbs': 'เช่น ใบย่านาง, มะรุม'},
        'น้ำ': {'description': 'พลังแห่งการหล่อเลี้ยง มีอารมณ์อ่อนไหวง่วงง่าย', 'behavior': 'ควรตื่นเช้ารับแดด เดินริมแม่น้ำ', 'herbs': 'เช่น ตะไคร้, บัวบก, กระเจี๊ยบ'},
        'ไฟ': {'description': 'พลังแห่งการเผาผลาญ เร่าร้อน มีพลังสูง แต่หงุดหงิดง่าย', 'behavior': 'ควรหลีกเลี่ยงแดดจัด ฝึกสมาธิ', 'herbs': 'เช่น ฟ้าทะลายโจร, รางจืด, แตงกวา'}
    }
    return questions, element_map, results_guide

def analyze_and_display_results(scores, results_guide):
    if not scores: return
    max_score = max(scores.values())
    top_elements = [element for element, score in scores.items() if score == max_score]
    st.balloons()
    st.header("🧾 ผลลัพธ์ของคุณ:")
    primary_element = top_elements[0]
    result = results_guide[primary_element]
    st.subheader(f"🔹 คุณมี “ธาตุประจำเจ้าเรือน” คือ: {primary_element}")
    st.markdown("---")
    st.markdown(f"### 💡 คำแนะนำสำหรับธาตุ {primary_element}:")
    st.markdown(f"**ลักษณะ:** {result['description']}")
    st.markdown(f"**พฤติกรรม:** {result['behavior']}")
    st.markdown(f"**สมุนไพร:** {result['herbs']}")
    st.session_state['user_element'] = primary_element
    st.markdown("---")
    st.info("ต้องการคำแนะนำที่เหมาะกับคุณโดยเฉพาะหรือไม่?")
    st.page_link("pages/consult_ai.py", label=f"คุยกับ AI เพื่อรับคำแนะนำสำหรับธาตุ {primary_element} ต่อ", icon="💬")

questions, element_map, results_guide = get_quiz_data()

with st.form("quiz_form"):
    user_answers = []
    st.info("กรุณาเลือกคำตอบที่ตรงกับคุณมากที่สุดในแต่ละข้อ")
    for i, q_data in enumerate(questions):
        st.subheader(f"❓ {q_data['question']}")
        answer = st.radio("เลือกคำตอบ:", options=q_data['options'].keys(), format_func=lambda key: f"{key}: {q_data['options'][key]}", key=f"q{i}", label_visibility="collapsed")
        user_answers.append(answer)
    submitted = st.form_submit_button("วิเคราะห์ผลลัพธ์")

if submitted:
    scores = {'ลม': 0, 'ดิน': 0, 'น้ำ': 0, 'ไฟ': 0}
    for answer_key in user_answers:
        element = element_map[answer_key]
        scores[element] += 1
    analyze_and_display_results(scores, results_guide)