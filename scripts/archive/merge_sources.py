import re
import os
import fitz
from html import unescape

def parse_html_symbols():
    html_path = r"c:\Users\Cong\OneDrive - Newcastle University\Documents\Website\IPA\source\all symbols.html"
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    rows = re.findall(r'<tr>(.*?)</tr>', content, re.DOTALL)
    parsed = {}
    for row in rows[1:]:
        tds = re.findall(r'<td.*?>(.*?)</td>', row, re.DOTALL)
        if len(tds) >= 7:
            ipa_num = re.sub(r'<.*?>', '', tds[0]).strip()
            ipa_name = re.sub(r'<.*?>', '', tds[1]).strip()
            char_cell = tds[3]
            
            stripped_char = re.sub(r'<.*?>', '', char_cell).strip()
            char_val = unescape(stripped_char)
            
            usv = re.sub(r'<.*?>', '', tds[4]).strip().upper().zfill(4)
            unicode_name = re.sub(r'<.*?>', '', tds[5]).strip()
            ipa_desc = re.sub(r'<.*?>', '', tds[6]).strip()
            status = re.sub(r'<.*?>', '', tds[7]).strip() if len(tds) > 7 else ""
            
            parsed[usv] = {
                'ipa_num': ipa_num,
                'ipa_name': ipa_name,
                'symbol': char_val,
                'hex_code': usv,
                'unicode_name': unicode_name,
                'ipa_desc': ipa_desc,
                'status': status
            }
    return parsed

def parse_unitipa_pdf():
    pdf_path = r"c:\Users\Cong\OneDrive - Newcastle University\Documents\Website\IPA\IPA_unitipa_sl.pdf"
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text() + "\n"
        
    lines = [line.strip() for line in full_text.split('\n') if line.strip()]
    
    records = []
    current_record = {}
    
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
            i -= 1
        i += 1
        
    if current_record:
        records.append(current_record)
        
    pdf_data = {}
    for r in records:
        hex_val = r.get('hex_value', '').strip().upper().zfill(4)
        if hex_val:
            pdf_data[hex_val] = r
    return pdf_data

def merge():
    html_data = parse_html_symbols()
    pdf_data = parse_unitipa_pdf()
    
    print(f"HTML entries: {len(html_data)}")
    print(f"PDF entries: {len(pdf_data)}")
    
    # Merge
    merged = []
    all_hexes = set(html_data.keys()).union(set(pdf_data.keys()))
    print(f"Total unique hexes: {len(all_hexes)}")
    
    matched = 0
    for hex_code in sorted(all_hexes):
        html_entry = html_data.get(hex_code, {})
        pdf_entry = pdf_data.get(hex_code, {})
        
        # Combine
        symbol = html_entry.get('symbol') or ""
        ipa_num = html_entry.get('ipa_num') or pdf_entry.get('ipa_number') or ""
        ipa_name = html_entry.get('ipa_name') or pdf_entry.get('ipa_name') or ""
        unicode_name = html_entry.get('unicode_name') or pdf_entry.get('unicode_name') or ""
        ipa_desc = html_entry.get('ipa_desc') or pdf_entry.get('name') or ""
        tipa_code = pdf_entry.get('tipa_code') or ""
        afii_code = pdf_entry.get('afii_code') or ""
        
        # If symbol is empty, we can compute it from hex_code
        if not symbol and hex_code:
            try:
                symbol = chr(int(hex_code, 16))
            except ValueError:
                pass
                
        if html_entry and pdf_entry:
            matched += 1
            
        merged.append({
            'hex': hex_code,
            'symbol': symbol,
            'ipa_num': ipa_num,
            'ipa_name': ipa_name,
            'unicode_name': unicode_name,
            'ipa_desc': ipa_desc,
            'tipa': tipa_code,
            'afii': afii_code
        })
        
    print(f"Perfect matches (in both): {matched}")
    print(f"Merged size: {len(merged)}")
    
    # Print 5 that didn't have PDF matches and 5 that didn't have HTML matches
    no_pdf = [m for m in merged if not pdf_data.get(m['hex'])]
    no_html = [m for m in merged if not html_data.get(m['hex'])]
    
    print(f"\nNo PDF match ({len(no_pdf)}):")
    for r in no_pdf[:5]:
        print(f"Hex: {r['hex']} | Symbol: {repr(r['symbol'])} | Name: {r['ipa_name']}")
        
    print(f"\nNo HTML match ({len(no_html)}):")
    for r in no_html[:5]:
        print(f"Hex: {r['hex']} | Name: {r['unicode_name']}")

if __name__ == "__main__":
    merge()
