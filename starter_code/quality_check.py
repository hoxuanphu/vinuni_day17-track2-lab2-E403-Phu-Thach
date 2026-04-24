# ==========================================
# ROLE 3: OBSERVABILITY & QA ENGINEER
# ==========================================
# Task: Implement quality gates to reject corrupt data or logic discrepancies.

def run_quality_gate(document_dict):
    # Reject documents with 'content' length < 20 characters
    if len(document_dict.get('content', '')) < 20:
        return False

    # Reject documents containing toxic/error strings (e.g., 'Null pointer exception')
    toxic_strings = ['null pointer exception', 'error', 'exception', 'corrupt', 'invalid']
    content_lower = document_dict.get('content', '').lower()
    if any(toxic in content_lower for toxic in toxic_strings):
        return False

    # Flag discrepancies (e.g., if tax calculation comment says 8% but code says 10%)
    # For code documents, check for tax rate discrepancies
    if document_dict.get('source_type') == 'Code':
        source_metadata = document_dict.get('source_metadata', {})
        warnings = source_metadata.get('warnings', [])
        for warning in warnings:
            if 'tax' in warning.lower() and ('8%' in warning and '10%' in warning):
                return False  # Flag as discrepancy

    # Return True if pass, False if fail.
    return True
