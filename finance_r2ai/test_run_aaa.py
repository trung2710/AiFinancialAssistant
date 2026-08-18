import os
import json
from src.services.financial_document_chunker import FinancialDataPipeline

def run_test():
    # Khởi tạo pipeline
    print("Đang khởi tạo pipeline...")
    pipeline = FinancialDataPipeline()
    
    # Đường dẫn file cần test
    test_file = r"C:\vscode\AiFinancialAssistant\finance_r2ai\data\financial_statements\AAA\2025\AAA_financial_statements_2025_consolidated\AAA_financial_statements_2025_consolidated_extracted.txt"
    
    print(f"Đang xử lý file: {test_file}")
    chunks = pipeline.process_chunk(test_file)
    
    print(f"\n================ CÁC BẢNG TRÍCH XUẤT ĐƯỢC ================")
    print(f"Tổng số bảng tìm thấy: {len(chunks)}")
    
    # In ra một số thông tin để kiểm chứng
    for i, chunk in enumerate(chunks):
        metadata = chunk['metadata']
        df_records = chunk['dataframe']
        context_text = chunk['context_text']
        
        # Đếm số lượng cột dựa trên record đầu tiên
        num_columns = len(df_records[0]) if df_records else 0
        
        print(f"\n[Bảng {i+1}] ID: {chunk['chunk_id']}")
        print(f"  - Công ty: {metadata.get('company_name')} ({metadata.get('ticker')})")
        print(f"  - Báo cáo: {metadata.get('report_type')} - Năm: {metadata.get('year')}")
        print(f"  - Số dòng: {len(df_records)} | Số cột: {num_columns}")
        print(f"  - Text nối ở trên (100 ký tự đầu): {repr(context_text[:100])}...")
        
    # Lưu kết quả ra file JSON
    output_file = "test_output_aaa.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=4)
        
    print(f"\n✅ Đã chạy xong! Toàn bộ dữ liệu chi tiết đã được lưu vào file: {output_file}")

if __name__ == "__main__":
    run_test()
