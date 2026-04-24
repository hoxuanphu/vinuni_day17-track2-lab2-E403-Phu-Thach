import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Clean the transcript text and extract key information.

def clean_transcript(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # ------------------------------------------
    
    # 1. Xóa bỏ các noise tokens như [Music], [inaudible], [Laughter] và 
    # Pattern này tìm các nội dung nằm trong ngoặc vuông bắt đầu bằng các từ khóa nhiễu
    noise_pattern = r'\[(Music|inaudible|Laughter|source|Speaker).*?\]'
    cleaned_text = re.sub(noise_pattern, '', text)
    
    # 2. Loại bỏ timestamps dạng [00:00:00]
    timestamp_pattern = r'\[\d{2}:\d{2}:\d{2}\]'
    cleaned_text = re.sub(timestamp_pattern, '', cleaned_text)
    
    # Làm sạch khoảng trắng thừa sau khi xóa các token
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    
    # 3. Tìm giá tiền được nhắc đến bằng chữ tiếng Việt ("năm trăm nghìn")
    # Sử dụng search để tìm cụm từ cụ thể trong văn bản gốc
    price_pattern = r'(năm\s+trăm\s+nghìn)'
    match = re.search(price_pattern, text, re.IGNORECASE)
    extracted_price = match.group(1) if match else None
    
    # 4. Trả về dictionary theo UnifiedDocument schema
    price_val = 0
    if extracted_price and "năm trăm nghìn" in extracted_price.lower():
        price_val = 500000

    return {
        "document_id": "transcript-001",
        "content": cleaned_text,
        "source_type": "Video",
        "author": "Speaker",
        "timestamp": None,
        "source_metadata": {
            "source_file": file_path,
            "has_price_info": extracted_price is not None,
            "detected_price_vnd": price_val
        }
    }

# Ví dụ thực thi:
# result = clean_transcript('demo_transcript.txt')
# print(result)