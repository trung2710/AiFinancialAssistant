from huggingface_hub import snapshot_download

# Thay "thu_muc_cua_ban" bằng đường dẫn bạn muốn lưu 
# Ví dụ: "./data/ViFinQA" hoặc "D:/Datasets/ViFinQA"
snapshot_download(
    repo_id="AIGuruTinix/ViFinQA", 
    repo_type="dataset", 
    local_dir="/home/manh/Data/data_finance_g2ai"
)