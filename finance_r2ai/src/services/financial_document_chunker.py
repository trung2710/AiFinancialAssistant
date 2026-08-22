import os
import json
from typing import List, Dict, Any
from pathlib import Path
import pandas as pd
from src.services.financial_table_extractor import FinancialTableExtractor
from src.services.report_metadata_extractor import ReportMetadataExtractor
from src.config.settings import Settings


class FinancialDataPipeline:
    def __init__(self, output_base_dir: str = Settings.PREPROCESS_DIR):
        self.metadata_extractor = ReportMetadataExtractor()
        self.table_extractor = FinancialTableExtractor(noise_threshold=1)
        self.output_base_dir = Path(output_base_dir)

    def process_chunk(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Thực thi toàn bộ luồng: Đọc file -> Lấy Meta -> Parse Bảng -> Chuẩn hóa số -> Ghi CSV -> Ghi Synchronized Text -> Trả về list Chunk chuẩn JSON
        """
        # 1. Bóc metadata
        metadata = self.metadata_extractor.extract(file_path)

        # 2. Lấy tên thư mục chứa file báo cáo
        folder_name = metadata.get(
            'original_folder') or Path(file_path).parent.name

        # Tạo cấu trúc thư mục đầu ra
        tables_dir = self.output_base_dir / "tables" / folder_name
        text_dir = self.output_base_dir / "text"
        json_dir = self.output_base_dir / "json"

        os.makedirs(tables_dir, exist_ok=True)
        os.makedirs(text_dir, exist_ok=True)
        os.makedirs(json_dir, exist_ok=True)

        # 3. Đọc nội dung file
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_txt = f.read()

        # 4. Trích xuất bảng, chuẩn hóa số liệu và sinh văn bản đồng bộ
        table_chunks, sync_text = self.table_extractor.process(
            raw_txt, folder_name=folder_name)

        # Ghi file văn bản đồng bộ
        sync_file_path = text_dir / f"{folder_name}_synchronized.txt"
        with open(sync_file_path, 'w', encoding='utf-8') as f:
            f.write(sync_text)

        final_chunks = []
        # 5. Lưu CSV và đóng gói JSON chunk
        for idx, chunk in enumerate(table_chunks, start=1):
            # 5.1. Tạo ID chuẩn
            chunk_id = f"{metadata['ticker']}_{metadata['year']}_{metadata['report_type']}_table_{idx}"

            # 5.2. Xuất file CSV cho từng bảng
            csv_filename = f"table_{idx}.csv"
            csv_file_path = tables_dir / csv_filename
            rel_csv_path = f"tables/{folder_name}/{csv_filename}"

            df_clean = chunk['dataframe'].copy()
            df_clean.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

            # 5.3. Chuẩn bị DataFrame dạng dict cho JSON
            df_clean_json = df_clean.fillna("")
            df_clean_json.columns = df_clean_json.columns.astype(str)
            clean_table_data = df_clean_json.to_dict(orient='records')

            # 5.4. Đóng gói chunk metadata
            chunk_metadata = metadata.copy()
            chunk_metadata['table_name'] = chunk.get('table_name')
            chunk_metadata['unit'] = chunk.get('unit')
            chunk_metadata['start_line'] = chunk.get('start_line')
            chunk_metadata['csv_path'] = rel_csv_path
            chunk_metadata['csv_abs_path'] = str(csv_file_path)

            final_chunk = {
                "chunk_id": chunk_id,
                "metadata": chunk_metadata,
                "context_text": chunk['context_text'],
                "raw_table": chunk.get('raw_table', ''),
                "dataframe": clean_table_data
            }
            final_chunks.append(final_chunk)

        # Ghi file JSON tổng hợp cho file báo cáo này
        json_file_path = json_dir / f"{folder_name}.json"
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(final_chunks, f, ensure_ascii=False, indent=4)

        return final_chunks


if __name__ == "__main__":
    chunker = FinancialDataPipeline()

    folder_path = Settings.FINANCIAL_STATEMENTS_DIR
    folder_save_json = Settings.SAVE_JSON_DIR

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

            print(
                f"[{index}/{total_files}] ✅ Xong: {file_name_txt} -> {len(document_chunks)} bảng")
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
