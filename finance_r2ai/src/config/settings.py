import os
from pathlib import Path

class Settings:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    PROJECT_ROOT = BASE_DIR.parent
    
    PATH_CODE_STOCK = str(PROJECT_ROOT / "instructions" / "data" / "code_stock.csv")
    
    FINANCIAL_STATEMENTS_DIR = str(PROJECT_ROOT / "instructions" / "data" / "financial_statements")
    SAVE_JSON_DIR = str(BASE_DIR / "save_json")
    PREPROCESS_DIR = str(BASE_DIR / "preprocess")