import re
import sys
from pathlib import Path
from typing import Dict

from src.config.settings import Settings
import pandas as pd


class ReportMetadataExtractor:
    def __init__(self):
        self.path_code_stock = Settings.PATH_CODE_STOCK
        df_mapper = pd.read_csv(self.path_code_stock)
        self.company_mapper = dict(
            zip(df_mapper['Mã CK'], df_mapper['Tên công ty']))
        self.year_pattern = re.compile(r'20\d{2}$')

    def _determine_report_type(self, folder_name: str) -> str:
        folder_lower = folder_name.lower()

        # báo cáo thuyết minh
        if "explanation" in folder_lower or "explanatory" in folder_lower:
            return "explanations"

        # báo cáo tổng hợp
        elif "aggregated" in folder_lower:
            return "aggregated"

        # Báo cáo hợp nhaatss
        elif "consolidated" in folder_lower:
            return "consolidated"

        # Báo cáo riêng lẻ
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


# == == == == == == == == == == == == == == == == == == == == ==
# KHU VỰC CHẠY THỬ NGHIỆM(TESTING)
# == == == == == == == == == == == == == == == == == == == == ==
# if __name__ == "__main__":
#     # Khởi tạo đối tượng xử lý
#     metadata_extractor = ReportMetadataExtractor()

#     test_paths = [
#         "/home/newuser/Code/AiFinancialAssistant/instructions/data/financial_statements/ABB/2022/ABB_financial_statements_2022_consolidated/ABB_financial_statements_2022_consolidated_extracted.txt",
#         "/home/newuser/Code/AiFinancialAssistant/instructions/data/financial_statements/ABB/2025/ABB_financial_statements_2025_separate/ABB_financial_statements_2025_separate_extracted.txt",
#         "instructions/data/financial_statements/ACV/2022/ACV_financial_statements_2022_aggregated/ACV_financial_statements_2022_aggregated_extracted.txt"]

#     for p in test_paths:
#         try:
#             meta = metadata_extractor.extract(p)
#             print(f"[{meta['ticker']} - {meta['company_name']} - {meta['year']}] Loại: {meta['report_type'].upper().ljust(12)} <- (Folder gốc: {meta['original_folder']})")
#         except ValueError as e:
#             print(e)
