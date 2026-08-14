# PHÁT HIỆN TIN GIẢ VÀ TIN NHẮN LỪA ĐẢO TIẾNG VIỆT BẰNG PHOBERT

Đây là đồ án chuyên ngành xây dựng hệ thống phát hiện tin giả và tin nhắn lừa đảo trên mạng xã hội tiếng Việt, sử dụng mô hình PhoBERT (fine-tune) làm phương pháp chính, đối chiếu với ba mô hình học máy baseline (Naive Bayes, SVM, LSTM) để đánh giá hiệu quả một cách khách quan.

Bộ dữ liệu thực nghiệm được tổng hợp từ hai nguồn: (1) tập bài đăng mạng xã hội/tin tức đã gán nhãn tin thật – tin giả, và (2) tập tin nhắn mô phỏng các kịch bản lừa đảo phổ biến tại Việt Nam (sinh theo template có điền ngẫu nhiên nhiều thành phần biến đổi nhằm tăng tính đa dạng). Sau khi làm sạch, bộ dữ liệu gồm 13.679 mẫu, gán nhãn nhị phân: `0` – An toàn và `1` – Độc hại (tin giả/lừa đảo).

> **Lưu ý:** Phần dữ liệu tin nhắn lừa đảo hiện tại phần lớn là dữ liệu tổng hợp, chưa phải thu thập hoàn toàn từ thực tế
## 1. Giới thiệu tổng quan và bài toán

Đề tài giải quyết bài toán phân loại văn bản nhị phân có giám sát: cho một đoạn văn bản tiếng Việt (bài đăng mạng xã hội hoặc tin nhắn), mô hình dự đoán nhãn `0` (an toàn) hoặc `1` (độc hại — tin giả hoặc lừa đảo).

### 1.1. Phạm vi dữ liệu

Dữ liệu văn bản thuần túy (không xử lý hình ảnh/video/âm thanh), gồm hai loại:

- **Tin tức/bài đăng mạng xã hội** — dạng bài viết dài (trung bình ~151 từ), chủ đề chủ yếu xoay quanh tin giả thời sự/y tế.
- **Tin nhắn** — dạng văn bản ngắn (trung bình ~17 từ), mô phỏng các kịch bản lừa đảo phổ biến: giả mạo ngân hàng, giả danh cơ quan chức năng, tuyển dụng ảo, lừa đảo tình cảm/trúng thưởng.

### 1.2. Quy trình thực hiện

Đề tài được thực hiện theo quy trình chuẩn cho bài toán học máy:

1. Thu thập dữ liệu
2. Tiền xử lý dữ liệu (chuẩn hóa Unicode, loại URL/email/HTML/emoji, loại trùng lặp)
3. Phân tích khám phá dữ liệu (EDA)
4. Trích xuất đặc trưng (TF-IDF cho Naive Bayes/SVM; embedding học từ đầu cho LSTM; tokenizer PhoBERT cho PhoBERT)
5. Chia tập Train/Validation/Test (80/10/10, có phân tầng theo nhãn)
6. Xây dựng và huấn luyện các mô hình baseline (Naive Bayes, SVM) và mô hình đề xuất (LSTM, PhoBERT)
7. Huấn luyện mô hình
8. Tối ưu siêu tham số (GridSearchCV cho Naive Bayes/SVM; Optuna cho PhoBERT)
9. Đánh giá mô hình (Accuracy, Precision, Recall, F1-Score, Confusion Matrix)
10. So sánh hiệu năng các mô hình

## 2. Mô tả các thành phần thư mục trong bộ dữ liệu

```
FakeNews/
├── Đồ_án_FakeNews.ipynb        
├── data/
│   ├── cleaned_dataset.csv     # Dữ liệu đã làm sạch (13.679 mẫu)
│   ├── train_split.csv         # Tập huấn luyện (10.943 mẫu)
│   ├── val_split.csv           # Tập kiểm định (1.368 mẫu)
│   └── test_split.csv          # Tập kiểm tra (1.368 mẫu)
├── results/
│   ├── baseline_results.csv              # Kết quả Naive Bayes, SVM
│   ├── phobert_results.csv               # Kết quả PhoBERT
│   ├── eda_overview.png                  # Biểu đồ phân tích dữ liệu (EDA)
│   ├── model_comparison_chart_decimal.png # Biểu đồ so sánh 4 mô hình (dạng số thập phân)
│   ├── cm_naive_bayes.png                # Confusion Matrix — Naive Bayes
│   └── cm_svm.png                        # Confusion Matrix — SVM
└── README.md
```

## 3. Các mô hình được xây dựng và so sánh

| Mô hình | Biểu diễn đặc trưng | Thư viện |
|---|---|---|
| Naive Bayes | TF-IDF (n-gram 1,2) | scikit-learn |
| SVM | TF-IDF (n-gram 1,2) | scikit-learn |
| LSTM | Embedding học từ đầu | PyTorch |
| **PhoBERT** (mô hình đề xuất) | Contextual Embedding (tiền huấn luyện) | Hugging Face Transformers |

### Kết quả trên tập kiểm tra

| Mô hình | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| Naive Bayes | 0.8999 | 1.0000 | 0.6549 | 0.7915 |
| SVM | 90.9678 | 0.9809 | 0.9068 | 0.9424 |
| LSTM | 0.9364 | 0.9212 | 0.8539 | 0.8863 |
| **PhoBERT** | **0.9700** | 0.9785 | **0.9169** | **0.9467** |

PhoBERT đạt hiệu quả cao nhất trong 4 mô hình, xác nhận lợi thế của việc tận dụng tri thức ngôn ngữ từ giai đoạn tiền huấn luyện quy mô lớn so với việc học biểu diễn ngôn ngữ từ đầu.

## 4. Các thư viện được sử dụng

1. Pandas, NumPy — xử lý dữ liệu
2. Scikit-learn — Naive Bayes, SVM, TF-IDF, GridSearchCV, các chỉ số đánh giá
3. PyTorch — xây dựng và huấn luyện LSTM
4. Hugging Face Transformers — tải và fine-tune PhoBERT
5. Optuna — tối ưu siêu tham số tự động
6. VnCoreNLP (py_vncorenlp) — tách từ tiếng Việt
7. Matplotlib, Seaborn — trực quan hóa dữ liệu và kết quả

## 5. Cách chạy lại project

Toàn bộ pipeline (từ tiền xử lý dữ liệu đến huấn luyện, tối ưu siêu tham số và so sánh 4 mô hình) đã được gộp chung vào **một file notebook duy nhất**: [`Đồ_án_FakeNews.ipynb`](Đồ_án_FakeNews.ipynb).

**Cách chạy:**

1. Mở file `Đồ_án_FakeNews.ipynb` trên Google Colab (khuyến nghị, do cần GPU cho PhoBERT/LSTM): vào [colab.research.google.com](https://colab.research.google.com) → File → Upload notebook.
2. Bật GPU: Runtime → Change runtime type → chọn GPU (T4).
3. Chạy tuần tự **từng cell từ trên xuống dưới** (Runtime → Run all), theo đúng thứ tự các phần đã đánh dấu bằng tiêu đề markdown trong notebook:
   1. Tiền xử lý dữ liệu
   2. Phân tích dữ liệu (EDA)
   3. Chia dữ liệu Train / Validation / Test
   4. Feature Engineering
   5. Huấn luyện mô hình PhoBERT
   6. Huấn luyện mô hình LSTM
   7. Huấn luyện mô hình Naive Bayes và SVM
   8. Sinh dữ liệu giả lập (tùy chọn — chỉ cần chạy nếu muốn tái tạo lại tập tin nhắn tổng hợp)
   9. Tối ưu siêu tham số
   10. So sánh hiệu năng các mô hình

> **Lưu ý:** Không chạy nhảy cóc từng cell riêng lẻ — một số cell (ví dụ phần huấn luyện LSTM/PhoBERT) phụ thuộc vào biến đã được tạo ra ở các cell tiền xử lý/chia dữ liệu phía trên.

## 6. Tác giả

- **Sinh viên thực hiện:** Nguyễn Đức Nhật — MSSV 2311555174 — Lớp 23DTH2B
- **Ngành:** Khoa học Dữ liệu
- **Giảng viên hướng dẫn:** Phạm Đình Tài
- **Đơn vị:** Khoa Công nghệ Thông tin, Trường Đại học Nguyễn Tất Thành

## 7. Tài liệu tham khảo

1. Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS.
2. Devlin, J., et al. (2019). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. NAACL.
3. Nguyen, D. Q., & Nguyen, A. T. (2020). *PhoBERT: Pre-trained language models for Vietnamese*. Findings of EMNLP.
4. Hochreiter, S., & Schmidhuber, J. (1997). *Long Short-Term Memory*. Neural Computation.
5. Cortes, C., & Vapnik, V. (1995). *Support-Vector Networks*. Machine Learning.
