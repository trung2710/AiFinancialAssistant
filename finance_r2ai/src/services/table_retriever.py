import os
import json
import csv
import logging
from typing import List, Dict, Any
from src.config.settings import Settings

logger = logging.getLogger(__name__)


class TableRetriever:
    def __init__(self):
        self.save_json_dir = Settings.SAVE_JSON_DIR

    def _build_file_name(self, ticker: str, year: str, report_type: str) -> str:
        # Trả về format chuẩn: VNM_financial_statements_2022_consolidated_extracted.json
        return f"{ticker}_financial_statements_{year}_{report_type}_extracted.json"

    def _calculate_overlap(self, query: str, text: str) -> float:
        """Thuật toán Jaccard / Token Overlap cơ bản để tính độ tương đồng từ khóa"""
        if not query or not text:
            return 0.0

        # Tokenize cơ bản (chuyển chữ thường, cắt khoảng trắng)
        query_tokens = set(query.lower().split())
        text_tokens = set(text.lower().split())

        if not query_tokens:
            return 0.0

        # Tính số lượng token trùng khớp
        overlap = len(query_tokens.intersection(text_tokens))
        return overlap / len(query_tokens)

    # tìm mã chứng khoán
    def _resolve_tickers(self, tickers: List[str], company_names: List[str]) -> List[str]:
        """Tự động dò file code_stock.csv nếu thiếu tickers nhưng có company_names."""
        if not tickers and company_names:
            code_stock_path = Settings.PATH_CODE_STOCK
            if os.path.exists(code_stock_path):
                try:
                    with open(code_stock_path, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        next(reader)  # bỏ qua header
                        company_to_ticker = {row[1].strip().lower(): row[0].strip() for row in reader if len(row) >= 2}

                    for company in company_names:
                        c_lower = company.strip().lower()
                        for name_db, tck in company_to_ticker.items():
                            if name_db in c_lower or c_lower in name_db:
                                if tck not in tickers:
                                    tickers.append(tck)
                                    logger.info(f"Tự động tra cứu: {company} -> {tck}")
                except Exception as e:
                    logger.error(f"Lỗi đọc {code_stock_path}: {e}")
        return tickers

    # tìm path file
    def _get_report_file_path(self, ticker: str, year: str, report_type: str) -> tuple[str, str]:
        """Tìm file báo cáo, trả về (file_path, report_id). Có cơ chế fallback."""
        file_name = self._build_file_name(ticker, year, report_type)
        file_path = os.path.join(self.save_json_dir, file_name)
        report_id = file_name.replace(".json", "")

        if not os.path.exists(file_path):
            alt_type = "consolidated" if report_type == "separate" else "separate"
            alt_file_name = self._build_file_name(ticker, year, alt_type)
            alt_file_path = os.path.join(self.save_json_dir, alt_file_name)
            if os.path.exists(alt_file_path):
                logger.info(f"Fallback sang {alt_type} cho {ticker} năm {year}")
                return alt_file_path, alt_file_name.replace(".json", "")
            
            # Fallback 2: Báo cáo không có chữ separate/consolidated (thường là cty chứng khoán)
            no_type_file_name = f"{ticker}_financial_statements_{year}_extracted.json"
            no_type_file_path = os.path.join(self.save_json_dir, no_type_file_name)
            if os.path.exists(no_type_file_path):
                logger.info(f"Fallback sang báo cáo chung (không có loại) cho {ticker} năm {year}")
                return no_type_file_path, no_type_file_name.replace(".json", "")
            
            logger.warning(f"Không tìm thấy báo cáo nào cho {ticker} năm {year}")
            return "", ""
        return file_path, report_id

    # tính điểm cho các bảng
    def _score_tables_in_file(self, file_path: str, metric: str) -> List[tuple[float, int]]:
        """Đọc file JSON, tính điểm cho các bảng và trả về danh sách (điểm, dòng_bắt_đầu)."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                chunks = json.load(f)
        except Exception as e:
            logger.error(f"Lỗi đọc file {file_path}: {e}")
            return []

        chunk_scores = []
        for chunk in chunks:
            metadata = chunk.get("metadata", {})

            # Tiêu đề bảng thường nằm ở khoảng 10 dòng cuối cùng trước khi bắt đầu bảng
            context_lines = chunk.get("context_text", "").strip().split('\n')
            short_context = " ".join(context_lines[-10:])

            df_text = ""
            exact_match_in_row = False
            dataframe = chunk.get("dataframe", [])

            if isinstance(dataframe, list):
                for row in dataframe:
                    # Chỉ lấy giá trị ở cột đầu tiên (chứa tên chỉ tiêu tài chính) để tránh nhiễu
                    col0_val = str(row.get("0", ""))
                    df_text += col0_val + " "

                    if metric.lower() in col0_val.lower():
                        exact_match_in_row = True

            full_text_to_match = f"{short_context} {df_text}".strip()
            score = self._calculate_overlap(metric, full_text_to_match)

            # Boost điểm cực mạnh nếu tên khoản mục xuất hiện nguyên văn trong cột đầu tiên
            if exact_match_in_row:
                score += 5.0
            elif metric.lower() in full_text_to_match.lower():
                score += 2.0

            start_line = metadata.get("start_line", 0)
            chunk_scores.append((score, start_line))

        chunk_scores.sort(key=lambda x: x[0], reverse=True)
        return chunk_scores

    # hàm tổng gọi pipeline retriver
    def retrieve(self, parsed_query: Dict[str, Any], top_k: int = 2) -> List[str]:
        """
        Dựa vào kết quả của LLM Query Parser, tìm kiếm top_k bảng phù hợp nhất.
        Trả về danh sách các chuỗi dạng "<id_báo_cáo>|<vị_trí_dòng>".
        """
        results = []

        tickers = parsed_query.get("final_tickers") or parsed_query.get("tickers") or []
        company_names = parsed_query.get("company_names", [])
        years = parsed_query.get("years", [])
        report_type = parsed_query.get("report_type", "consolidated")
        metric = parsed_query.get("metric", "")

        tickers = self._resolve_tickers(tickers, company_names)

        if not isinstance(report_type, str) or report_type not in ["separate", "consolidated", "aggregated", "explanations"]:
            report_type = "consolidated"

        for ticker in tickers:
            for year in years:
                file_path, report_id = self._get_report_file_path(ticker, year, report_type)
                if not file_path:
                    continue

                chunk_scores = self._score_tables_in_file(file_path, metric)

                # Giới hạn lấy top_k bảng có điểm > 0
                for score, start_line in chunk_scores[:top_k]:
                    if score > 0:
                        results.append(f"{report_id}|{start_line}")

        return list(set(results))  # Loại bỏ trùng lặp nếu có
