# DATASET

Thư mục này chứa dữ liệu đã qua xử lý, dùng để huấn luyện và đánh giá các mô hình phát hiện tin giả/tin nhắn lừa đảo tiếng Việt.

## Nguồn dữ liệu gốc

Bộ dữ liệu được tổng hợp từ hai nguồn:

1. **Tin tức/bài đăng mạng xã hội** — tập dữ liệu dạng bài viết đã gán nhãn tin thật/tin giả (chủ đề chủ yếu xoay quanh tin giả thời sự, y tế).
2. **Tin nhắn** — tập tin nhắn mô phỏng các kịch bản lừa đảo phổ biến tại Việt Nam, sinh theo template có điền ngẫu nhiên nhiều thành phần biến đổi (tên người, ngân hàng, số tiền, đường dẫn...) nhằm tăng tính đa dạng.

> **Lưu ý về hạn chế:** Phần lớn dữ liệu tin nhắn hiện tại là dữ liệu **tổng hợp (synthetic)**, chưa phải thu thập hoàn toàn từ các vụ lừa đảo thật ngoài thực tế. Đây là hạn chế đã được ghi nhận trong báo cáo và là hướng phát triển ưu tiên tiếp theo.

## Mô tả các file

| File | Số mẫu | Mô tả |
|---|---|---|
| `cleaned_dataset.csv` | 13.679 | Dữ liệu đầy đủ sau khi làm sạch (chuẩn hóa Unicode, loại URL/email/HTML/emoji, loại trùng lặp) |
| `train_split.csv` | 10.943 | Tập huấn luyện (80%) |
| `val_split.csv` | 1.368 | Tập kiểm định (10%) — dùng trong lúc huấn luyện để theo dõi hiệu quả mô hình, chọn epoch/tham số tốt nhất |
| `test_split.csv` | 1.368 | Tập kiểm tra (10%) — chỉ dùng một lần duy nhất để đánh giá kết quả cuối cùng, không tham gia huấn luyện |

Cả 3 tập train/val/test được chia theo phương pháp **stratified sampling** (phân tầng theo nhãn), đảm bảo tỉ lệ giữa hai lớp đồng nhất giữa các tập.

## Cấu trúc cột dữ liệu

| Cột | Kiểu dữ liệu | Mô tả |
|---|---|---|
| `text` | string | Nội dung văn bản (bài đăng hoặc tin nhắn) đã làm sạch |
| `label` | int (0/1) | Nhãn phân loại: `0` = An toàn, `1` = Độc hại (tin giả/lừa đảo) |
| `source` | string | Nguồn gốc mẫu dữ liệu: `news` (tin tức/mạng xã hội) hoặc `Message` (tin nhắn) |

## Thống kê phân phối nhãn (trên `cleaned_dataset.csv`)

| Nhãn | Số mẫu | Tỉ lệ |
|---|---|---|
| 0 — An toàn | 9.707 | 70,96% |
| 1 — Độc hại | 3.972 | 29,04% |

Dữ liệu vẫn còn **mất cân bằng** giữa hai lớp — cần lưu ý khi huấn luyện (đã áp dụng `class_weight="balanced"` cho SVM) và khi diễn giải các chỉ số đánh giá (ưu tiên F1-Score thay vì chỉ dùng Accuracy).

## Cách tái tạo lại dữ liệu

Toàn bộ quy trình xử lý dữ liệu (từ dữ liệu thô đến các file trong thư mục này) nằm trong phần **"Tiền xử lý dữ liệu"**, **"Chia dữ liệu Train/Validation/Test"** và **"Code Tự động Sinh Dữ liệu Giả lập"** của notebook chính [`Đồ_án_FakeNews.ipynb`](../Đồ_án_FakeNews.ipynb).
