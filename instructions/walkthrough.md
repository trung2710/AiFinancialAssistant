# Báo cáo Hoàn thành Giai đoạn Tiền Xử lý (Data Preprocessing Walkthrough)

Toàn bộ các mục trong **Implementation Plan** đã được hoàn thành 100% và kiểm chứng qua các báo cáo thực tế (`AAA_2025` và `ABB_2020`).

---

## 1. Các hạng mục đã thực hiện

### 1.1 Chuẩn hóa Dữ liệu Số (Numeric Normalization)
- **Regex thông minh**: Áp dụng biểu thức chính quy `^\d{1,3}(?:\.\d{3})+(?:,\d+)?$` để nhận diện chính xác số liệu kế toán Việt Nam.
- **Xử lý số âm**: Đổi các định dạng số âm dạng ngoặc đơn `(1.234.567)` thành `-1234567`.
- **Dấu chấm & dấu phẩy**: Xóa dấu chấm phân cách ngàn `.` và đổi dấu phẩy thập phân `,` thành dấu chấm `.`.
- **Bảo vệ dữ liệu không phải tiền**: Các cột Thuyết minh (như `10.1`, `12.3`...), các số tỷ lệ phần trăm (`96,92%`) hoặc chữ văn bản hoàn toàn không bị ảnh hưởng và được giữ nguyên dạng chuỗi.

### 1.2 Xuất Bảng biểu ra File CSV (CSV Export)
- Các bảng sau khi cắt, nối trang và chuẩn hóa số liệu được ghi ra file `.csv` riêng biệt với mã hóa `utf-8-sig` (thân thiện với Excel/Pandas).
- Thư mục lưu trữ: `C:\vscode\AiFinancialAssistant\finance_r2ai\preprocess\tables\<folder_name>\table_<N>.csv`.
- Đường dẫn CSV (`csv_path`) được tự động nhúng vào phần metadata của từng chunk JSON.

### 1.3 Tạo File Văn bản Đồng bộ (Synchronized Text Files)
- Tạo file sao chép mới tại `C:\vscode\AiFinancialAssistant\finance_r2ai\preprocess\text\<folder_name>_synchronized.txt`.
- **Bảo toàn 100% văn bản gốc**: Giữ nguyên các dòng ngắt trang `===== PAGE X =====`, tiêu đề, chân trang và xuống dòng từ file trích xuất gốc.
- **Liên kết đồng bộ**: Thay thế các khối HTML `<table>...</table>` bằng Markdown link `[TABLE_N](tables/<folder_name>/table_N.csv)`.

### 1.5 Chuẩn hóa Cấu trúc Bảng biểu Nâng cao (Table Standardization - Step C)
- **Làm phẳng Tiêu đề Đa tầng (`_flatten_headers`)**: Tự động phát hiện các dòng tiêu đề chữ ở đầu DataFrame (do OCR thiếu thẻ `<th>`) và làm phẳng chúng bằng cách gộp các tầng tiêu đề lại với nhau nối bằng dấu `_` (VD: `31/12/2025 (VND)_Giá gốc`). Loại bỏ hoàn toàn dòng tiêu đề giả `0,1,2,3,4`.
- **Lan truyền Ngữ cảnh Nhóm (`_propagate_group_context`)**: Tự động phát hiện các dòng tiêu đề nhóm lớn (như `NỢ PHẢI TRẢ`, `VỐN CHỦ SỞ HỮU` hoặc `Phải thu của khách hàng` gộp `colspan="N"`) và lan truyền tên nhóm này làm tiền tố đính kèm vào trước các chỉ tiêu con (dùng ký hiệu `__` chuẩn cho Pandas Query, VD: `NỢ PHẢI TRẢ__Tiền gửi của khách hàng`).
- **Tổng quát hóa $N$ cột**: Xử lý mượt mà cho mọi loại bảng với số cột $N$ bất kỳ ($N=2, 3, 4, 8, 12...$).

---

## 2. Kết quả Kiểm thử (Verification Results)

Đã chạy kiểm thử thực tế trên tập dữ liệu `AAA_2025_consolidated` và `ABB_2020_consolidated`:
- **Số lượng bảng trích xuất**: Trích xuất thành công 48 bảng biểu (tính cả các bảng nối trang).
- **Thư mục đầu ra `preprocess/`**:
  - `preprocess/tables/`: Đã tạo đầy đủ các file CSV từ `table_1.csv` đến `table_48.csv`.
  - `preprocess/text/`: Đã tạo file `..._synchronized.txt` khớp 100% văn bản gốc.
  - `preprocess/json/`: Đã tạo file `.json` chứa danh sách chunk chuẩn format.

---

## 3. Cấu trúc Thư mục Kết quả Đầu ra

```
C:\vscode\AiFinancialAssistant\finance_r2ai\preprocess\
├── tables/
│   ├── AAA_financial_statements_2025_consolidated/
│   │   ├── table_1.csv
│   │   ├── table_2.csv
│   │   └── ...
│   └── ABB_financial_statements_2020_consolidated/
│       ├── table_1.csv
│       └── ...
├── text/
│   ├── AAA_financial_statements_2025_consolidated_synchronized.txt
│   └── ABB_financial_statements_2020_consolidated_synchronized.txt
└── json/
    ├── AAA_financial_statements_2025_consolidated.json
    └── ABB_financial_statements_2020_consolidated.json
```
