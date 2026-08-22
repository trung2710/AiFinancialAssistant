# Kế Hoạch Triển Khai: Tạo Dataset Fine-tune Tầng 2 (Text-to-Pandas)

**Mục tiêu:** Sử dụng **Gemini 3.5 Flash Lite** (thông qua API) đóng vai trò "Teacher Model" để giải 1000+ câu hỏi trong `ViFinQA_train.jsonl`, tự động sinh ra file dataset chuẩn để fine-tune Qwen 9B.

## 1. Định dạng Dataset Đầu ra
Định dạng chuẩn **ChatML** cho file `ViFinQA_finetune.jsonl` (tối ưu để fine-tune Qwen bằng thư viện Unsloth).
```json
{
  "messages": [
    {"role": "system", "content": "Bạn là chuyên gia tài chính. Dựa vào Bảng dữ liệu (dạng Markdown), hãy viết code Python bằng thư viện Pandas để trả về kết quả chính xác theo yêu cầu câu hỏi. Tên hàm luôn là `solve(df)`."},
    {"role": "user", "content": "BẢNG DỮ LIỆU:\n| Chỉ tiêu | Năm 2018 |\n|---|---|\n| Lãi tiền gửi | 1500 |\n\nCÂU HỎI: Lãi tiền gửi năm 2018 là bao nhiêu?"},
    {"role": "assistant", "content": "```python\nimport pandas as pd\n\ndef solve(df):\n    return df[df['Chỉ tiêu'] == 'Lãi tiền gửi']['Năm 2018'].values[0]\n```"}
  ]
}
```

## 2. Kiến trúc Script Tự Động Hóa
Script sẽ chạy hoàn toàn tự động 100% tại máy local, không phụ thuộc vào LLM trên Colab.

### Bước 1: Khởi tạo Client
- Dùng SDK `google-genai` kết nối API Gemini 3.5 Flash Lite.
- Xử lý Rate Limit (nếu dùng gói Free, cần delay giữa các request) và tự động Retry khi lỗi mạng.

### Bước 2: Auto-Parsing (Tầng 1)
- Gửi từng câu hỏi trong `ViFinQA_train.jsonl` cho Gemini 3.5 Flash Lite để parse ra JSON (`company_names`, `tickers`, `years`, `metric`).
- Map tên công ty sang mã chứng khoán bằng `query_parser.py`.

### Bước 3: Table Retrieval (Tầng 1)
- Đưa kết quả parse vào `table_retriever.py` để tìm ra bảng (CSV) liên quan nhất.

### Bước 4: Data Formatting
- Đọc file CSV đã tìm được và chuyển nó thành chuỗi định dạng Markdown.
- Chèn Bảng Markdown + Câu hỏi vào Prompt gửi cho Gemini.

### Bước 5: Sinh Code Pandas (Tầng 2 - Teacher)
- Gọi Gemini 3.5 Flash Lite lần 2 để đóng vai chuyên gia tài chính.
- Yêu cầu viết code `solve(df)` logic tính toán.

### Bước 6: Lưu kết quả
- Lưu bộ 3 (System, User, Assistant) vào file `ViFinQA_finetune.jsonl`.

## 3. Quá trình Xác thực (Verification)
- Cần chạy thử script với khoảng 5 câu đầu tiên của tập train để kiểm tra output.
- Xem xét code sinh ra có hợp lý không trước khi chạy toàn bộ 1000 câu.
