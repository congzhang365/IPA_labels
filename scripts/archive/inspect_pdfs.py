import os

def check_pdf():
    # Try importing common PDF extraction libraries
    libraries = ['pypdf', 'pdfplumber', 'fitz', 'PyPDF2']
    available = []
    for lib in libraries:
        try:
            __import__(lib)
            available.append(lib)
        except ImportError:
            pass
    print("Available PDF libraries:", available)

    pdf_files = ['iparef11.pdf', 'phonsymbol.pdf', 'IPA_unitipa_sl.pdf']
    for pdf in pdf_files:
        path = os.path.join(r"c:\Users\Cong\OneDrive - Newcastle University\Documents\Website\IPA", pdf)
        exists = os.path.exists(path)
        size = os.path.getsize(path) if exists else 0
        print(f"File {pdf}: Exists={exists}, Size={size} bytes")

if __name__ == "__main__":
    check_pdf()
