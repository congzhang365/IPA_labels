import fitz  # PyMuPDF
import re
import os

def parse_unitipa_pdf():
    pdf_path = r"c:\Users\Cong\OneDrive - Newcastle University\Documents\Website\IPA\IPA_unitipa_sl.pdf"
    if not os.path.exists(pdf_path):
        print("PDF does not exist")
        return
        
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text() + "\n"
        
    # Split the text by blocks of "Name:"
    # Let's inspect the layout. Each record looks like:
    # Name:
    # VOICELESS BILABIAL PLOSIVE
    # IPA name:
    # Lower-case P
    # IPA number:
    # 101
    # Unicode name:
    # LATIN SMALL LETTER P
    # Unicode range:
    # Basic Latin
    # Hex value:
    # 0070
    # TIPA code:
    # p
    # AFII code:
    # E2A2
    
    # We can split the text on lines and process page contents.
    lines = [line.strip() for line in full_text.split('\n') if line.strip()]
    
    records = []
    current_record = {}
    last_key = None
    
    # Key-value state machine
    keys_map = {
        'Name:': 'name',
        'IPA name:': 'ipa_name',
        'IPA number:': 'ipa_number',
        'Unicode name:': 'unicode_name',
        'Unicode range:': 'unicode_range',
        'Hex value:': 'hex_value',
        'TIPA code:': 'tipa_code',
        'AFII code:': 'afii_code'
    }
    
    i = 0
    while i < len(lines):
        line = lines[i]
        if line in keys_map:
            key = keys_map[line]
            # The value is usually on the next line or lines
            i += 1
            val_parts = []
            while i < len(lines) and lines[i] not in keys_map:
                val_parts.append(lines[i])
                i += 1
            val = " ".join(val_parts).strip()
            
            if key == 'name':
                if current_record:
                    records.append(current_record)
                current_record = {'name': val}
            else:
                current_record[key] = val
            # decrement i since the outer loop or the inner loop has advanced past the next key
            i -= 1
        i += 1
        
    if current_record:
        records.append(current_record)
        
    print(f"Total parsed records from unitipa PDF: {len(records)}")
    for j, r in enumerate(records[:10]):
        print(f"Record {j+1}: {r}")

if __name__ == "__main__":
    parse_unitipa_pdf()
