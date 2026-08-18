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

    def process(self, raw_txt: str) -> List[Dict[str, Any]]:
        # Xóa marker ngắt trang để nối liền văn bản
        cleaned_text = re.sub(r'===== PAGE \d+ =====', '\n', raw_txt)

        # Cắt kẹp chả: Text -> Table -> Text -> Table
        parts = re.split(r'(<table.*?</table>)', cleaned_text, flags=re.IGNORECASE | re.DOTALL)

        chunks = []
        pending_chunk = None
        search_offset = 0

        for i in range(0, len(parts) - 1, 2):
            context_text = parts[i].strip()
            table_html = parts[i + 1]
            
            # Tìm dòng bắt đầu của bảng
            start_index = raw_txt.find(table_html, search_offset)
            if start_index != -1:
                start_line = raw_txt.count('\n', 0, start_index) + 1
                search_offset = start_index + len(table_html)
            else:
                start_line = None
                
            # Trích xuất tên bảng và đơn vị tính
            table_name, unit = self._extract_table_name_and_unit(context_text)

            try:
                df_current = pd.read_html(StringIO(table_html))[0]
            except ValueError:
                continue

            # Xử lý gộp bảng
            if pending_chunk is not None:
                is_repeated = self._is_repeated_header(pending_chunk['dataframe'], df_current)
                # Tín hiệu gộp bảng: có chữ "tiếp theo" VÀ đi kèm tên loại bảng/báo cáo
                context_lower = context_text.lower()
                has_tiep_theo = "tiếp theo" in context_lower and any(kw in context_lower for kw in ["bảng", "báo cáo", "thuyết minh"])
                
                # Nếu tiêu đề trùng khớp hoàn toàn HOẶC có chữ "tiếp theo"
                allowed_noise = 10 if (is_repeated or has_tiep_theo) else self.noise_threshold

                if (self._is_noise_text(context_text) <= allowed_noise and
                        len(df_current.columns) == len(pending_chunk['dataframe'].columns)):

                    if is_repeated:
                        df_current = df_current.iloc[1:].reset_index(drop=True)

                    df_current.columns = pending_chunk['dataframe'].columns
                    merged_df = pd.concat([pending_chunk['dataframe'], df_current], ignore_index=True)

                    # Cập nhật DataFrame, Giữ nguyên đoạn context_text gốc của bảng đầu tiên
                    pending_chunk['dataframe'] = merged_df
                    continue
                else:
                    chunks.append(pending_chunk)
                    pending_chunk = None

            # Bắt đầu một chunk mới
            if pending_chunk is None:
                pending_chunk = {
                    'context_text': context_text,
                    'dataframe': df_current,
                    'start_line': start_line,
                    'table_name': table_name,
                    'unit': unit
                }

        if pending_chunk is not None:
            chunks.append(pending_chunk)

        return chunks


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

