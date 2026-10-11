# Instructions for Updating the IPA Labels Database

This project compiles IPA symbol metadata from raw HTML/PDF source documents into a unified UTF-8 encoded CSV database. The CSV is the editable source of truth; the R and Python packages consume generated compressed JSON copies.

Depending on what you want to change, here are the step-by-step instructions.

---

## Scenario A: Directly Editing the Database (Recommended)

If you just want to edit, correct, or add a column or value (such as a TIPA code, SAMPA mapping, or label description), you can edit the CSV file directly:

1. **Edit the main CSV file**:
   Open [ipa_symbols.csv](file:///c:/Users/Cong/OneDrive%20-%20Newcastle%20University/Documents/Website/IPA/ipa_symbols.csv) in any spreadsheet editor (like Excel) or a text editor (like VS Code), make your changes, and save it using **UTF-8 encoding**.

2. **Generate the package databases**:
   Open a terminal at the repository root and run:
   ```bash
   py -3.12 build_package_data.py
   ```
   *(This updates both `python_package/ipa_labels/data/ipa_symbols.json.gz` and `r_package/ipa_labels/inst/extdata/ipa_symbols.json.gz`.)*

3. **Verification**:
   The package loaders read the generated data dynamically at runtime. No package reinstall or compilation is required for local development.

---

## Scenario B: Rebuilding from Raw Source Documents

If you have updated the underlying HTML file [all symbols.html](file:///c:/Users/Cong/OneDrive%20-%20Newcastle%20University/Documents/Website/IPA/source/all%20symbols.html) or the PDF document `IPA_unitipa_sl.pdf` and want to compile a brand new database from scratch:

1. **Update the raw files**:
   Place your new `all symbols.html` inside the `source/` folder, or replace `IPA_unitipa_sl.pdf` in the root folder.

2. **Run the generator script**:
   Open a terminal and run:
   ```bash
   python generate_csv.py
   ```
   *(This reads the source documents, performs the cross-checks, parses the sub-features, merges the datasets, and overwrites the main `ipa_symbols.csv` file)*

3. **Generate the new package databases**:
   Run the database build script:
   ```bash
   py -3.12 build_package_data.py
   ```

4. **Verify changes**:
   Run the verification test script:
   ```bash
   python test_python_package.py
   ```

---

## Package Locations

- Main Database CSV: [ipa_symbols.csv](file:///c:/Users/Cong/OneDrive%20-%20Newcastle%20University/Documents/Website/IPA/ipa_symbols.csv)
- Python Package Source: `python_package/ipa_labels/`
- R Package Source: `r_package/ipa_labels/`
