// --- 1. Import Library ที่จำเป็น ---
const logger = require('./logger'); // <--- เพิ่มเข้ามาเป็นอันดับแรก
const express = require('express');
const cors = require('cors');
const path = require('path');
const { GoogleGenerativeAI } = require('@google/generative-ai');
const admin = require("firebase-admin");
require('dotenv').config();

// --- 2. ตั้งค่า Firebase Admin ---
const serviceAccount = require("./firebase-key.json");
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});
const db = admin.firestore();

// --- 3. ตั้งค่าเซิร์ฟเวอร์ Express ---
const app = express();
const PORT = process.env.PORT || 3000;
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// --- 4. ตั้งค่า Gemini AI ---
const apiKey = process.env.GEMINI_API_KEY;
if (!apiKey) {
  // เปลี่ยนมาใช้ logger.error และออกจากโปรแกรม
  logger.error("FATAL: GEMINI_API_KEY is not set in .env file");
  process.exit(1);
}
const genAI = new GoogleGenerativeAI(apiKey);

// สร้างตัวแปรว่างไว้สำหรับเก็บข้อมูลสินค้า
let allProducts = [];

// ฟังก์ชันสำหรับโหลดข้อมูลสินค้าจาก Firestore
async function loadProductsFromFirestore() {
    try {
        // เปลี่ยนมาใช้ logger.info
        logger.info("Attempting to load products from Firestore...");
        const productsCollection = db.collection('products');
        const snapshot = await productsCollection.get();
        if (snapshot.empty) {
            // เปลี่ยนมาใช้ logger.warn
            logger.warn("No products found in the 'products' collection in Firestore.");
            return;
        }
        // แปลงข้อมูลแล้วเก็บในตัวแปร allProducts
        allProducts = snapshot.docs.map(doc => ({
            product_id: doc.id,
            ...doc.data()
        }));
        // เปลี่ยนมาใช้ logger.info พร้อมบอกจำนวนที่โหลดได้
        logger.info(`Successfully loaded ${allProducts.length} products from Firestore.`);
    } catch (error) {
        // เปลี่ยนมาใช้ logger.error พร้อมเก็บข้อมูล error ทั้งหมด
        logger.error("Failed to load products from Firestore", {
          errorMessage: error.message,
          stack: error.stack
        });
    }
}


// --- 5. สร้าง API Endpoints ---

// Endpoint เดิมสำหรับ AI Chat (แก้ไขเล็กน้อย)
app.post('/api/consult', async (req, res) => {
  const { question, element } = req.body;

  if (!question || question.trim() === '') {
    return res.status(400).json({ message: 'กรุณาส่งคำถาม' });
  }
  try {
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash-latest" });
    const productContext = JSON.stringify(allProducts, null, 2);
    
    let prompt = `คุณคือ "incave AI" ผู้เชี่ยวชาญสุขภาพองค์รวมที่เป็นมิตร ข้อมูลผลิตภัณฑ์ทั้งหมดที่มีคือ: ${productContext}.`;
    if (element) {
        prompt += ` ผู้ใช้คนนี้มีพื้นฐานเป็น "ธาตุ${element}" โปรดให้คำแนะนำที่สอดคล้องกับธาตุของเขาด้วย.`;
    }
    prompt += ` ตอบคำถามของผู้ใช้: "${question.trim()}" หากเกี่ยวข้องกับสินค้าให้แนะนำได้ แต่อย่าพยายามวินิจฉัยโรค และแนะนำให้ปรึกษาแพทย์ผู้เชี่ยวชาญเสมอเมื่อเป็นเรื่องที่เกี่ยวข้องกับอาการเจ็บป่วย`;

    const result = await model.generateContent(prompt);
    const response = await result.response;
    res.json({ answer: response.text() });
  } catch (error) {
    // เปลี่ยนมาใช้ logger.error
    logger.error("Error processing /api/consult", {
      errorMessage: error.message,
      stack: error.stack,
      requestBody: req.body // บันทึกข้อมูลที่ส่งมาด้วย (ยกเว้นข้อมูลส่วนตัว)
    });
    res.status(500).json({ answer: 'ขออภัยค่ะ ระบบไม่สามารถประมวลผลได้ในขณะนี้' });
  }
});

// Endpoint เดิมสำหรับค้นหาธาตุ (ไม่มีการแก้ไข)
app.post('/api/find-element', (req, res) => {
    const { birthdate } = req.body;
    if (!birthdate) {
        return res.status(400).json({ message: 'กรุณาส่งวันเกิด' });
    }
    const month = new Date(birthdate).getMonth() + 1;
    let element = '';
    let description = '';
    if ([12, 1, 2].includes(month)) { element = 'ธาตุน้ำ'; description = 'เจ้าแห่งการปรับตัว ไหลลื่นเหมือนสายน้ำ มีความคิดสร้างสรรค์'; }
    else if ([3, 4, 5].includes(month)) { element = 'ธาตุลม'; description = 'นักสื่อสาร มีความคล่องแคล่วว่องไว ชอบการเปลี่ยนแปลง'; }
    else if ([6, 7, 8].includes(month)) { element = 'ธาตุไฟ'; description = 'มีความเป็นผู้นำ มีพลังและความกระตือรือร้นสูง'; }
    else { element = 'ธาตุดิน'; description = 'มีความมั่นคง หนักแน่น เหมือนดั่งปฐพี เป็นที่พึ่งพาได้'; }
    res.json({ element: element, description: description });
});

// --- 6. Error Handlers ---
app.use((req, res, next) => {
  res.status(404).sendFile(path.join(__dirname, 'public', '404.html'));
});

// --- 7. สั่งให้เซิร์ฟเวอร์เริ่มทำงาน ---
app.listen(PORT, () => {
  // เปลี่ยนมาใช้ logger.info
  logger.info(`Server is starting up and listening on port ${PORT}`);
  // เรียกใช้ฟังก์ชันโหลดข้อมูลตอนเซิร์ฟเวอร์เริ่มทำงาน
  loadProductsFromFirestore();
});