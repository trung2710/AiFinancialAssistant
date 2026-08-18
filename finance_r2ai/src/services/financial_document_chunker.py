import os
import json
from typing import List, Dict, Any
from pathlib import Path
import pandas as pd
from src.services.financial_table_extractor import FinancialTableExtractor
from src.services.report_metadata_extractor import ReportMetadataExtractor


class FinancialDataPipeline:
    def __init__(self):
        self.metadata_extractor = ReportMetadataExtractor()
        self.table_extractor = FinancialTableExtractor(noise_threshold=1)

    def process_chunk(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Thực thi toàn bộ luồng: Đọc file -> Lấy Meta -> Parse Bảng -> Làm sạch -> Trả về danh sách Chunk chuẩn JSON
        """
        # 1. Bóc metadata
        metadata = self.metadata_extractor.extract(file_path)

        # 2. Đọc nội dung file
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_txt = f.read()

        # 3. Trích xuất bảng và context text (Trả về list chứa DataFrame thô)
        table_chunks = self.table_extractor.process(raw_txt)

        final_chunks = []
        # 4. Làm sạch dữ liệu, gắn metadata và đóng gói hoàn chỉnh
        for idx, chunk in enumerate(table_chunks):
            # 4.1. Tạo ID chuẩn
            chunk_id = f"{metadata['ticker']}_{metadata['year']}_{metadata['report_type']}_table_{idx + 1}"

            # 4.2. XỬ LÝ LÀM SẠCH DATAFRAME CHUẨN JSON
            df_clean = chunk['dataframe'].copy()

            # Biến NaN thành chuỗi rỗng "" để tránh lỗi chuẩn JSON
            df_clean = df_clean.fillna("")

            # Ép tên cột thành string (tránh lỗi JSON do key là số nguyên)
            df_clean.columns = df_clean.columns.astype(str)

            # Convert thẳng sang dạng list of dicts (thân thiện với LLM)
            clean_table_data = df_clean.to_dict(orient='records')

            # 4.3. Đóng gói chunk
            chunk_metadata = metadata.copy()
            chunk_metadata['table_name'] = chunk.get('table_name')
            chunk_metadata['unit'] = chunk.get('unit')
            chunk_metadata['start_line'] = chunk.get('start_line')
            
            final_chunk = {
                "chunk_id": chunk_id,
                "metadata": chunk_metadata,
                "context_text": chunk['context_text'],
                "dataframe": clean_table_data
            }
            final_chunks.append(final_chunk)

        return final_chunks


if __name__ == "__main__":
    chunker = FinancialDataPipeline()

    folder_path = "/home/manh/Data/data_finance_r2ai/financial_statements"
    folder_save_json = "/home/manh/Code/finance_r2ai/save_json"

    # Tạo thư mục lưu trữ nếu chưa có
    os.makedirs(folder_save_json, exist_ok=True)

    # Dùng rglob để quét tất cả các file .txt trong mọi thư mục con
    txt_files = list(Path(folder_path).rglob("*.txt"))
    total_files = len(txt_files)

    print(f"Bắt đầu quét và xử lý {total_files} files...\n" + "=" * 40)

    success_count = 0
    error_count = 0
    skip_count = 0

    for index, file_path_obj in enumerate(txt_files, start=1):
        file_path_str = str(file_path_obj)
        file_name_txt = file_path_obj.name

        # Đổi đuôi .txt thành .json
        file_name_json = file_path_obj.stem + ".json"
        save_path = os.path.join(folder_save_json, file_name_json)

        # Bỏ qua nếu file json đã được xử lý từ trước
        if os.path.exists(save_path):
            print(f"[{index}/{total_files}] ⏩ Đã tồn tại, bỏ qua: {file_name_json}")
            skip_count += 1
            continue

        try:
            # Chạy pipeline băm chunk
            document_chunks = chunker.process_chunk(file_path_str)

            # Ghi ra file JSON
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(document_chunks, f, ensure_ascii=False, indent=4)

            print(f"[{index}/{total_files}] ✅ Xong: {file_name_txt} -> {len(document_chunks)} bảng")
            success_count += 1

        except Exception as e:
            print(f"[{index}/{total_files}] ❌ Lỗi tại file {file_name_txt}: {e}")
            error_count += 1

    print("\n" + "=" * 40)
    print(f"THỐNG KÊ HOÀN THÀNH:")
    print(f"- Tổng số file quét: {total_files}")
    print(f"- Xử lý thành công : {success_count}")
    print(f"- Đã bỏ qua (đã có): {skip_count}")
    print(f"- Lỗi khi xử lý    : {error_count}")
    print("=" * 40)
