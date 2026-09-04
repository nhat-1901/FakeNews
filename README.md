# 🛡️ Hệ Thống Phát Hiện Tin Giả & Tin Nhắn Lừa Đảo Bằng PhoBERT

Dự án ứng dụng mô hình học sâu **PhoBERT** (fine-tuned) kết hợp với **FastAPI** (Backend) và **Streamlit** (Frontend) để phân loại và phát hiện tin tức giả mạo, tin nhắn lừa đảo trên mạng xã hội tiếng Việt theo thời gian thực.

---

## 📌 Tính Năng Chính
- **Phân loại nhị phân chính xác cao:** Phân biệt văn bản An toàn (Nhãn 0) và Độc hại/Lừa đảo (Nhãn 1).
- **Đọc hiểu ngữ cảnh tiếng Việt:** Xử lý tốt rào cản từ ghép, teencode, cố tình viết sai chính tả.
- **Kiến trúc phân tách:** Backend RESTful API (FastAPI) và Giao diện Web trực quan (Streamlit).

---

## 📂 Cấu Trúc Thư Mục

`
FakeNewApp/
│
├── backend_main.py          # FastAPI RESTful API server
├── frontend_app.py         # Streamlit Web UI
├── requirements.txt        # Danh sách các thư viện cần thiết
├── .gitignore              # Cấu hình bỏ qua file nặng/file rác khi push Git
├── README.md               # Tài liệu hướng dẫn dự án
│
└── phobert_fakenews_final/ # Thư mục chứa trọng số mô hình PhoBERT đã fine-tune
    ├── config.json
    ├── tokenizer_config.json
    ├── vocab.txt
    ├── bpe.codes
    └── model.safetensors   # Trọng số mô hình (~540MB)
`

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Ứng Dụng

### 1. Cài đặt môi trường & thư viện
`ash
pip install -r requirements.txt
`

### 2. Khởi động Backend Server (FastAPI)
Mở cửa sổ Terminal 1:
`ash
uvicorn backend_main:app --reload --port 8000
`
- API chạy tại: http://localhost:8000
- Tài liệu API tương tác (Swagger UI): http://localhost:8000/docs

### 3. Khởi động Giao diện Web (Streamlit)
Mở cửa sổ Terminal 2:
`ash
streamlit run frontend_app.py
`
- Ứng dụng Web tự động mở tại: http://localhost:8501

---

## 👨‍💻 Tác Giả
- **Sinh viên:** Nguyễn Đức Nhật
- **Giảng viên hướng dẫn:** Thầy Phạm Đình Tài
- **Khoa Công nghệ Thông tin - Trường Đại học Nguyễn Tất Thành**
