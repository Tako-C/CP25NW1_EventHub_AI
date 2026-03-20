# ใช้ Python Image ที่มีขนาดเล็ก (Alpine หรือ Slim)
FROM python:3.11-slim

# ตั้งค่า Working Directory ใน Container
WORKDIR /app

# ป้องกันไม่ให้ Python สร้างไฟล์ .pyc และให้ Output แสดงผลทันที
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# ติดตั้ง dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดทั้งหมดเข้าไปใน Container
COPY . .

# สั่งรัน FastAPI ด้วย Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
