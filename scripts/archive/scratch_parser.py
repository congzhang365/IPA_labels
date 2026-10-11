import re
from html import unescape

def parse_html():
    html_path = r"c:\Users\Cong\OneDrive - Newcastle University\Documents\Website\IPA\source\all symbols.html"
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all table rows
    rows = re.findall(r'<tr>(.*?)</tr>', content, re.DOTALL)
    print(f"Total rows found: {len(rows)}")
    
    parsed = []
    for row in rows[1:]:  # skip header row
        # Find all <td>...</td>
        tds = re.findall(r'<td.*?>(.*?)</td>', row, re.DOTALL)
        if len(tds) >= 7:
            ipa_num = re.sub(r'<.*?>', '', tds[0]).strip()
            ipa_name = re.sub(r'<.*?>', '', tds[1]).strip()
            char_cell = tds[3]
            
            # Remove HTML tags inside the char cell, leaving just the text (which may contain entities)
            stripped_char = re.sub(r'<.*?>', '', char_cell).strip()
            # Decode HTML entities (e.g. &#x0070; -> p)
            char_val = unescape(stripped_char)
            
            usv = re.sub(r'<.*?>', '', tds[4]).strip()
            unicode_name = re.sub(r'<.*?>', '', tds[5]).strip()
            ipa_desc = re.sub(r'<.*?>', '', tds[6]).strip()
            status = re.sub(r'<.*?>', '', tds[7]).strip() if len(tds) > 7 else ""
            
            # Decimal code is the integer value of the hex code/USV
            decimal_code = ""
            if usv:
                try:
                    decimal_code = str(int(usv, 16))
                except ValueError:
                    pass

            parsed.append({
                'ipa_num': ipa_num,
                'ipa_name': ipa_name,
                'symbol': char_val,
                'hex_code': usv,
                'decimal_code': decimal_code,
                'unicode_name': unicode_name,
                'ipa_desc': ipa_desc,
                'status': status
            })
            
    print(f"Successfully parsed {len(parsed)} entries.")
    for i, entry in enumerate(parsed[:10]):
        print(f"{i+1}. IPA:{entry['ipa_num']} | Name:{entry['ipa_name']} | Symbol:{entry['symbol']} | Hex:{entry['hex_code']} | Dec:{entry['decimal_code']} | Desc:{entry['ipa_desc']}")

if __name__ == "__main__":
    parse_html()
