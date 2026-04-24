import ast
import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract docstrings and comments from legacy Python code.

def extract_logic_from_code(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    # ------------------------------------------
    
    # Kết quả trả về theo UnifiedDocument schema
    extracted_data = {
        "functions": [],
        "business_rules": [],
        "metadata": {"source": file_path}
    }

    try:
        # Sử dụng 'ast' để parse source code thành cây cú pháp
        tree = ast.parse(source_code)

        # 1. Tìm docstrings của các hàm bằng AST
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node)
                extracted_data["functions"].append({
                    "name": node.name,
                    "docstring": docstring if docstring else "No docstring provided",
                    "lineno": node.lineno
                })

        # 2. Sử dụng regex để tìm business rules trong comments
        # Pattern này tìm các comment bắt đầu bằng "# Business Logic Rule"
        rule_pattern = r"#\s*(Business Logic Rule\s*\d+[:\-]?\s*.*)"
        rules = re.findall(rule_pattern, source_code, re.IGNORECASE)
        
        for rule in rules:
            extracted_data["business_rules"].append(rule.strip())

    except SyntaxError as e:
        return {"error": f"Failed to parse Python code: {str(e)}"}
    
    return extracted_data

# Ví dụ test nhanh
# result = extract_logic_from_code('path/to/your/legacy_script.py')
# print(result)