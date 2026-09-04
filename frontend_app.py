
import requests
import streamlit as st

API_URL = "http://localhost:8000/predict"

st.set_page_config(page_title="Phát hiện Tin giả & Lừa đảo — PhoBERT", page_icon="🛡️", layout="centered")

st.title("🛡️ Phát hiện Tin giả & Tin nhắn Lừa đảo")
st.caption("Đồ án: Phân tích và phát hiện tin giả, tin nhắn lừa đảo trên mạng xã hội bằng PhoBERT")

# Kiểm tra backend có đang chạy không
try:
    health = requests.get("http://localhost:8000/", timeout=3)
    backend_ok = health.status_code == 200
except requests.exceptions.RequestException:
    backend_ok = False

if not backend_ok:
    st.error(
        "⚠️ Không kết nối được đến backend API. Hãy mở một terminal khác và chạy:\n\n"
        "`uvicorn backend_main:app --reload --port 8000`\n\n"
        "sau đó tải lại trang này."
    )
    st.stop()

st.success("✅ Đã kết nối backend PhoBERT thành công.")

example_options = {
    "-- Chọn ví dụ có sẵn hoặc tự nhập --": "",
    "Ví dụ: Tin nhắn lừa đảo": "Tài khoản của bạn phát hiện đăng nhập lạ. Vui lòng xác thực ngay tại bit.ly/xacthuc-tk để tránh bị khóa trong 24 giờ.",
    "Ví dụ: Tin nhắn an toàn": "Chiều nay đi đá bóng không? Sân cũ nhé, 5 giờ tập trung.",
}
choice = st.selectbox("Ví dụ nhanh", list(example_options.keys()))

text_input = st.text_area(
    "Nội dung văn bản",
    value=example_options[choice],
    height=150,
    placeholder="Dán nội dung bài đăng hoặc tin nhắn vào đây...",
)

if st.button("🔍 Kiểm tra", type="primary"):
    if not text_input.strip():
        st.warning("Vui lòng nhập nội dung văn bản trước khi kiểm tra.")
    else:
        with st.spinner("PhoBERT đang phân tích..."):
            try:
                res = requests.post(API_URL, json={"text": text_input}, timeout=30)
                res.raise_for_status()
                result = res.json()
            except requests.exceptions.RequestException as e:
                st.error(f"Lỗi khi gọi API: {e}")
                st.stop()

        st.divider()
        if result["label"] == 1:
            st.error("### ⚠️ CẢNH BÁO: Có dấu hiệu ĐỘC HẠI (tin giả/lừa đảo)")
        else:
            st.success("### ✅ AN TOÀN")

        st.metric("Độ tin cậy của dự đoán", f"{result['confidence']*100:.1f}%")
        st.progress(result["confidence"])

        with st.expander("Xem chi tiết xác suất từng nhãn"):
            st.table({
                "Nhãn": ["An toàn", "Độc hại"],
                "Xác suất": [
                    f"{result['probabilities']['An toàn']*100:.2f}%",
                    f"{result['probabilities']['Độc hại']*100:.2f}%",
                ],
            })

        st.caption(
            "⚠️ Đây là công cụ hỗ trợ tham khảo dựa trên mô hình học máy (PhoBERT), "
            "không thay thế cho việc xác minh thông tin qua các nguồn chính thống."
        )

st.divider()
with st.expander("ℹ️ Về mô hình này"):
    st.markdown("""
    - **Mô hình:** PhoBERT (fine-tune) — mô hình đề xuất chính của đồ án
    - **Kiến trúc:** PhoBERT-base, 12 lớp Transformer Encoder, ~135 triệu tham số
    - **Hiệu quả trên tập kiểm tra:** Accuracy 97,00% · F1-Score 94,67%
    - **Backend:** FastAPI · **Frontend:** Streamlit 
    """)