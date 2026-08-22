from src.services.table_retriever import TableRetriever
from src.services.gemini_client import GeminiClient
import os
import sys
import json
import logging
from typing import Dict, Any

# Add project path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Schema for Query Parser
query_parser_schema = {
    "type": "OBJECT",
    "properties": {
        "company_names": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Danh sách tên đầy đủ của các công ty (vd: ['CTCP Tập đoàn Đầu tư Địa ốc No Va'])"
        },
        "tickers": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Danh sách các mã chứng khoán viết tắt (vd: ['NVL'], ['HBC', 'GEX', 'VGC', 'SJG']). Tự động suy ra mã nếu câu hỏi chỉ có tên công ty."
        },
        "years": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Danh sách các năm được nhắc đến (vd: ['2017', '2021', '2023'])"
        },
        "report_type": {
            "type": "STRING",
            "description": "Loại báo cáo (chỉ chọn 1 trong: separate, consolidated, aggregated, explanations)"
        },
        "metric": {
            "type": "STRING",
            "description": "Tên chỉ số/khoản mục tài chính nguyên văn từ câu hỏi"
        },
        "unit": {
            "type": "STRING",
            "description": "Đơn vị tính (vd: triệu đồng, tỷ đồng, phần trăm, hoặc null nếu không nhắc đến)"
        }
    },
    "required": ["company_names", "tickers", "years", "report_type", "metric", "unit"]
}


def parse_query(client: GeminiClient, question: str) -> Dict[str, Any]:
    system_prompt = (
        "Bạn là hệ thống trích xuất thông tin tài chính tự động chính xác tuyệt đối.\n"
        "Nhiệm vụ của bạn là đọc câu hỏi người dùng và trích xuất các trường thông tin theo đúng định dạng JSON yêu cầu.\n\n"
        "Quy tắc trích xuất:\n"
        "1. `company_names`: Mảng chứa tên đầy đủ của các công ty được nhắc đến.\n"
        "2. `tickers`: Mảng chứa các mã chứng khoán (in hoa 3 ký tự, vd: ['NVL'], ['HBC', 'GEX', 'VGC', 'SJG']). Nếu câu hỏi chỉ có tên công ty mà không ghi mã, bạn hãy tự suy ra mã chứng khoán (vd: 'Tập đoàn Hòa Phát' -> 'HPG', 'Vinamilk' -> 'VNM').\n"
        "3. `years`: Mảng danh sách các năm được nhắc đến (dạng chuỗi 4 chữ số, vd: ['2017', '2021']).\n"
        "4. `report_type`: Chỉ chọn 1 trong: 'separate' (nếu nhắc 'công ty mẹ', 'riêng'), 'consolidated' (nếu nhắc 'hợp nhất' hoặc mặc định), 'aggregated' (tổng hợp), 'explanations' (thuyết minh).\n"
        "5. `metric`: Tên khoản mục, chỉ tiêu tài chính nguyên văn trong câu hỏi.\n"
        "6. `unit`: Đơn vị tính được hỏi (triệu đồng, tỷ đồng, phần trăm, hoặc null nếu không nhắc đến).\n\n"
        "Dưới đây là các ví dụ mẫu chuẩn:\n\n"

        "❓ Câu hỏi: Giá trị trung bình của chi phí lãi vay ngắn hạn phải trả vào cuối năm 2022 của CTCP Tập đoàn Xây dựng Hòa Bình (HBC), CTCP Tập đoàn GELEX (GEX), Tổng Công ty Viglacera - CTCP (VGC) và Tổng Công ty Sông Đà - CTCP (SJG) là bao nhiêu tỷ đồng?\n"
        "👉 Trả về:\n"
        "{\n"
        '  "company_names": ["CTCP Tập đoàn Xây dựng Hòa Bình", "CTCP Tập đoàn GELEX", "Tổng Công ty Viglacera - CTCP", "Tổng Công ty Sông Đà - CTCP"],\n'
        '  "tickers": ["HBC", "GEX", "VGC", "SJG"],\n'
        '  "years": ["2022"],\n'
        '  "report_type": "consolidated",\n'
        '  "metric": "chi phí lãi vay ngắn hạn phải trả",\n'
        '  "unit": "tỷ đồng"\n'
        "}\n\n"
        "❓ Câu hỏi: Tỷ trọng doanh thu từ khu vực Lào so với tổng doanh thu toàn công ty của CTCP Hoàng Anh Gia Lai (HAG) trung bình trong các năm 2015, 2016, 2017 và 2022 là bao nhiêu phần trăm?\n"
        "👉 Trả về:\n"
        "{\n"
        '  "company_names": ["CTCP Hoàng Anh Gia Lai"],\n'
        '  "tickers": ["HAG"],\n'
        '  "years": ["2015", "2016", "2017", "2022"],\n'
        '  "report_type": "consolidated",\n'
        '  "metric": "tỷ trọng doanh thu từ khu vực Lào so với tổng doanh thu toàn công ty",\n'
        '  "unit": "phần trăm"\n'
        "}\n\n"
        "❓ Câu hỏi: Giá trị trung bình cộng thuế TNDN đã nộp của Ngân hàng TMCP Ngoại thương Việt Nam (VCB) công ty mẹ qua các năm 2018, 2020, 2021, 2022 và 2025 là bao nhiêu triệu đồng?\n"
        "👉 Trả về:\n"
        "{\n"
        '  "company_names": ["Ngân hàng TMCP Ngoại thương Việt Nam"],\n'
        '  "tickers": ["VCB"],\n'
        '  "years": ["2018", "2020", "2021", "2022", "2025"],\n'
        '  "report_type": "separate",\n'
        '  "metric": "thuế TNDN đã nộp",\n'
        '  "unit": "triệu đồng"\n'
        "}\n\n"
        "❓ Câu hỏi: Trung bình số dư cuối kỳ khoản vay bên liên quan ngắn hạn của CTCP Tập đoàn Kỹ nghệ gỗ Trường Thành (TTF) công ty mẹ trong các năm 2018, 2021, 2022 và 2024 là bao nhiêu tỷ đồng?\n"
        "👉 Trả về:\n"
        "{\n"
        '  "company_names": ["CTCP Tập đoàn Kỹ nghệ gỗ Trường Thành"],\n'
        '  "tickers": ["TTF"],\n'
        '  "years": ["2018", "2021", "2022", "2024"],\n'
        '  "report_type": "separate",\n'
        '  "metric": "số dư cuối kỳ khoản vay bên liên quan ngắn hạn",\n'
        '  "unit": "tỷ đồng"\n'
        "}\n\n"
        "❓ Câu hỏi: Trong số CTCP Tập đoàn PC1 (PC1) – công ty mẹ, Tổng Công ty Viglacera - CTCP (VGC) – công ty mẹ và CTCP SAM Holdings (SAM) – công ty mẹ, vào cuối năm 2016, số công ty có số dư tiền và tương đương tiền ngắn hạn trên 100 tỷ đồng là bao nhiêu?\n"
        "👉 Trả về:\n"
        "{\n"
        '  "company_names": ["CTCP Tập đoàn PC1", "Tổng Công ty Viglacera - CTCP", "CTCP SAM Holdings"],\n'
        '  "tickers": ["PC1", "VGC", "SAM"],\n'
        '  "years": ["2016"],\n'
        '  "report_type": "separate",\n'
        '  "metric": "số dư tiền và tương đương tiền ngắn hạn",\n'
        '  "unit": "tỷ đồng"\n'
        "}\n\n"
        "❓ Câu hỏi: Vào cuối năm nào trong các năm 2016, 2017, 2018 và 2020, vốn chủ sở hữu của Tập đoàn Công nghiệp Cao su Việt Nam - CTCP (GVR) đạt mức cao nhất?\n"
        "👉 Trả về:\n"
        "{\n"
        '  "company_names": ["Tập đoàn Công nghiệp Cao su Việt Nam - CTCP"],\n'
        '  "tickers": ["GVR"],\n'
        '  "years": ["2016", "2017", "2018", "2020"],\n'
        '  "report_type": "consolidated",\n'
        '  "metric": "vốn chủ sở hữu",\n'
        '  "unit": null\n'
        "}"
    )

    response_text = client.generate_content(
        prompt=question,
        model="gemini-3.5-flash-lite",
        system_instruction=system_prompt,
        response_schema=query_parser_schema
    )

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        logger.error(f"Lỗi parse JSON từ Gemini: {response_text}")
        return {}


def generate_pandas_code(client: GeminiClient, question: str, markdown_table: str) -> str:
    system_instruction = (
        "Bạn là chuyên gia tài chính và lập trình Python với thư viện Pandas.\n"
        "Dựa vào Bảng dữ liệu tài chính (dạng Markdown) và Câu hỏi, hãy viết một hàm Python tên `solve(df)` để tính toán và trả về kết quả chính xác.\n\n"
        "Quy tắc bắt buộc:\n"
        "1. Chỉ trả về khối code Python (trong cặp ```python ... ```), tuyệt đối không có văn bản giải thích thêm.\n"
        "2. Định nghĩa hàm luôn là `def solve(df):` với `df` là DataFrame đại diện cho bảng dữ liệu.\n"
        "3. Xử lý an toàn: Lọc dòng theo từ khóa chỉ tiêu không phân biệt hoa thường. Lưu ý: Dữ liệu số trong DataFrame ĐÃ ĐƯỢC CHUẨN HÓA thành dạng số thực/số nguyên chuẩn của Python (ví dụ: -123456.78). TUYỆT ĐỐI KHÔNG DÙNG `.replace('.', '')` vì sẽ làm hỏng phần thập phân. Chỉ cần ép kiểu `float(val)`.\n"
        "4. Chú ý tới đơn vị tính: Bảng có thể đang ở đơn vị VND, hoặc Triệu VND, Tỷ VND. So sánh với đơn vị trong câu hỏi để nhân/chia cho phù hợp (ví dụ hỏi tỷ đồng mà bảng là VND thì chia 1e9).\n\n"
        "Ví dụ mẫu:\n"
        "```python\n"
        "import pandas as pd\n\n"
        "def solve(df):\n"
        "    # Lọc dòng chứa chỉ tiêu và lấy giá trị theo cột năm tương ứng\n"
        "    row = df[df.iloc[:, 0].astype(str).str.contains('Lãi tiền gửi', case=False, na=False)]\n"
        "    if row.empty:\n"
        "        return 0.0\n"
        "    val = row.iloc[0]['31/12/2018'] if '31/12/2018' in df.columns else row.iloc[0, 3]\n"
        "    # Chuyển đổi định dạng số an toàn\n"
        "    clean_val = float(val) if pd.notna(val) and str(val).strip() != '' else 0.0\n"
        "    # Nếu bảng là VND, câu hỏi hỏi Tỷ đồng:\n"
        "    return clean_val / 1e9\n"
        "```"
    )

    prompt = f"BẢNG DỮ LIỆU:\n{markdown_table}\n\nCÂU HỎI: {question}"

    response_text = client.generate_content(
        prompt=prompt,
        model="gemini-3.5-flash-lite",
        system_instruction=system_instruction
    )

    return response_text


def get_markdown_table(report_id: str, start_line: int, save_json_dir: str) -> str:
    """Lấy nội dung markdown của bảng từ file JSON dựa trên report_id và start_line"""
    file_path = os.path.join(save_json_dir, f"{report_id}.json")
    if not os.path.exists(file_path):
        return ""

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)

        for chunk in chunks:
            if chunk.get("metadata", {}).get("start_line") == start_line:
                # Dữ liệu bảng lưu dưới key "dataframe" (list of dicts)
                df_data = chunk.get("dataframe", [])
                if not df_data:
                    return ""
                
                # Chuyển đổi list of dicts thành Markdown table
                headers = list(df_data[0].keys())
                md_table = "|" + "|".join(headers) + "|\n"
                md_table += "|" + "|".join(["---"] * len(headers)) + "|\n"
                for row in df_data:
                    md_table += "|" + "|".join([str(row.get(h, "")).replace("|", "\\|") for h in headers]) + "|\n"
                
                return md_table
    except Exception as e:
        logger.error(f"Lỗi lấy markdown table từ {file_path}: {e}")

    return ""


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_root = os.path.dirname(base_dir)

    input_file = os.path.join(project_root, "instructions", "data", "ViFinQA_train.jsonl")
    output_file = os.path.join(project_root, "instructions", "data", "ViFinQA_finetune.jsonl")

    client = GeminiClient()
    retriever = TableRetriever()
    save_json_dir = retriever.save_json_dir

    logger.info(f"Bắt đầu đọc dữ liệu từ: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f_in, \
            open(output_file, 'w', encoding='utf-8') as f_out:

        # Test với 5 câu đầu tiên theo plan
        count = 0
        max_samples = 5

        for line in f_in:
            if not line.strip():
                continue

            if count >= max_samples:
                break

            try:
                record = json.loads(line)
                question = record.get("question", "")

                logger.info(f"\n--- Đang xử lý câu hỏi {record.get('id', count+1)} ---")
                logger.info(f"Q: {question}")

                # Bước 1: Parse Query
                parsed_query = parse_query(client, question)
                logger.info(f"Parsed: {parsed_query}")

                # Bước 2: Table Retrieval
                retrieval_results = retriever.retrieve(parsed_query, top_k=1)

                if not retrieval_results:
                    logger.warning("Không tìm thấy bảng phù hợp!")
                    continue

                # Lấy bảng top 1
                best_match = retrieval_results[0]
                report_id, start_line_str = best_match.split("|")
                start_line = int(start_line_str)

                markdown_table = get_markdown_table(report_id, start_line, save_json_dir)
                if not markdown_table:
                    logger.warning("Không lấy được nội dung bảng dạng Markdown!")
                    continue

                # Bước 3: Gửi cho Teacher Model sinh code
                logger.info("Đang sinh code Pandas bằng Gemini...")
                pandas_code = generate_pandas_code(client, question, markdown_table)

                # Bước 4: Lưu định dạng ChatML
                chatml_record = {
                    "messages": [
                        {
                            "role": "system",
                            "content": "Bạn là chuyên gia tài chính. Dựa vào Bảng dữ liệu (dạng Markdown), hãy viết code Python bằng thư viện Pandas để trả về kết quả chính xác theo yêu cầu câu hỏi. Tên hàm luôn là `solve(df)`."
                        },
                        {
                            "role": "user",
                            "content": f"BẢNG DỮ LIỆU:\n{markdown_table}\n\nCÂU HỎI: {question}"
                        },
                        {
                            "role": "assistant",
                            "content": pandas_code
                        }
                    ]
                }

                f_out.write(json.dumps(chatml_record, ensure_ascii=False) + "\n")
                logger.info("Lưu thành công!")
                count += 1

                # Nghỉ 4 giây giữa các bản ghi để tránh vượt quá 15 RPM của Gemini Free Tier
                import time
                # Sleep để tránh bị giới hạn API (15 RPM -> nên sleep 10s cho an toàn vì mỗi câu hỏi gọi API 2 lần)
                time.sleep(10)

            except Exception as e:
                logger.error(f"Lỗi xử lý record: {e}")

    logger.info(f"Hoàn tất tạo dataset mẫu. Đã lưu tại: {output_file}")


if __name__ == "__main__":
    main()
