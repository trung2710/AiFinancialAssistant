import os
import json
from pathlib import Path
from huggingface_hub import snapshot_download

# Đường dẫn thư mục đích
data_root = Path("/home/newuser/Code/AiFinancialAssistant/instructions/data")
data_root.mkdir(parents=True, exist_ok=True)

print(f"Downloading entire ViFinQA dataset (questions, financial_statements, code_stock) to: {data_root} ...")
snapshot_download(
    repo_id="AIGuruTinix/ViFinQA",
    repo_type="dataset",
    local_dir=str(data_root),
    local_dir_use_symlinks=False
)

print("\n--- Kiểm tra dữ liệu đã tải ---")

# Đọc questions
questions_file = data_root / "questions" / "questions.jsonl"
if questions_file.exists():
    with questions_file.open(encoding="utf-8") as file:
        questions = [json.loads(line) for line in file if line.strip()]
    print(f"Tổng số câu hỏi: {len(questions)}")
    print(f"First question: {questions[0]}")

# Quét danh sách báo cáo tài chính
statement_paths = sorted((data_root / "financial_statements").glob("*/*/*/*.txt"))
print(f"Tổng số file báo cáo tài chính (.txt): {len(statement_paths)}")

if statement_paths:
    first_statement = statement_paths[0].read_text(encoding="utf-8", errors="replace")
    print(f"\nFirst statement path: {statement_paths[0]}")
    print(f"First 300 chars of statement:\n{first_statement[:300]}")

print("\nTất cả dữ liệu đã được tải về thành công vào thư mục:", data_root)
