import os
from pathlib import Path

class Settings:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    PATH_CODE_STOCK = str(BASE_DIR / "data" / "code_stock.csv")