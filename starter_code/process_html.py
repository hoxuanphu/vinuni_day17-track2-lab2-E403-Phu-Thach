from bs4 import BeautifulSoup

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract product data from the HTML table, ignoring boilerplate.

def parse_html_catalog(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    # ------------------------------------------
    
    # Use BeautifulSoup to find the table with id 'main-catalog'
    table = soup.find('table', id='main-catalog')
    if not table:
        return []
    
    results = []
    # Extract rows, handling 'N/A' or 'Liên hệ' in the price column.
    rows = table.find('tbody').find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 6:
            continue
            
        product_id = cols[0].get_text(strip=True)
        product_name = cols[1].get_text(strip=True)
        category = cols[2].get_text(strip=True)
        price_raw = cols[3].get_text(strip=True)
        stock = cols[4].get_text(strip=True)
        rating = cols[5].get_text(strip=True)
        
        # Clean price
        price_val = 0.0
        if price_raw not in ['N/A', 'Liên hệ']:
            # Remove "VND" and commas
            price_clean = price_raw.replace('VND', '').replace(',', '').strip()
            try:
                price_val = float(price_clean)
            except ValueError:
                price_val = 0.0
        
        doc = {
            "document_id": f"html-product-{product_id}",
            "content": f"Product {product_name} in category {category}. Price: {price_raw}. Stock: {stock}. Rating: {rating}.",
            "source_type": "HTML",
            "author": "VinShop System",
            "timestamp": None,
            "source_metadata": {
                "product_id": product_id,
                "product_name": product_name,
                "category": category,
                "price": price_val,
                "stock": stock,
                "rating": rating
            }
        }
        results.append(doc)
    
    return results

