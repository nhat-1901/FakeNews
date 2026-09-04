# 🛡️ HƯỚNG DẪN CÀI ĐẶT & CHẠY WEB APP DEMO

Tài liệu này hướng dẫn chi tiết cách khởi chạy và kiểm thử hệ thống phát hiện tin giả & tin nhắn lừa đảo bằng mô hình PhoBERT qua giao diện Web tương tác.

---

## 🏗️ Kiến Trúc Hệ Thống

Hệ thống được thiết kế theo mô hình phân tách 2 lớp:
1. **Backend Server (FastAPI):** Tiếp nhận yêu cầu HTTP POST, tiền xử lý văn bản (chuẩn hóa Unicode NFC, làm sạch, tách từ VnCoreNLP), nạp mô hình PhoBERT và thực hiện suy luận nhị phân trong $< 0.5$ giây.
2. **Frontend UI (Streamlit):** Cung cấp giao diện trực quan cho người dùng nhập liệu, hiển thị nhãn dự đoán (**An toàn / Độc hại**) kèm thanh % độ tin cậy và bảng chi tiết xác suất.

---

## 🚀 Các Bước Khởi Chạy

### Bước 1: Cài đặt các thư viện cần thiết
Mở Terminal / Command Prompt và chạy lệnh:
```bash
pip install -r requirements.txt
```

---

### Bước 2: Khởi động Backend API (FastAPI)
Mở cửa sổ **Terminal 1**:
```bash
python -m uvicorn backend_main:app --reload --port 8000
```
* **Địa chỉ API:** `http://localhost:8000`
* **Tài liệu Swagger API tương tác:** `http://localhost:8000/docs`

---

### Bước 3: Khởi động Giao diện Web (Streamlit)
Mở thêm một cửa sổ **Terminal 2**:
```bash
python -m streamlit run frontend_app.py
```
* Hệ thống sẽ tự động mở trình duyệt web tại địa chỉ: `http://localhost:8501`

---
