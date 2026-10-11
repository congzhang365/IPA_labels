import re
import os
import fitz
from html import unescape

# Re-use the html and pdf parsing logic
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

def analyze_and_categorize():
    html_data = parse_html_symbols()
    pdf_data = parse_unitipa_pdf()
    
    all_hexes = set(html_data.keys()).union(set(pdf_data.keys()))
    
    types = {}
    
    for hex_code in sorted(all_hexes):
        html_entry = html_data.get(hex_code, {})
        pdf_entry = pdf_data.get(hex_code, {})
        
        ipa_num = html_entry.get('ipa_num') or pdf_entry.get('ipa_number') or ""
        ipa_name = html_entry.get('ipa_name') or pdf_entry.get('ipa_name') or ""
        unicode_name = html_entry.get('unicode_name') or pdf_entry.get('unicode_name') or ""
        ipa_desc = html_entry.get('ipa_desc') or pdf_entry.get('name') or ""
        
        # Determine the type of the symbol
        # We can look at the unicode_name, ipa_num, or ipa_desc
        # Typically:
        # Consonants numbers are in the range 100-199 (some exceptions like ejectives/clicks)
        # Vowels numbers are in the range 300-399 (some exceptions like secondary vowels)
        # Diacritics numbers are in the range 400-499
        # Suprasegmentals numbers are in the range 500-599
        
        desc_lower = ipa_desc.lower()
        u_name_lower = unicode_name.lower()
        
        symbol_type = 'other'
        if any(w in desc_lower for w in ['plosive', 'nasal', 'trill', 'tap', 'flap', 'fricative', 'approximant', 'click', 'implosive', 'ejective']):
            symbol_type = 'consonant'
        elif 'vowel' in desc_lower or any(w in desc_lower for w in ['front', 'back', 'central', 'close', 'open']):
            # diacritics with front/back/close/open should be diacritics
            if 'modifier' in u_name_lower or 'combining' in u_name_lower or 'diacritic' in desc_lower or any(w in desc_lower for w in ['stress', 'long', 'short', 'tone', 'accent', 'release', 'tongue root', 'raised', 'lowered']):
                symbol_type = 'diacritic'
            else:
                symbol_type = 'vowel'
        elif 'modifier' in u_name_lower or 'combining' in u_name_lower or 'diacritic' in desc_lower or any(w in desc_lower for w in ['stress', 'long', 'short', 'tone', 'accent', 'release', 'tongue root', 'raised', 'lowered']):
            symbol_type = 'diacritic'
        
        # Let's override based on IPA number ranges if present
        if ipa_num:
            try:
                num = int(ipa_num.split('+')[0]) # handle composite numbers
                if 100 <= num <= 183:
                    symbol_type = 'consonant'
                elif 301 <= num <= 397:
                    symbol_type = 'vowel'
                elif 401 <= num <= 433:
                    symbol_type = 'diacritic'
                elif 501 <= num <= 512:
                    symbol_type = 'suprasegmental'
            except ValueError:
                pass
                
        # Let's count them
        types[symbol_type] = types.get(symbol_type, 0) + 1
        
        # Parse attributes
        voicing, place, manner = "", "", ""
        height, frontness, roundedness = "", "", ""
        
        if symbol_type == 'consonant':
            # voicing
            if 'voiceless' in desc_lower:
                voicing = 'voiceless'
            elif 'voiced' in desc_lower:
                voicing = 'voiced'
            else:
                voicing = 'voiced' # default for consonants that are voiced by default unless specified
                
            # place
            places = ['bilabial', 'labiodental', 'dental', 'alveolar', 'postalveolar', 'retroflex', 'palatal', 'velar', 'uvular', 'pharyngeal', 'glottal', 'epiglottal', 'alveolo-palatal', 'palatoalveolar', 'labial-velar', 'labial-palatal']
            for p in places:
                if p in desc_lower:
                    place = p
                    break
            if not place:
                # check composites
                if 'labial' in desc_lower:
                    place = 'labial'
                elif 'pharyngealized' in desc_lower:
                    place = 'pharyngeal'
                    
            # manner
            manners = ['plosive', 'nasal', 'trill', 'tap or flap', 'flap', 'tap', 'lateral fricative', 'fricative', 'lateral approximant', 'approximant', 'click', 'implosive', 'ejective']
            for m in manners:
                if m in desc_lower:
                    manner = m
                    break
                    
        elif symbol_type == 'vowel':
            # height
            heights = ['close-mid', 'open-mid', 'near-close', 'near-open', 'close', 'open', 'mid']
            for h in heights:
                if h in desc_lower:
                    height = h
                    break
            
            # frontness
            fronts = ['near-front', 'near-back', 'front', 'back', 'central']
            for f in fronts:
                if f in desc_lower:
                    frontness = f
                    break
                    
            # roundedness
            if 'unrounded' in desc_lower:
                roundedness = 'unrounded'
            elif 'rounded' in desc_lower:
                roundedness = 'rounded'
            elif 'schwa' in desc_lower or 'schwa' in unicode_name.lower():
                roundedness = 'unrounded' # schwa is unrounded
                
        # print some classifications
        if symbol_type == 'consonant' and not place:
            print(f"Consonant with no place: {hex_code} | {unicode_name} | {ipa_desc}")
            
    print("\nSymbol counts by type:")
    for t, count in types.items():
        print(f"{t}: {count}")

if __name__ == "__main__":
    analyze_and_categorize()
