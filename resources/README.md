# Reference resources

These files are local reference material used to check `ipa_symbols.csv`.
They are not installed as part of either package.

| File | Role |
| --- | --- |
| `accessiblechart.html` | Unicode IPA chart; the file contains its own MIT notice. |
| `IPA_unitipa_sl.pdf` | TIPA, AFII, Unicode, and IPA-label reference. |
| `iparef11.pdf` | Hagiwara reference chart for IPA typography. |
| `phonsymbol.pdf` | SIL Unicode phonetic-symbol reference. |
| `IPA Symbol Equivalents - Writing Systems Technical Resources.url` | Link to the SIL/Writing Systems Technical Resources reference page. |
| `iparef11_page1.txt` | Extracted text from page 1 of `iparef11.pdf`. |
| `iparef11_pages.txt` | Extracted text from pages 2–4 of `iparef11.pdf`. |
| `phonsymbol_page1.txt` | Extracted text from page 1 of `phonsymbol.pdf`. |
| `phoible-v2.0.1.zip` / `phoible-extracted/` | Pinned PHOIBLE 2.0.1 source used to generate segment features and inventories. |
| `Blocks- latest.txt` | Machine-readable Unicode block data used to add `unicode_range`. |

The extracted text files are convenience copies, not separate sources. Their
relationship to the PDFs is checked by `scripts/validate_resources.py`.

The reference files have different authors and licensing terms. Check each
source's own notice before redistributing the source files or copying
substantial expressive content. The package does not redistribute these files.

PHOIBLE 2.0.1 is attributed to the PHOIBLE project and its contributors and is
used under its CC BY 4.0 data licence. Unicode block data is from the Unicode
Character Database. The generated package data records these sources so that
feature and inventory provenance remains explicit.
