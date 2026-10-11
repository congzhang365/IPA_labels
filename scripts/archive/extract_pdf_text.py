import fitz  # PyMuPDF
import os

def search_pdfs():
    dir_path = r"c:\Users\Cong\OneDrive - Newcastle University\Documents\Website\IPA"
    pdf_files = ['iparef11.pdf', 'phonsymbol.pdf', 'IPA_unitipa_sl.pdf']
    
    for pdf_name in pdf_files:
        path = os.path.join(dir_path, pdf_name)
        if not os.path.exists(path):
            continue
        print(f"\n=== Inspecting {pdf_name} ===")
        doc = fitz.open(path)
        print(f"Number of pages: {len(doc)}")
        
        # Search for key terms across all pages
        terms = ['sampa', 'arpabet', 'tipa', 'af ii', 'afii']
        term_pages = {t: [] for t in terms}
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text().lower()
            for t in terms:
                if t in text:
                    term_pages[t].append(page_num + 1)
        
        for t, pages in term_pages.items():
            if pages:
                print(f"Term '{t}' found in pages: {pages}")
                
        # Let's print out the text of page 1 to see the general content
        print(f"--- Page 1 text preview ({pdf_name}) ---")
        p1_text = doc[0].get_text()
        print(p1_text[:600] + "...")

if __name__ == "__main__":
    search_pdfs()
