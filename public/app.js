// รอให้หน้าเว็บโหลดเสร็จก่อน แล้วค่อยเริ่มทำงาน
document.addEventListener('DOMContentLoaded', () => {

    const productListDiv = document.getElementById('product-list');

    // ใช้ fetch เพื่อ "คุย" กับ API ที่เราสร้างไว้
    fetch('http://localhost:3000/api/products')
        .then(response => response.json()) // แปลงข้อมูลที่ได้กลับมาเป็น JSON
        .then(products => {
            // เมื่อได้ข้อมูลสินค้ามาแล้ว (ในตัวแปรชื่อ products)
            console.log('ได้รับข้อมูลสินค้าแล้ว:', products);

            // วนลูปเพื่อสร้างการ์ดสินค้าทีละชิ้น
            products.forEach(product => {
                // สร้าง div สำหรับการ์ดสินค้า
                const card = document.createElement('div');
                card.className = 'product-card';

                // กำหนดเนื้อหาข้างใน (HTML) ให้กับการ์ด
                card.innerHTML = `
                    <img src="${product.image_url}" alt="${product.name}">
                    <h3>${product.name}</h3>
                    <p>ราคา: ${product.price ? product.price + ' บาท' : 'เริ่มต้น ' + product.variants[0].price + ' บาท'}</p>
                    <button>ดูรายละเอียด</button>
                `;

                // นำการ์ดที่สร้างเสร็จแล้วไปแปะในหน้าเว็บ
                productListDiv.appendChild(card);
            });
        })
        .catch(error => {
            // หากเกิดข้อผิดพลาดในการเชื่อมต่อ
            console.error('เกิดข้อผิดพลาด:', error);
            productListDiv.innerHTML = '<p>ไม่สามารถโหลดข้อมูลสินค้าได้ โปรดลองอีกครั้ง</p>';
        });
});