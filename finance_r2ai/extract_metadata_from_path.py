from pathlib import Path
import re


def extract_metadata_from_path(file_path: str) -> dict:
    """
    Hàm này nhận vào đường dẫn file và trả về dictionary chứa metadata chuẩn.
    Giải quyết toàn bộ các edge cases (1, 2, aggregated, thiếu nhãn...)
    """
    path_obj = Path(file_path)

    # Mặc định lấy từ cấu trúc folder: /TICKER/YEAR/...
    ticker = path_obj.parts[-4].upper()
    year = path_obj.parts[-3]

    # Lấy tên folder con trực tiếp chứa file
    parent_folder = path_obj.parent.name.lower()

    report_type = "unknown"

    # 1. Xử lý nhóm Bản giải trình (Explanations)
    if "explanation" in parent_folder or "explanatory" in parent_folder:
        report_type = "explanations"

    # 2. Xử lý nhóm Báo cáo tổng hợp (Aggregated)
    elif "aggregated" in parent_folder:
        report_type = "aggregated"

    # 3. Xử lý nhóm Hợp nhất (Consolidated) - Bắt luôn cả trường hợp có số _1, _2 ở đuôi
    elif "consolidated" in parent_folder:
        report_type = "consolidated"

    # 4. Xử lý nhóm Báo cáo riêng (Separate) - Bắt luôn cả trường hợp có số _1, _2 ở đuôi
    elif "separate" in parent_folder:
        report_type = "separate"

    # 5. Xử lý nhóm Báo cáo duy nhất (Tên folder kết thúc bằng NĂM, không có chữ consolidated/separate)
    # Ví dụ: HND_financial_statements_2023
    elif re.search(r'20\d{2}$', parent_folder):
        report_type = "separate"  # Quy chuẩn về báo cáo riêng cho các công ty không có công ty con

    return {
        "ticker": ticker,
        "year": year,
        "report_type": report_type,
        "original_folder": parent_folder
    }


# --- Test thử với các đường dẫn ngoại lệ bạn vừa tìm được ---
test_paths = [
    "NAB/2023/NAB_financial_statements_2023_consolidated_1/NAB_financial_statements_2023_consolidated_1_extracted.txt",
    "FTS/2023/FTS_financial_statements_2023/FTS_financial_statements_2023_extracted.txt",
    "VSF/2025/VSF_financial_statements_2025_aggregated/VSF_financial_statements_2025_aggregated_extracted.txt",
    "PRT/2020/PRT_2020_financial_statement_explanations/PRT_2020_financial_statement_explanations_extracted.txt",
    "SJG/2025/SJG_financial_statements_2025_aggregated/SJG_financial_statements_2025_aggregated_extracted.txt",
    "/home/manh/Data/data_finance_r2ai/financial_statements/ASM/2020/ASM_financial_statements_2020_separate/ASM_financial_statements_2020_separate_extracted.txt"
]

for p in test_paths:
    meta = extract_metadata_from_path(p)
    print(f"[{meta['ticker']} - {meta['year']}] Loại: {meta['report_type'].upper().ljust(12)} <- (Folder gốc: {meta['original_folder']})")