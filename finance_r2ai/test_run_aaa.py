from src.services.financial_document_chunker import FinancialDataPipeline

def run_test():
    print("Đang khởi tạo pipeline...")
    pipeline = FinancialDataPipeline()
    
    test_file = r"C:\vscode\AiFinancialAssistant\finance_r2ai\data\financial_statements\AAA\2025\AAA_financial_statements_2025_consolidated\AAA_financial_statements_2025_consolidated_extracted.txt"
    
    print(f"Đang xử lý file: {test_file}")
    chunks = pipeline.process_chunk(test_file)
    
    print(f"\n================ CÁC BẢNG TRÍCH XUẤT ĐƯỢC ================")
    print(f"Tổng số bảng tìm thấy: {len(chunks)}")
    
    for i, chunk in enumerate(chunks):
        metadata = chunk['metadata']
        df_records = chunk['dataframe']
        context_text = chunk['context_text']
        
        num_columns = len(df_records[0]) if df_records else 0
        
        print(f"\n[Bảng {i+1}] ID: {chunk['chunk_id']}")
        print(f"  - Công ty: {metadata.get('company_name')} ({metadata.get('ticker')})")
        print(f"  - Báo cáo: {metadata.get('report_type')} - Năm: {metadata.get('year')}")
        print(f"  - Số dòng: {len(df_records)} | Số cột: {num_columns}")
        print(f"  - Đường dẫn CSV: {metadata.get('csv_path')}")
        if df_records and len(df_records) > 0:
            print(f"  - Mẫu dữ liệu dòng 1: {df_records[0]}")
        
    print(f"\n✅ Đã chạy xong! Kiểm tra các thư mục trong preprocess:")
    print(f" - CSV tables: finance_r2ai/preprocess/tables/AAA_financial_statements_2025_consolidated/")
    print(f" - Synchronized text: finance_r2ai/preprocess/text/AAA_financial_statements_2025_consolidated_synchronized.txt")
    print(f" - JSON chunks: finance_r2ai/preprocess/json/AAA_financial_statements_2025_consolidated.json")

if __name__ == "__main__":
    run_test()
