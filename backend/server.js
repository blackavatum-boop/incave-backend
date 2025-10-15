// C:\Users\Aom AMGOOD\OneDrive\Desktop\incave-backend\server.js
// นี่คือโค้ดหลังบ้านที่ถูกต้องและสมบูรณ์

const express = require('express');
const { GoogleGenerativeAI } = require('@google/generative-ai');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(express.json());
app.use(cors());

// ตรวจสอบว่ามี API Key หรือไม่
if (!process.env.GOOGLE_API_KEY) {
  console.error("CRITICAL ERROR: GOOGLE_API_KEY is not defined in your .env file.");
  process.exit(1); // หยุดการทำงานถ้าไม่มี Key
}
const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);

// API Endpoint สำหรับ AI
app.post('/api/consult', async (req, res) => {
  try {
    const { question, element } = req.body;
    if (!question) {
      return res.status(400).json({ error: 'Question is required' });
    }

    // ⭐ แก้ไขชื่อโมเดลเป็น 'gemini-pro' ที่เสถียร
    const model = genAI.getGenerativeModel({ model: 'gemini-pro' });

    const prompt = `You are "Incave AI," an expert in holistic health. A user with the element "${element || 'unknown'}" is asking: "${question}". Provide a helpful and polite answer.`;

    const result = await model.generateContent(prompt);
    const response = await result.response;
    res.json({ answer: response.text() });

  } catch (error) {
    console.error('Error calling Google AI:', error);
    res.status(500).json({ error: 'Failed to get response from AI service.' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`✅ Incave AI Backend (Node.js) is running successfully on port ${PORT}`);
});