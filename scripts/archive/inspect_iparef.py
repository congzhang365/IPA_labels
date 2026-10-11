import fitz
import os

def parse_iparef():
    pdf_path = r"c:\Users\Cong\OneDrive - Newcastle University\Documents\Website\IPA\iparef11.pdf"
    if not os.path.exists(pdf_path):
        print("PDF does not exist")
        return
        
    doc = fitz.open(pdf_path)
    print(f"iparef11.pdf pages: {len(doc)}")
    
    text = doc[0].get_text()
    out_path = r"c:\Users\Cong\OneDrive - Newcastle University\Documents\Website\IPA\iparef11_page1.txt"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Page 1 text saved to {out_path}")

if __name__ == "__main__":
    parse_iparef()
