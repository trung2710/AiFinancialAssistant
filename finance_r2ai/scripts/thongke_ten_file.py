from pathlib import Path
from collections import Counter
import pandas as pd


def analyze_dataset_structure(root_dir_path):
    root_dir = Path(root_dir_path)

    if not root_dir.exists():
        print(f"Lỗi: Đường dẫn '{root_dir_path}' không tồn tại!")
        return

    category_stats = Counter()
    report_type_stats = Counter()

    print("Đang quét dữ liệu...")

    # Duyệt qua tất cả các file .txt trong toàn bộ cây thư mục gốc
    for txt_file in root_dir.rglob("*.txt"):
        # Lấy danh sách các cấp folder từ root_dir đến file .txt
        try:
            relative_parts = txt_file.relative_to(root_dir).parts
        except ValueError:
            continue

        # 1. Thống kê theo Loại tài liệu/Giấy tờ (Folder cấp 1 ngay dưới root, ví dụ: financial_statements)
        if len(relative_parts) > 1:
            main_category = relative_parts[0]
            category_stats[main_category] += 1

        # 2. Thống kê theo Loại báo cáo (Trích xuất từ folder con trực tiếp chứa file)
        parent_folder_name = txt_file.parent.name
        parts = parent_folder_name.split("_")

        # Tách lấy từ cuối cùng (consolidated, separate, ...)
        report_type = parts[-1] if len(parts) > 1 else parent_folder_name
        report_type_stats[report_type] += 1

    # --- IN KẾT QUẢ THỐNG KÊ ---
    print("\n" + "=" * 50)
    print("1. THỐNG KÊ THEO NHÓM GIẤY TỜ / TÀI LIỆU CẤP CAO")
    print("=" * 50)
    df_cat = pd.DataFrame(category_stats.items(), columns=["Nhóm tài liệu (Folder chính)", "Số lượng file .txt"]).sort_values(by="Số lượng file .txt", ascending=False)
    print(df_cat.to_string(index=False))

    print("\n" + "=" * 50)
    print("2. THỐNG KÊ CHI TIẾT THEO LOẠI BÁO CÁO (CONSOLIDATED / SEPARATE...)")
    print("=" * 50)
    df_rep = pd.DataFrame(report_type_stats.items(), columns=["Loại Báo cáo / Hậu tố Folder", "Số lượng file .txt"]).sort_values(by="Số lượng file .txt", ascending=False)
    print(df_rep.to_string(index=False))


# --- Thử nghiệm ---
if __name__ == "__main__":
    # Đặt đường dẫn đến folder cha chứa toàn bộ dữ liệu (chứa cả financial_statements)
    ROOT_DATA_DIR = "/home/manh/Data/data_finance_r2ai"

    analyze_dataset_structure(ROOT_DATA_DIR)