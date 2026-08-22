import os
import json
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

    def retrieve(self, parsed_query: Dict[str, Any], top_k: int = 2) -> List[str]:
        """
        Dựa vào kết quả của LLM Query Parser, tìm kiếm top_k bảng phù hợp nhất.
        Trả về danh sách các chuỗi dạng "<id_báo_cáo>|<vị_trí_dòng>".
        """
        results = []

        tickers = parsed_query.get("final_tickers", [])
        years = parsed_query.get("years", [])
        report_type = parsed_query.get("report_type", "consolidated")
        metric = parsed_query.get("metric", "")

        if not isinstance(report_type, str) or report_type not in ["separate", "consolidated", "aggregated", "explanations"]:
            report_type = "consolidated"

        for ticker in tickers:
            for year in years:
                # 1. Định vị file JSON chứa báo cáo
                file_name = self._build_file_name(ticker, year, report_type)
                file_path = os.path.join(self.save_json_dir, file_name)
                report_id = file_name.replace(".json", "")

                # Cơ chế Fallback: Nếu không có separate thì lấy consolidated và ngược lại
                if not os.path.exists(file_path):
                    alt_type = "consolidated" if report_type == "separate" else "separate"
                    alt_file_name = self._build_file_name(ticker, year, alt_type)
                    alt_file_path = os.path.join(self.save_json_dir, alt_file_name)
                    if os.path.exists(alt_file_path):
                        file_path = alt_file_path
                        report_id = alt_file_name.replace(".json", "")
                        logger.info(f"Fallback sang {alt_type} cho {ticker} năm {year}")
                    else:
                        logger.warning(f"Không tìm thấy báo cáo nào cho {ticker} năm {year}")
                        continue

                # 2. Quét các bảng trong file JSON
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        chunks = json.load(f)
                except Exception as e:
                    logger.error(f"Lỗi đọc file {file_path}: {e}")
                    continue

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
                            # Chỉ lấy giá trị ở cột đầu tiên (chứa tên chỉ tiêu tài chính) để tránh nhiễu từ các cột số liệu
                            col0_val = str(row.get("0", ""))
                            df_text += col0_val + " "

                            # Kiểm tra xem metric có nằm trọn vẹn trong tên chỉ tiêu của dòng này không
                            if metric.lower() in col0_val.lower():
                                exact_match_in_row = True

                    full_text_to_match = f"{short_context} {df_text}".strip()

                    score = self._calculate_overlap(metric, full_text_to_match)

                    # Boost điểm cực mạnh nếu tên khoản mục xuất hiện nguyên văn trong cột đầu tiên (match trúng chỉ tiêu)
                    if exact_match_in_row:
                        score += 5.0
                    elif metric.lower() in full_text_to_match.lower():
                        score += 2.0

                    start_line = metadata.get("start_line", 0)
                    chunk_scores.append((score, start_line))

                # 3. Lấy Top-K bảng liên quan nhất
                chunk_scores.sort(key=lambda x: x[0], reverse=True)

                # Giới hạn lấy top_k bảng có điểm > 0
                for score, start_line in chunk_scores[:top_k]:
                    if score > 0:
                        results.append(f"{report_id}|{start_line}")

        return list(set(results))  # Loại bỏ trùng lặp nếu có
