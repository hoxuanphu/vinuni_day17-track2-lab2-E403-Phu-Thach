import pandas as pd

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Process sales records, handling type traps and duplicates.

def process_sales_csv(file_path):
    # --- FILE READING (Handled for students) ---
    df = pd.read_csv(file_path)
    # ------------------------------------------
    
    # Remove duplicate rows based on 'id'
    df = df.drop_duplicates(subset=['id'])
    
    # Clean 'price' column
    def clean_price(price):
        if pd.isna(price):
            return 0.0
        price_str = str(price).lower().strip()
        
        # Mapping for text numbers
        text_nums = {
            "five dollars": 5.0,
            "ten dollars": 10.0,
            # Add more if needed based on data
        }
        if price_str in text_nums:
            return text_nums[price_str]
            
        # Remove currency symbols and commas
        price_str = re.sub(r'[^\d\.\-]', '', price_str)
        
        try:
            val = float(price_str)
            return abs(val) # Assuming prices should be positive
        except ValueError:
            return 0.0

    import re
    df['price'] = df['price'].apply(clean_price)
    
    # Normalize 'date_of_sale'
    def normalize_date(date_str):
        if pd.isna(date_str):
            return None
        try:
            # Try various formats using pandas to_datetime
            return pd.to_datetime(date_str).strftime('%Y-%m-%d')
        except:
            return None

    df['date_of_sale'] = df['date_of_sale'].apply(normalize_date)
    
    # Return a list of dictionaries for the UnifiedDocument schema.
    results = []
    for _, row in df.iterrows():
        doc = {
            "document_id": f"csv-sale-{row['id']}",
            "content": f"Sale of {row['product_name']} in category {row['category']} for price {row['price']}",
            "source_type": "CSV",
            "author": f"Seller {row['seller_id']}",
            "timestamp": row['date_of_sale'],
            "source_metadata": {
                "product_name": row['product_name'],
                "category": row['category'],
                "price": row['price'],
                "stock": row['stock_quantity']
            }
        }
        results.append(doc)
    
    return results

