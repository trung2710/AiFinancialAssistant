import pandas as pd
from io import StringIO

html_content = """<table><tr><td rowspan="2"></td><td colspan="2">31/12/2025 (VND)</td><td colspan="2">01/01/2025 (VND)</td></tr><tr><td>Giá gốc</td><td>Giá trị ghi sổ</td><td>Giá gốc</td><td>Giá trị ghi sổ</td></tr><tr><td>Ngắn hạn</td><td>78.000.000.000</td><td>78.000.000.000</td><td>55.000.000.000</td><td>55.000.000.000</td></tr><tr><td>- Tiền gửi có kỳ hạn (*)</td><td>78.000.000.000</td><td>78.000.000.000</td><td>55.000.000.000</td><td>55.000.000.000</td></tr><tr><td>Tổng</td><td>78.000.000.000</td><td>78.000.000.000</td><td>55.000.000.000</td><td>55.000.000.000</td></tr></table>"""

# Đọc bảng bằng pandas
dfs = pd.read_html(StringIO(html_content))
df = dfs[0]

# In DataFrame thu được
print("--- DATAFRAME THU ĐƯỢC ---")
print(df)
print("\n--- XUẤT RA DẠNG CSV ---")
print(df.to_csv(index=False))
