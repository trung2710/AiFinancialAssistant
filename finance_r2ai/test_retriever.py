from src.services.table_retriever import TableRetriever
import os
import sys

# Thêm đường dẫn project vào sys.path để import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main():
    retriever = TableRetriever()

    # Giả lập kết quả trả về từ Tầng 1 (Query Parser)
    # Dựa theo câu hỏi: "Trong số CTCP Tập đoàn PC1 (PC1) – công ty mẹ, Tổng Công ty Viglacera - CTCP (VGC) – công ty mẹ và CTCP SAM Holdings (SAM) – công ty mẹ, vào cuối năm 2016, số công ty có số dư tiền và tương đương tiền ngắn hạn trên 100 tỷ đồng là bao nhiêu?"

    parsed_query = {
        'company_names': ['CTCP Hàng không Vietjet'],
        'tickers': ['VJC'],
        'years': ['2018'],
        'report_type': 'separate',
        'metric': 'Lãi tiền gửi',
        'unit': 'triệu đồng'
    }

    print("=" * 50)
    print("Bắt đầu test TableRetriever")
    print(f"Parsed Query: {parsed_query}")
    print("-" * 50)

    results = retriever.retrieve(parsed_query, top_k=2)

    print("Kết quả (ID Báo Cáo | Dòng bắt đầu):")
    for r in results:
        print(f" => {r}")

    print("=" * 50)


if __name__ == "__main__":
    main()
