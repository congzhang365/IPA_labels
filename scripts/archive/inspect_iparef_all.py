import fitz
import os

def parse_iparef_all():
    pdf_path = r"c:\Users\Cong\OneDrive - Newcastle University\Documents\Website\IPA\iparef11.pdf"
    if not os.path.exists(pdf_path):
        print("PDF does not exist")
        return
        
    doc = fitz.open(pdf_path)
    out_path = r"c:\Users\Cong\OneDrive - Newcastle University\Documents\Website\IPA\iparef11_pages.txt"
    with open(out_path, 'w', encoding='utf-8') as f:
        for page_num in range(1, min(4, len(doc))):
            f.write(f"\n--- PAGE {page_num+1} ---\n")
            f.write(doc[page_num].get_text())
    print(f"Pages 2-4 text saved to {out_path}")

if __name__ == "__main__":
    parse_iparef_all()
