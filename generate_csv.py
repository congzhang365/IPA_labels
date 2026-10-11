import re
import os
import csv
import fitz
from html import unescape

BLOCKS_PATH = r"c:\Users\Cong\OneDrive - Newcastle University\Documents\Website\IPA\resources\Blocks- latest.txt"

def unicode_block(hex_code):
    if not hex_code or "+" in hex_code or not os.path.exists(BLOCKS_PATH):
        return ""
    try:
        codepoint = int(hex_code, 16)
    except ValueError:
        return ""
    with open(BLOCKS_PATH, encoding="utf-8") as stream:
        for line in stream:
            line = line.split("#", 1)[0].strip()
            if not line or ";" not in line:
                continue
            span, name = [part.strip() for part in line.split(";", 1)]
            start, end = [int(part, 16) for part in span.split("..")]
            if start <= codepoint <= end:
                return name
    return "No_Block"

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
    pdf_path = r"c:\Users\Cong\OneDrive - Newcastle University\Documents\Website\IPA\resources\IPA_unitipa_sl.pdf"
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

# Comprehensive X-SAMPA mapping
X_SAMPA_MAP = {
    # Consonants
    'p': 'p', 'b': 'b', 't': 't', 'd': 'd', 'ʈ': 't`', 'ɖ': 'd`', 'c': 'c', 'ɟ': 'J\\',
    'k': 'k', 'g': 'g', 'ɡ': 'g', 'q': 'q', 'ɢ': 'G\\', 'ʔ': '?', 'm': 'm', 'ɱ': 'F',
    'n': 'n', 'ɳ': 'n`', 'ɲ': 'J', 'ŋ': 'N', 'ɴ': 'N\\', 'ʙ': 'B\\', 'r': 'r', 'ʀ': 'R\\',
    'ɾ': '4', 'ɽ': 'r`', 'ɸ': 'p\\', 'β': 'B', 'f': 'f', 'v': 'v', 'θ': 'T', 'ð': 'D',
    's': 's', 'z': 'z', 'ʃ': 'S', 'ʒ': 'Z', 'ʂ': 's`', 'ʐ': 'z`', 'ç': 'C', 'ʝ': 'j\\',
    'x': 'x', 'ɣ': 'G', 'χ': 'X', 'ʁ': 'R', 'ħ': 'X\\', 'ʕ': '?\\', 'h': 'h', 'ɦ': 'h\\',
    'ɬ': 'l\\', 'ɮ': 'I\\', 'ʋ': 'P', 'ɹ': 'r\\', 'ɻ': 'r\\`', 'j': 'j', 'ɰ': 'M\\',
    'l': 'l', 'let': 'l', 'ɭ': 'l`', 'ʎ': 'L', 'ʟ': 'L\\', 'ɓ': 'b_<', 'ɗ': 'd_<',
    'ʄ': 'J\\_<', 'ɠ': 'g_<', 'ʛ': 'G\\_<', 'ʘ': 'O\\', 'ǀ': '|', 'ǃ': '!', 'ǂ': '=',
    'ǁ': '||', 'ɺ': '|\\', 'ɧ': 'x\\', 'w': 'w', 'ʍ': 'w\\', 'ɥ': 'H', 'ʢ': 'H\\',
    'ʡ': '>\\', 'ɕ': 's\\', 'ʑ': 'z\\',
    # Vowels
    'i': 'i', 'y': 'y', 'ɨ': '1', 'ʉ': '}', 'ɯ': 'M', 'u': 'u', 'ɪ': 'I', 'ʏ': 'Y',
    'ʊ': 'U', 'e': 'e', 'ø': '2', 'ɘ': '@\\', 'ɵ': '8', 'ɤ': '7', 'o': 'o', 'ə': '@',
    'ɛ': 'E', 'œ': '9', 'ɜ': '3', 'ɞ': '3\\', 'ʌ': 'V', 'ɔ': 'O', 'æ': '{', 'ɐ': '6',
    'a': 'a', 'ɶ': '&', 'ɑ': 'A', 'ɒ': 'Q',
    # Diacritics / Stress / Length / Tones
    'ˈ': '"', 'ˌ': '%', 'ː': ':', 'ˑ': ':\\', '˘': '_X', '̥': '_0', '̬': '_v', 'ʰ': '_h',
    '̹': '_O', '̜': '_c', '̟': '_+', '̠': '_-', '̈': '_"', '̽': '_x', '̩': '_=', '̯': '_^',
    '˞': '_r', '̤': '_t', '̰': '_a', '̼': '_G', '̪': '_d', '̺': '_a', '̻': '_m', '̃': '_~',
    'ⁿ': '_n', 'ˡ': '_l', 'ʷ': '_w', 'ʲ': '_j', 'ˠ': '_Y', 'ˤ': '_?\\', '̴': '_e', '̚': '_[',
    '̋': '_T', '́': '_H', '̄': '_M', '̀': '_L', '̏': '_B', '̌': '_R', '̂': '_F',
    '̝': '_r', '̞': '_o', '̘': '_A', '̙': '_q'
}

# ARPABET mapping (English phonemes)
ARPABET_MAP = {
    # Vowels
    'i': 'IY', 'ɪ': 'IH', 'e': 'EY', 'ɛ': 'EH', 'æ': 'AE', 'ɑ': 'AA', 'ɒ': 'AO', 'ɔ': 'AO',
    'o': 'OW', 'ʊ': 'UH', 'u': 'UW', 'ʌ': 'AH', 'ə': 'AH', 'ɜ': 'ER', 'ɝ': 'ER', 'a': 'AA',
    # Consonants
    'p': 'P', 'b': 'B', 't': 'T', 'd': 'D', 'k': 'K', 'g': 'G', 'ɡ': 'G', 'm': 'M', 'n': 'N',
    'ŋ': 'NG', 'f': 'F', 'v': 'V', 'θ': 'TH', 'ð': 'DH', 's': 'S', 'z': 'Z', 'ʃ': 'SH',
    'ʒ': 'ZH', 'h': 'HH', 'ɦ': 'HH', 'x': 'KH', 'w': 'W', 'j': 'Y', 'ɹ': 'R', 'r': 'R', 'l': 'L',
    'ʔ': 'Q'
}

# Explicit categories from labels.py
EXPLICIT_CONSONANTS = {
    'p', 'b', 'ɓ', 'ɸ', 'β', 'f', 'v', 'ⱱ', 't', 'd', 'ɗ', 'ʈ', 'ɖ', 'θ', 'ð', 'k', 'ɡ', 'ɠ', 'q', 'ɢ',
    'ʛ', 'x', 'ɣ', 'χ', 'ʁ', 'm', 'ɱ', 'n', 'ɳ', 'ɲ', 'ŋ', 'ɴ', 's', 'z', 'ʃ', 'ʒ', 'ʂ', 'ʐ', 'ɕ', 'ʑ',
    'ç', 'ʝ', 'r', 'ɾ', 'ɽ', 'ʀ', 'ʙ', 'ɺ', 'l', 'ɬ', 'ɮ', 'ɭ', 'ʎ', 'ʟ', 'h', 'ɦ', 'ħ', 'ʕ', 'ʜ', 'ʔ',
    'ʡ', 'ʢ', 'ɧ', 'w', 'ʍ', 'ɥ', 'j', 'ɰ', 'ɹ', 'ɻ', 'ʋ', 'c', 'ɟ', 'ʄ', 'ʘ', 'ǀ', 'ǃ', 'ǂ', 'ǁ'
}

EXPLICIT_VOWELS = {
    'i', 'y', 'ɪ', 'ʏ', 'ɨ', 'ʉ', 'e', 'ə', 'ɘ', 'ɛ', 'ɜ', 'ɞ', 'o', 'ø', 'ɵ', 'ɔ', 'œ', 'a', 'ɑ', 'ɐ',
    'ɒ', 'æ', 'ɶ', 'u', 'ɯ', 'ʊ', 'ʌ', 'ɤ'
}

EXPLICIT_DIACRITICS = {
    'ˈ', 'ˌ', 'ː', 'ˑ', 'ʼ', '˘', '̥', '̬', 'ʰ', '̹', '̜', '̟', '̠', '̈', '̽', '̩', '̯', '˞', '̤', '̰', '̼',
    '̪', '̺', '̻', '̃', 'ⁿ', 'ˡ', 'ʷ', 'ʲ', 'ˠ', 'ˤ', '̴', '̚', '̋', '́', '̄', '̀', '̏', '̌', '̂', '᷄',
    '᷅', '᷈', '͡', '͜', '̝', '̞', '̘', '̙'
}

def generate_csv():
    html_data = parse_html_symbols()
    pdf_data = parse_unitipa_pdf()
    
    print(f"HTML entries: {len(html_data)}")
    print(f"PDF entries: {len(pdf_data)}")
    
    all_hexes = set(html_data.keys()).union(set(pdf_data.keys()))
    print(f"Total unique hex codes: {len(all_hexes)}")
    
    merged = []
    for hex_code in sorted(all_hexes):
        html_entry = html_data.get(hex_code, {})
        pdf_entry = pdf_data.get(hex_code, {})
        
        symbol = html_entry.get('symbol') or ""
        ipa_num = html_entry.get('ipa_num') or pdf_entry.get('ipa_number') or ""
        ipa_name = html_entry.get('ipa_name') or pdf_entry.get('ipa_name') or ""
        unicode_name = html_entry.get('unicode_name') or pdf_entry.get('unicode_name') or ""
        ipa_desc = html_entry.get('ipa_desc') or pdf_entry.get('name') or ""
        tipa_code = pdf_entry.get('tipa_code') or ""
        afii_code = pdf_entry.get('afii_code') or ""
        afii_match = re.search(r"\b([A-Fa-f0-9]{4,6})\b", afii_code)
        afii_code = afii_match.group(1).upper() if afii_match else ""
        unicode_range = pdf_entry.get('unicode_range') or unicode_block(hex_code)
        
        # Format hex code safely
        # E.g. "006B + 02BC" or single "0070"
        if not symbol and hex_code:
            try:
                # If it's a composite hex code
                parts = hex_code.split('+')
                symbol = "".join(chr(int(p.strip(), 16)) for p in parts)
            except ValueError:
                pass
                
        # Classify symbol type
        desc_lower = ipa_desc.lower()
        u_name_lower = unicode_name.lower()
        
        symbol_type = 'other'
        
        # Check explicit first
        if symbol in EXPLICIT_CONSONANTS:
            symbol_type = 'consonant'
        elif symbol in EXPLICIT_VOWELS:
            symbol_type = 'vowel'
        elif symbol in EXPLICIT_DIACRITICS:
            # check if it is a stress marker or length marker -> suprasegmental
            if any(w in desc_lower for w in ['stress', 'long', 'half-long']):
                symbol_type = 'suprasegmental'
            else:
                symbol_type = 'diacritic'
        else:
            # Fallback range-based and description-based classification
            # Stress, length, tone marks, group marks -> suprasegmental
            if any(w in desc_lower or w in u_name_lower for w in ['stress', 'long', 'half-long', 'tone mark', 'vertical line', 'undertie']):
                symbol_type = 'suprasegmental'
            elif 'combining' in u_name_lower or 'modifier' in u_name_lower or 'diacritic' in desc_lower or any(w in desc_lower for w in ['release', 'tongue root', 'raised', 'lowered']):
                symbol_type = 'diacritic'
            elif any(w in desc_lower for w in ['plosive', 'nasal', 'trill', 'tap', 'flap', 'fricative', 'approximant', 'click', 'implosive', 'ejective']):
                symbol_type = 'consonant'
            elif 'vowel' in desc_lower or any(w in desc_lower for w in ['front', 'back', 'central', 'close', 'open']):
                symbol_type = 'vowel'
            
        # Refine by IPA number if we have it
        if ipa_num:
            try:
                num = int(ipa_num.split('+')[0].strip())
                if 100 <= num <= 199:
                    symbol_type = 'consonant'
                elif 300 <= num <= 399:
                    symbol_type = 'vowel'
                elif 400 <= num <= 499:
                    symbol_type = 'diacritic'
                elif 500 <= num <= 599:
                    symbol_type = 'suprasegmental'
            except ValueError:
                pass
                
        # Parse features
        voicing, place, manner = "", "", ""
        height, closeness, openness, frontness, roundedness = "", "", "", "", ""
        description = ipa_desc
        
        if symbol_type == 'consonant':
            # voicing
            if 'voiceless' in desc_lower:
                voicing = 'voiceless'
            elif 'voiced' in desc_lower:
                voicing = 'voiced'
            else:
                # default click/implosives/ejectives
                if 'click' in desc_lower or 'implosive' in desc_lower:
                    voicing = 'voiced'
                else:
                    voicing = 'voiced' if 'voiced' in desc_lower or not 'voiceless' in desc_lower else 'voiceless'
                    
            # place
            places = ['bilabial', 'labiodental', 'dental', 'alveolar', 'postalveolar', 'retroflex', 'palatal', 'velar', 'uvular', 'pharyngeal', 'glottal', 'epiglottal', 'alveolo-palatal', 'palatoalveolar', 'labial-velar', 'labial-palatal']
            for p in places:
                if p in desc_lower:
                    place = p
                    break
            if not place:
                if 'labial' in desc_lower:
                    place = 'labial'
                elif 'pharyngeal' in desc_lower:
                    place = 'pharyngeal'
                    
            # manner
            manners = ['plosive', 'nasal', 'trill', 'tap or flap', 'flap', 'tap', 'lateral fricative', 'fricative', 'lateral approximant', 'approximant', 'click', 'implosive', 'ejective']
            for m in manners:
                if m in desc_lower:
                    manner = m
                    break
            if not manner:
                if 'fricatives' in desc_lower:
                    manner = 'fricative'
                elif 'approximants' in desc_lower:
                    manner = 'approximant'
                    
        elif symbol_type == 'vowel':
            # height / closeness / openness - make them all available
            heights = ['close-mid', 'open-mid', 'near-close', 'near-open', 'close', 'open', 'mid']
            for h in heights:
                if h in desc_lower:
                    height = h
                    closeness = h
                    openness = h
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
            elif 'schwa' in desc_lower or 'schwa' in u_name_lower:
                roundedness = 'unrounded'
                
        # Decimal code calculation
        decimal_code = ""
        if hex_code and '+' not in hex_code:
            try:
                decimal_code = str(int(hex_code, 16))
            except ValueError:
                pass
                
        # USV code calculation (e.g., U+0070 or U+006B + U+02BC)
        usv_code = ""
        if hex_code:
            parts = hex_code.split('+')
            usv_code = " + ".join(f"U+{p.strip()}" for p in parts)
                
        # SAMPA and ARPABET mapping
        sampa = X_SAMPA_MAP.get(symbol, "")
        arpabet = ARPABET_MAP.get(symbol, "")
        
        # Fallback mappings for composite or spacing modifier characters if possible
        if not sampa and symbol:
            # try to build if it's a composite (like t͡ʃ or kʼ)
            # ejectives
            if symbol.endswith('ʼ'):
                base = symbol[:-1]
                if base in X_SAMPA_MAP:
                    sampa = X_SAMPA_MAP[base] + '_>'
            elif len(symbol) == 1:
                # check if there's a lowercase ASCII equivalent
                if ord(symbol) < 128:
                    sampa = symbol
                    
        merged.append({
            'symbol': symbol,
            'ipa_number': ipa_num,
            'usv_code': usv_code,
            'hex_code': hex_code,
            'decimal_code': decimal_code,
            'tipa': tipa_code,
            'af_ii': afii_code,
            'ipa_name': ipa_name,
            'unicode_name': unicode_name,
            'unicode_range': unicode_range,
            'type': symbol_type,
            'voicing': voicing,
            'place': place,
            'manner': manner,
            'height': height,
            'closeness': closeness,
            'openness': openness,
            'frontness': frontness,
            'roundedness': roundedness,
            'description': description,
            'sampa': sampa,
            'arpabet': arpabet
        })
        
    # Write to CSV
    csv_path = r"c:\Users\Cong\OneDrive - Newcastle University\Documents\Website\IPA\ipa_symbols.csv"
    
    headers = [
        'symbol', 'ipa_number', 'usv_code', 'hex_code', 'decimal_code', 'tipa', 'af_ii',
        'ipa_name', 'unicode_name', 'unicode_range', 'type', 'voicing', 'place', 'manner',
        'height', 'closeness', 'openness', 'frontness', 'roundedness',
        'description', 'sampa', 'arpabet'
    ]
    
    with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for r in merged:
            writer.writerow(r)
            
    print(f"Successfully generated CSV at {csv_path} with {len(merged)} records.")

if __name__ == "__main__":
    generate_csv()
