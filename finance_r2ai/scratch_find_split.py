import re
from pathlib import Path

def find_split_tables(folder_path):
    txt_files = list(Path(folder_path).rglob("*.txt"))
    for file_path in txt_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Tìm tất cả các đoạn có dạng </table> theo sau là vài khoảng trắng/dòng chữ ngắn và ===== PAGE \d+ ===== rồi lại <table>
        matches = re.finditer(r'</table>\s*(?:[^\n]+\s*){0,3}===== PAGE \d+ =====\s*<table>', content, re.IGNORECASE)
        
        for match in matches:
            print(f"Found in: {file_path}")
            print(f"Context around match:\n{content[max(0, match.start()-100):min(len(content), match.end()+100)]}")
            print("-" * 50)
            return True # Just find one

if __name__ == "__main__":
    find_split_tables(r"C:\vscode\AiFinancialAssistant\finance_r2ai\data\financial_statements\AAA")
