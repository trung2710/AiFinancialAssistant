import re
from pathlib import Path
from typing import Dict
from src.config.settings import Settings
import pandas as pd


class ReportMetadataExtractor:
    def __init__(self):
        self.path_code_stock = Settings.PATH_CODE_STOCK
        df_mapper = pd.read_csv(self.path_code_stock)
        self.company_mapper = dict(zip(df_mapper['Mã CK'], df_mapper['Tên công ty']))
        self.year_pattern = re.compile(r'20\d{2}$')

    def _determine_report_type(self, folder_name: str) -> str:
        folder_lower = folder_name.lower()
        if "explanation" in folder_lower or "explanatory" in folder_lower:
            return "explanations"
        elif "aggregated" in folder_lower:
            return "aggregated"
        elif "consolidated" in folder_lower:
            return "consolidated"
        elif "separate" in folder_lower:
            return "separate"
        elif self.year_pattern.search(folder_lower):
            return "separate"
        return "unknown"

    def extract(self, file_path: str) -> Dict[str, str]:
        path_obj = Path(file_path)
        if len(path_obj.parts) < 4:
            raise ValueError(f"Đường dẫn không đủ cấu trúc: {file_path}")

        ticker = path_obj.parts[-4].upper()
        year = path_obj.parts[-3]
        parent_folder = path_obj.parent.name

        report_type = self._determine_report_type(parent_folder)
        company_name = self.company_mapper.get(ticker, "")

        return {
            "ticker": ticker,
            "company_name": company_name,
            "year": year,
            "report_type": report_type,
            "original_folder": parent_folder
        }


# ==========================================
# KHU VỰC CHẠY THỬ NGHIỆM (TESTING)
# ==========================================
# if __name__ == "__main__":
#     # Khởi tạo đối tượng xử lý
#     metadata_extractor = ReportMetadataExtractor()
#
#     test_paths = [
#         "/home/manh/Data/data_finance_r2ai/financial_statements/NAB/2023/NAB_financial_statements_2023_consolidated_1/NAB_financial_statements_2023_consolidated_1_extracted.txt",
#         "/home/manh/Data/data_finance_r2ai/financial_statements/FTS/2023/FTS_financial_statements_2023/FTS_financial_statements_2023_extracted.txt",
#         "/home/manh/Data/data_finance_r2ai/financial_statements/VSF/2025/VSF_financial_statements_2025_aggregated/VSF_financial_statements_2025_aggregated_extracted.txt",
#         "/home/manh/Data/data_finance_r2ai/financial_statements/PRT/2020/PRT_2020_financial_statement_explanations/PRT_2020_financial_statement_explanations_extracted.txt",
#         "/home/manh/Data/data_finance_r2ai/financial_statements/SJG/2025/SJG_financial_statements_2025_aggregated/SJG_financial_statements_2025_aggregated_extracted.txt",
#         "/home/manh/Data/data_finance_r2ai/financial_statements/ASM/2020/ASM_financial_statements_2020_separate/ASM_financial_statements_2020_separate_extracted.txt"
#     ]
#
#     for p in test_paths:
#         try:
#             meta = metadata_extractor.extract(p)
#             print(f"[{meta['company_name']} - {meta['year']}] Loại: {meta['report_type'].upper().ljust(12)} <- (Folder gốc: {meta['original_folder']})")
#         except ValueError as e:
#             print(e)

