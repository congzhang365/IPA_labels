import fitz
import os

def parse_phonsymbol():
    pdf_path = r"c:\Users\Cong\OneDrive - Newcastle University\Documents\Website\IPA\phonsymbol.pdf"
    if not os.path.exists(pdf_path):
        print("PDF does not exist")
        return
        
    doc = fitz.open(pdf_path)
    print(f"phonsymbol.pdf pages: {len(doc)}")
    
    # Save the text of page 1 to a utf-8 file to inspect
    text = doc[0].get_text()
    out_path = r"c:\Users\Cong\OneDrive - Newcastle University\Documents\Website\IPA\phonsymbol_page1.txt"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Page 1 text saved to {out_path}")
    
    # Check if there are columns for SAMPA/ARPABET/etc
    terms = ['sampa', 'arpabet', 'tipa', 'afii', 'af ii']
    text_lower = text.lower()
    for t in terms:
        if t in text_lower:
            print(f"Term '{t}' is present on page 1")

if __name__ == "__main__":
    parse_phonsymbol()
