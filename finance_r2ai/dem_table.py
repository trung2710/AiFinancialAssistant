import json
from pathlib import Path


def count_total_tables(folder_path: str):
    """
    Quét toàn bộ file JSON trong thư mục và đếm tổng số bảng.
    """
    total_tables = 0

    # Tìm tất cả các file có đuôi .json trong thư mục (kể cả thư mục con)
    json_files = list(Path(folder_path).rglob("*.json"))
    total_files = len(json_files)

    print(f"Bắt đầu quét {total_files} file JSON...\n" + "=" * 45)

    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                chunks = json.load(f)

                # Mỗi phần tử trong list JSON đại diện cho 1 bảng
                if isinstance(chunks, list):
                    num_tables = len(chunks)
                    total_tables += num_tables
                else:
                    print(f"⚠️ Cảnh báo: File {file_path.name} không đúng định dạng list.")

        except json.JSONDecodeError:
            print(f"❌ Lỗi: File {file_path.name} bị hỏng định dạng JSON.")
        except Exception as e:
            print(f"❌ Lỗi khi đọc file {file_path.name}: {e}")

    print("=" * 45)
    print(f"🚀 TỔNG SỐ BẢNG ĐÃ TRÍCH XUẤT: {total_tables} bảng")
    print("=" * 45)


# ==========================================
# KHU VỰC CHẠY
# ==========================================
if __name__ == "__main__":
    # Điền đúng đường dẫn thư mục lưu JSON của bạn lúc nãy
    folder_save_json = "/home/manh/Code/finance_r2ai/save_json"

    count_total_tables(folder_save_json)