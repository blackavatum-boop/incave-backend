// --- 1. Import Library ที่จำเป็น ---
const express = require('express');
const cors = require('cors');
const path = require('path');
const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config(); // <<< เพิ่มเข้ามา: สำหรับโหลดค่าจากไฟล์ .env

// --- 2. ตั้งค่าเซิร์ฟเวอร์ ---
const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// <<< เปลี่ยนแปลงที่ 1: การจัดการ API Key ที่ปลอดภัย ---
const apiKey = process.env.GEMINI_API_KEY;
if (!apiKey) {
  console.error("ข้อผิดพลาด: ไม่ได้ตั้งค่า GEMINI_API_KEY ในไฟล์ .env");
  process.exit(1); // ออกจากโปรแกรมถ้าไม่มี Key
}
const genAI = new GoogleGenerativeAI(apiKey);

// --- 3. ฐานข้อมูลจำลอง ---
const allProducts = [
  { "product_id": "P001", "type": "physical", "name": "Am Good Nano Oil", "description": "น้ำมันสมุนไพรนาโนซึมไว...", "price": 350.00, "image_url": "/images/nano-oil.jpg" },
  { "product_id": "P002", "type": "physical", "name": "Am Good Coffee", "description": "กาแฟสุขภาพหอมเข้ม...", "price": 350.00, "image_url": "/images/coffee.jpg" },
  { "product_id": "P003", "type": "physical", "name": "AM Knock (น้ำมัน CBD)", "description": "น้ำมัน CBD เกรดพรีเมียม...", "price": 1150.00, "image_url": "/images/amknock.jpg" },
  { "product_id": "P004", "type": "physical", "name": "Am Fine", "description": "ผลิตภัณฑ์เสริมอาหารสูตรสมุนไพรระดับโลก...", "price": 900.00, "image_url": "/images/amfine.jpg" },
  { "product_id": "S001", "type": "service", "name": "บริการอบสินแร่ภูเขาไฟญี่ปุ่น", "description": "การบำบัดร่างกายด้วยความร้อน...", "image_url": "/images/sandbath.jpg", "variants": [{ "variant_id": "S001-A", "name": "เดินทางมาเอง", "price": 990.00 }, { "variant_id": "S001-B", "name": "บริการรับ-ส่ง (เฉพาะกรุงเทพฯ)", "price": 1350.00 }] }
];

// --- 4. สร้าง API Endpoints ---
app.get('/api/products', (req, res) => {
  res.json(allProducts);
});

app.get('/api/products/:id', (req, res) => {
  const productId = req.params.id;
  const product = allProducts.find(p => p.product_id === productId);
  if (product) {
    res.json(product);
  } else {
    res.status(404).json({ message: 'ไม่พบสินค้า' });
  }
});

app.post('/api/consult', async (req, res) => {
  const userQuestion = req.body.question;
  if (!userQuestion) {
    return res.status(400).json({ message: 'กรุณาส่งคำถาม' });
  }

  try {
    // <<< เปลี่ยนแปลงที่ 2: อัปเดตชื่อ Model ---
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash-latest" });

    // <<< เปลี่ยนแปลงที่ 3: ปรับปรุง Prompt ให้ฉลาดขึ้น ---
    const productContext = JSON.stringify(allProducts, null, 2);
    const prompt = `
      คุณคือ "incave AI" ผู้เชี่ยวชาญด้านสุขภาพและการดูแลร่างกายที่เป็นมิตรและให้ความช่วยเหลือ
      
      **ข้อมูลผลิตภัณฑ์ที่มีอยู่:**
      ${productContext}

      **หน้าที่ของคุณ:**
      1. ตอบคำถามของผู้ใช้เกี่ยวกับสุขภาพด้วยความห่วงใยและให้ข้อมูลที่เป็นประโยชน์
      2. หากคำถามเกี่ยวข้องกับอาการหรือปัญหาสุขภาพที่สามารถบรรเทาได้ด้วยผลิตภัณฑ์ที่มีอยู่ ให้แนะนำผลิตภัณฑ์ที่เกี่ยวข้อง 1-2 อย่าง พร้อมอธิบายสั้นๆ ว่าเหตุใดจึงเหมาะสม
      3. ห้ามให้คำวินิจฉัยทางการแพทย์เด็ดขาด
      4. ปิดท้ายคำตอบเสมอด้วยการแนะนำให้ปรึกษาแพทย์หรือผู้เชี่ยวชาญเพื่อรับการวินิจฉัยที่ถูกต้อง

      **คำถามจากผู้ใช้:**
      "${userQuestion}"

      โปรดให้คำแนะนำ:
    `;

    const result = await model.generateContent(prompt);
    const response = await result.response;
    const aiResponse = response.text();

    res.json({ answer: aiResponse });

  } catch (error) {
    // <<< เปลี่ยนแปลงที่ 4: เพิ่มการจัดการ Error ที่ดีขึ้น ---
    console.error('เกิดข้อผิดพลาดในการเรียกใช้ Gemini API:', error.message || error);
    res.status(500).json({ answer: 'ขออภัยค่ะ ระบบไม่สามารถประมวลผลคำถามได้ในขณะนี้ กรุณาลองใหม่อีกครั้ง' });
  }
});

app.get('/api/summary', (req, res) => {
  const healthSummary = {
    user_name: "ออม",
    element: "ธาตุดิน",
    health_tips: "ผู้มีธาตุดินควรรักษาสมดุลร่างกายด้วยการรับประทานอาหารรสฝาดและรสขม เช่น มะระ, สะเดา, ฝรั่ง",
    related_products: [
      { product_id: "P002", name: "Am Good Coffee", image_url: "/images/coffee.jpg" },
      { product_id: "P004", name: "Am Fine", image_url: "/images/amfine.jpg" }
    ]
  };
  res.json(healthSummary);
});

// --- 5. สั่งให้เซิร์ฟเวอร์เริ่มทำงาน ---
app.listen(PORT, () => {
  console.log(`เซิร์ฟเวอร์กำลังทำงานที่ http://localhost:${PORT}`);
});