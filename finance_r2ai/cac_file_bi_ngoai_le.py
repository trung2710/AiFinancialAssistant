from pathlib import Path
from collections import defaultdict
import pandas as pd


def inspect_edge_cases(root_dir_path):
    root_dir = Path(root_dir_path)

    if not root_dir.exists():
        print(f"Lỗi: Đường dẫn '{root_dir_path}' không tồn tại!")
        return

    # Dictionary gom nhóm danh sách file theo loại ngoại lệ
    edge_cases = defaultdict(list)
    total_files = 0
    standard_files = 0

    for txt_file in root_dir.rglob("*.txt"):
        total_files += 1
        path_str = str(txt_file).lower()
        parent_folder_name = txt_file.parent.name

        # Lấy hậu tố của folder con
        parts = parent_folder_name.split("_")
        suffix = parts[-1] if len(parts) > 1 else parent_folder_name

        # Kiểm tra chuẩn (consolidated / separate)
        if "consolidated" in suffix:
            standard_files += 1
        elif "separate" in suffix:
            standard_files += 1
        else:
            # Gom nhóm theo loại ngoại lệ
            edge_cases[suffix].append(txt_file)

    # --- IN KẾT QUẢ DANH SÁCH NGOẠI LỆ ---
    print("=" * 80)
    print(f"TỔNG SỐ FILE: {total_files} | FILE CHUẨN: {standard_files} | FILE NGOẠI LỆ: {total_files - standard_files}")
    print("=" * 80)

    for category, files in sorted(edge_cases.items()):
        print(f"\n[+] NHÓM NGOẠI LỆ: '{category}' ({len(files)} files)")
        print("-" * 60)
        for f in files:
            # In đường dẫn tương đối tính từ root_dir cho ngắn gọn, dễ nhìn
            try:
                rel_path = f.relative_to(root_dir)
                print(f"  └─ {rel_path}")
            except ValueError:
                print(f"  └─ {f}")


# --- Chạy kiểm tra ---
if __name__ == "__main__":
    ROOT_DATA_DIR = "/home/manh/Data/data_finance_r2ai/financial_statements"
    inspect_edge_cases(ROOT_DATA_DIR)