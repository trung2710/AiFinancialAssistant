import re
import pandas as pd
from bs4 import BeautifulSoup
from unidecode import unidecode
from io import StringIO
from typing import List, Dict, Any


class FinancialTableExtractor:
    def __init__(self, noise_threshold: int = 1):
        self.noise_threshold = noise_threshold

    def _is_noise_text(self, text_chunk: str) -> int:
        lines = [line.strip() for line in text_chunk.split('\n') if line.strip()]
        
        filtered_lines = []
        for line in lines:
            line_lower = line.lower()
            
            # 1. Bỏ qua dòng tên công ty
            if "công ty" in line_lower and ("cổ phần" in line_lower or "trách nhiệm" in line_lower or "tnhh" in line_lower):
                continue
                
            # 2. Bỏ qua dòng tiêu đề báo cáo / header trang
            if any(kw in line_lower for kw in ["bảng cân đối", "kết quả hoạt động", "lưu chuyển tiền", "thuyết minh", "tiếp theo", "báo cáo tài chính", "báo cáo hợp nhất", "báo cáo riêng"]):
                continue
                
            # 3. Bỏ qua ngày tháng, đơn vị tính, mã biểu mẫu
            if any(kw in line_lower for kw in ["đơn vị tính", "vnd", "vnđ", "b01", "b02", "b03", "b09"]):
                continue
            if "ngày" in line_lower and "tháng" in line_lower and "năm" in line_lower:
                continue
            if "cho năm tài chính" in line_lower:
                continue
                
            # 4. Bỏ qua các dòng chỉ chứa số (thường là đánh số trang bị lệch)
            if line.isdigit():
                continue
                
            filtered_lines.append(line)
            
        return len(filtered_lines)

    def _normalize_text(self, text) -> str:
        if pd.isna(text):
            return ""
        return unidecode(str(text)).lower().strip()

    def _is_repeated_header(self, pending_df: pd.DataFrame, df_current: pd.DataFrame) -> bool:
        if df_current.empty:
            return False
        current_first_row = [self._normalize_text(val) for val in df_current.iloc[0]]
        pending_cols = [self._normalize_text(col) for col in pending_df.columns]
        if current_first_row == pending_cols:
            return True
        if not pending_df.empty:
            pending_first_row = [self._normalize_text(val) for val in pending_df.iloc[0]]
            if current_first_row == pending_first_row:
                return True
        return False

    def _extract_table_name_and_unit(self, context_text: str):
        lines = [line.strip() for line in context_text.split('\n') if line.strip()]
        unit = None
        table_name = None
        
        # 1. Quét tìm đơn vị tính
        for line in reversed(lines):
            line_lower = line.lower()
            if "đơn vị tính" in line_lower or "đvt" in line_lower:
                import re
                match = re.search(r'(?i)(?:đơn vị tính|đvt)\s*[:\-\s]\s*(.+)', line)
                if match:
                    unit = match.group(1).strip()
                break
                
        # 2. Quét tìm tên bảng từ dưới lên
        for line in reversed(lines):
            line_lower = line.lower()
            if not line:
                continue
            if "đơn vị tính" in line_lower or "đvt" in line_lower:
                continue
            if "ngày" in line_lower and "tháng" in line_lower and "năm" in line_lower:
                continue
            if "cho năm tài chính" in line_lower:
                continue
            if "b01" in line_lower or "b02" in line_lower or "b03" in line_lower or "b09" in line_lower:
                continue
            if line.isdigit():
                continue
            if "công ty" in line_lower and ("cổ phần" in line_lower or "tnhh" in line_lower):
                continue
                
            table_name = line
            break
            
        return table_name, unit

    def _normalize_value(self, val):
        if pd.isna(val) or val is None:
            return ""
        val_str = str(val).strip()
        if not val_str or val_str == "-":
            return val_str
            
        is_neg = False
        clean_s = val_str
        if clean_s.startswith('(') and clean_s.endswith(')'):
            is_neg = True
            clean_s = clean_s[1:-1].strip()
        elif clean_s.startswith('-'):
            is_neg = True
            clean_s = clean_s[1:].strip()
            
        pattern_thousands = r'^\d{1,3}(?:\.\d{3})+(?:,\d+)?$'
        pattern_decimal_comma = r'^\d+,\d+$'
        pattern_plain_int = r'^\d+$'
        
        if re.match(pattern_thousands, clean_s):
            num_s = clean_s.replace('.', '').replace(',', '.')
            try:
                num = float(num_s)
                if num.is_integer():
                    num = int(num)
                return -num if is_neg else num
            except ValueError:
                return val_str
        elif re.match(pattern_decimal_comma, clean_s):
            num_s = clean_s.replace(',', '.')
            try:
                num = float(num_s)
                return -num if is_neg else num
            except ValueError:
                return val_str
        elif re.match(pattern_plain_int, clean_s):
            try:
                num = int(clean_s)
                return -num if is_neg else num
            except ValueError:
                return val_str
                
        return val_str

    def _normalize_numeric_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df_clean = df.copy()
        for col in df_clean.columns:
            df_clean[col] = df_clean[col].apply(self._normalize_value)
        return df_clean

    def process(self, raw_txt: str, folder_name: str = "") -> tuple:
        # Cắt kẹp chả trực tiếp từ raw_txt để bảo toàn 100% văn bản gốc (kể cả các thẻ ===== PAGE X =====)
        parts = re.split(r'(<table.*?</table>)', raw_txt, flags=re.IGNORECASE | re.DOTALL)

        chunks = []
        pending_chunk = None
        search_offset = 0
        
        part_table_map = {}
        current_chunk_idx = 0

        for i in range(0, len(parts) - 1, 2):
            raw_context_text = parts[i]
            # Xóa tạm marker ngắt trang cho việc tính toán noise_text và trích metadata
            clean_context_text = re.sub(r'===== PAGE \d+ =====', '\n', raw_context_text).strip()
            table_html = parts[i + 1]
            
            # Tìm dòng bắt đầu của bảng
            start_index = raw_txt.find(table_html, search_offset)
            if start_index != -1:
                start_line = raw_txt.count('\n', 0, start_index) + 1
                search_offset = start_index + len(table_html)
            else:
                start_line = None
                
            # Trích xuất tên bảng và đơn vị tính
            table_name, unit = self._extract_table_name_and_unit(clean_context_text)

            try:
                df_current = pd.read_html(StringIO(table_html))[0]
            except ValueError:
                part_table_map[i + 1] = None
                continue

            # Xử lý gộp bảng
            if pending_chunk is not None:
                is_repeated = self._is_repeated_header(pending_chunk['dataframe'], df_current)
                # Tín hiệu gộp bảng: có chữ "tiếp theo" VÀ đi kèm tên loại bảng/báo cáo
                context_lower = clean_context_text.lower()
                has_tiep_theo = "tiếp theo" in context_lower and any(kw in context_lower for kw in ["bảng", "báo cáo", "thuyết minh"])
                
                # Nếu tiêu đề trùng khớp hoàn toàn HOẶC có chữ "tiếp theo"
                allowed_noise = 10 if (is_repeated or has_tiep_theo) else self.noise_threshold

                if (self._is_noise_text(clean_context_text) <= allowed_noise and
                        len(df_current.columns) == len(pending_chunk['dataframe'].columns)):

                    if is_repeated:
                        df_current = df_current.iloc[1:].reset_index(drop=True)

                    df_current.columns = pending_chunk['dataframe'].columns
                    merged_df = pd.concat([pending_chunk['dataframe'], df_current], ignore_index=True)

                    # Cập nhật DataFrame và nối thêm mã HTML gốc của bảng nối trang
                    pending_chunk['dataframe'] = merged_df
                    pending_chunk['raw_table'] += "\n" + table_html
                    part_table_map[i + 1] = current_chunk_idx
                    continue
                else:
                    # Chuẩn hóa số liệu cho pending_chunk trước khi cất
                    pending_chunk['dataframe'] = self._normalize_numeric_df(pending_chunk['dataframe'])
                    chunks.append(pending_chunk)
                    pending_chunk = None

            # Bắt đầu một chunk mới
            if pending_chunk is None:
                current_chunk_idx += 1
                pending_chunk = {
                    'context_text': clean_context_text,
                    'dataframe': df_current,
                    'start_line': start_line,
                    'table_name': table_name,
                    'unit': unit,
                    'chunk_index': current_chunk_idx,
                    'raw_table': table_html
                }
                part_table_map[i + 1] = current_chunk_idx

        if pending_chunk is not None:
            pending_chunk['dataframe'] = self._normalize_numeric_df(pending_chunk['dataframe'])
            chunks.append(pending_chunk)

        # Tạo chuỗi văn bản đồng bộ
        sync_parts = list(parts)
        for i in range(1, len(parts), 2):
            c_idx = part_table_map.get(i)
            if c_idx is not None:
                rel_path = f"tables/{folder_name}/table_{c_idx}.csv" if folder_name else f"table_{c_idx}.csv"
                sync_parts[i] = f"\n[TABLE_{c_idx}]({rel_path})\n"
            else:
                sync_parts[i] = ""
                
        synchronized_text = "".join(sync_parts)

        return chunks, synchronized_text


# ==========================================
# KHU VỰC CHẠY THỬ NGHIỆM (TESTING)
# ==========================================
# if __name__ == "__main__":
#     raw_text = """
#     ===== PAGE 1 =====
#     <table><tr><td></td><td>Năm nay</td><td>Năm trước</td></tr><tr><td>Vốn đầu tư của chủ sở hữu:</td><td></td><td></td></tr><tr><td>- Vốn góp đầu năm</td><td>2.588.678.490.000</td><td>2.588.678.490.000</td></tr><tr><td>- Vốn góp tăng trong năm</td><td></td><td></td></tr><tr><td>- Vốn góp giảm trong năm</td><td></td><td></td></tr><tr><td>- Vốn góp cuối năm</td><td>2.588.678.490.000</td><td>2.588.678.490.000</td></tr><tr><td>Cổ tức, lợi nhuận đã chia</td><td></td><td></td></tr><tr><td>19 . 4. Cổ phiếu</td><td>31/12/2021</td><td>01/01/2021</td></tr><tr><td>Số lượng cổ phiếu đăng ký phát hành</td><td>258.867.849</td><td>258.867.849</td></tr><tr><td>Số lượng cổ phiếu đã bán ra công chúng</td><td>258.867.849</td><td>258.867.849</td></tr><tr><td>- Cổ phiếu phổ thông</td><td>258.867.849</td><td>258.867.849</td></tr><tr><td>- Cổ phiếu ưu đãi</td><td></td><td></td></tr><tr><td>Số lượng cổ phiếu được mua lại</td><td></td><td></td></tr><tr><td>- Cổ phiếu phổ thông</td><td></td><td></td></tr><tr><td>- Cổ phiếu ưu đãi</td><td></td><td></td></tr><tr><td>Số lượng cổ phiếu đang lưu hành</td><td>258.867.849</td><td>258.867.849</td></tr><tr><td>- Cổ phiếu phổ thông</td><td>258.867.849</td><td>258.867.849</td></tr><tr><td>- Cổ phiếu ưu đãi</td><td></td><td></td></tr><tr><td colspan="3">Mệnh giá cổ phiếu đang lưu hành: 10.000 đồng/cổ phiếu</td></tr></table>
#     ===== PAGE 2 =====
#     <table><tr><td>19. 5. Các quỹ của công ty:</td><td>31/12/2021</td><td>01/01/2021</td></tr><tr><td>Quỹ đầu tư phát triển</td><td>86.099.684.648</td><td>78.099.684.648</td></tr><tr><td>Quỹ hỗ trợ sắp xếp doanh nghiệp</td><td></td><td></td></tr><tr><td>Quỹ khác thuộc vốn chủ sở hữu</td><td>4.971.647.795</td><td>4.971.647.795</td></tr></table>
#     """
#
#     # 1. Khởi tạo Pipeline
#     extractor = FinancialTableExtractor(noise_threshold=1)
#
#     # 2. Gọi hàm xử lý
#     results = extractor.process(raw_text)
#
#     # 3. In kết quả
#     for i, df in enumerate(results):
#         print(f"\n--- DATAFRAME THỨ {i+1} ---")
#         print(df.to_string())

