# PHÁT HIỆN TIN GIẢ VÀ TIN NHẮN LỪA ĐẢO TIẾNG VIỆT BẰNG PHOBERT

Đây là đồ án chuyên ngành xây dựng hệ thống phát hiện tin giả và tin nhắn lừa đảo trên mạng xã hội tiếng Việt, sử dụng mô hình PhoBERT (fine-tune) làm phương pháp chính, đối chiếu với ba mô hình học máy baseline (Naive Bayes, SVM, LSTM) để đánh giá hiệu quả một cách khách quan.

Bộ dữ liệu thực nghiệm được tổng hợp từ hai nguồn: (1) tập bài đăng mạng xã hội/tin tức đã gán nhãn tin thật – tin giả, và (2) tập tin nhắn mô phỏng các kịch bản lừa đảo phổ biến tại Việt Nam (sinh theo template có điền ngẫu nhiên nhiều thành phần biến đổi nhằm tăng tính đa dạng). Sau khi làm sạch, bộ dữ liệu gồm 13.679 mẫu, gán nhãn nhị phân: `0` – An toàn và `1` – Độc hại (tin giả/lừa đảo).

> 🌐 **Ứng dụng Demo:** Hệ thống đã được đóng gói thành Web App hoàn chỉnh (FastAPI + Streamlit). Xem chi tiết tại: 👉 [**Hướng dẫn cài đặt & chạy Web App (WEBAPP_GUIDE.md)**](WEBAPP_GUIDE.md)

---

## 1. Giới thiệu tổng quan và bài toán

Đề tài giải quyết bài toán phân loại văn bản nhị phân có giám sát: cho một đoạn văn bản tiếng Việt (bài đăng mạng xã hội hoặc tin nhắn), mô hình dự đoán nhãn `0` (an toàn) hoặc `1` (độc hại — tin giả hoặc lừa đảo).

### 1.1. Phạm vi dữ liệu

Dữ liệu văn bản thuần túy (không xử lý hình ảnh/video/âm thanh), gồm hai loại:
- **Tin tức/bài đăng mạng xã hội** — dạng bài viết dài (trung bình ~151 từ), chủ đề chủ yếu xoay quanh tin giả thời sự/y tế.
- **Tin nhắn** — dạng văn bản ngắn (trung bình ~17 từ), mô phỏng các kịch bản lừa đảo phổ biến: giả mạo ngân hàng, giả danh cơ quan chức năng, tuyển dụng ảo, lừa đảo tình cảm/trúng thưởng.

### 1.2. Quy trình thực hiện (10 bước chuẩn)

1. Thu thập dữ liệu
2. Tiền xử lý dữ liệu (chuẩn hóa Unicode, loại URL/email/HTML/emoji, loại trùng lặp)
3. Tách từ tiếng Việt bằng VnCoreNLP
4. Phân tích khám phá dữ liệu (EDA)
5. Trích xuất đặc trưng (TF-IDF cho Naive Bayes/SVM; embedding học từ đầu cho LSTM; tokenizer PhoBERT cho PhoBERT)
6. Chia tập Train/Validation/Test (80/10/10, có phân tầng theo nhãn)
7. Xây dựng và huấn luyện các mô hình baseline (Naive Bayes, SVM) và mô hình đề xuất (LSTM, PhoBERT)
8. Tối ưu siêu tham số (GridSearchCV cho Naive Bayes/SVM; Optuna cho PhoBERT)
9. Đánh giá mô hình (Accuracy, Precision, Recall, F1-Score, Confusion Matrix)
10. So sánh hiệu năng các mô hình và đóng gói ứng dụng

---

## 2. Mô tả các thành phần thư mục trong bộ dữ liệu

```text
FakeNews/
├── backend_main.py          # FastAPI server phục vụ mô hình
├── frontend_app.py         # Giao diện Web Streamlit
├── requirements.txt        # Thư viện phụ thuộc
├── README.md               # Báo cáo tổng quan đề tài
├── WEBAPP_GUIDE.md         # Hướng dẫn chạy Web App Demo
│
├── Đồ_án_FakeNews.ipynb    # Notebook toàn bộ quy trình thực nghiệm
│
├── Dataset/ (hoặc data/)
│   ├── cleaned_dataset.csv # Dữ liệu đã làm sạch (13.679 mẫu)
│   ├── train_split.csv     # Tập huấn luyện (10.943 mẫu)
│   ├── val_split.csv       # Tập kiểm định (1.368 mẫu)
│   └── test_split.csv      # Tập kiểm tra (1.368 mẫu)
│
└── Results/ (hoặc results/)
    ├── baseline_results.csv              # Kết quả Naive Bayes, SVM
    ├── phobert_results.csv               # Kết quả PhoBERT
    ├── eda_overview.png                  # Biểu đồ phân tích dữ liệu (EDA)
    ├── model_comparison_chart_decimal.png # Biểu đồ so sánh 4 mô hình
    ├── cm_naive_bayes.png                # Confusion Matrix — Naive Bayes
    └── cm_svm.png                        # Confusion Matrix — SVM
