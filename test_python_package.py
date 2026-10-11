import sys
import os
import csv
import shutil
import tempfile

# Append the python_package directory to sys.path to test it before installation
pkg_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "python_package"))
sys.path.insert(0, pkg_dir)

import ipa_labels

def safe_print(label, obj):
    """Safely print objects containing unicode characters to cp1252 consoles."""
    s = f"{label} {repr(obj)}"
    print(s.encode('ascii', 'backslashreplace').decode('ascii'))

def run_tests():
    print("=== Testing Python Package ipa_labels ===")

    # Test 0: Public package metadata is available
    print("\nTest 0: Check package version...")
    assert ipa_labels.__version__ == '0.2.0'

    # Structured groups, aliases, defaults, and PHOIBLE features.
    p = ipa_labels.get("p")
    assert p.symbol.ipa == "p"
    assert p.code.unicode == p.code.usv
    assert p.code.default == p.code.tipa
    assert p.label.default == p.label.full
    assert p.label.place == "bilabial"
    assert p.features.consonantal is True
    assert p.features.labial is True
    assert p.features.nasal is False
    assert p.description.ipa_name and p.description.unicode_name
    assert ipa_labels.lookup(code={"unicode": "U+0070"}, fields="symbol") == ["p"]
    assert ipa_labels.lookup(label={"place": "bilabial"}, fields="symbol")
    assert ipa_labels.get("not-a-symbol") is None
    assert len(ipa_labels.inventory(iso639_3="eng")) > 1

    # Test convenience accessors
    assert ipa_labels.get("p", "place") == "bilabial"
    places = ipa_labels.values("place", type="consonant", unique=True)
    assert "bilabial" in places
    assert "" not in places
    
    # Test 1: Query for symbol 'p' and verify its values
    print("\nTest 1: Lookup symbol 'p' details...")
    p_details = ipa_labels.lookup(symbol='p')
    if p_details:
        safe_print("Success! Details for 'p':", p_details[0])
        # Validate properties
        assert p_details[0]['tipa'] == 'p', f"Expected TIPA 'p', got {p_details[0]['tipa']}"
        assert p_details[0]['voicing'] == 'voiceless', f"Expected voicing 'voiceless', got {p_details[0]['voicing']}"
    else:
        print("Failed: No details found for 'p'")
        sys.exit(1)
        
    # Test 2: Structured search by features
    print("\nTest 2: Lookup voiceless velar plosive symbol...")
    symbols = ipa_labels.lookup(voicing='voiceless', place='velar', manner='plosive', fields='symbol')
    safe_print("Results:", symbols)
    assert 'k' in symbols, "Expected 'k' in symbols"
    
    # Test 3: Free-text search matching multiple terms
    print("\nTest 3: Query for 'voiced bilabial plosive'...")
    b_matches = ipa_labels.query('voiced bilabial plosive', fields='symbol')
    safe_print("Results:", b_matches)
    assert 'b' in b_matches, "Expected 'b' in matches"
    
    # Test 4: Query by IPA Name 'Esh'
    print("\nTest 4: Query for 'Esh'...")
    esh_matches = ipa_labels.query('Esh', fields='symbol')
    safe_print("Results:", esh_matches)
    assert 'ʃ' in esh_matches, "Expected 'ʃ' (Esh) in matches"
    
    # Test 5: Verify height/closeness/openness vowel fields are available
    print("\nTest 5: Checking height/closeness/openness vowel fields for 'i'...")
    i_details = ipa_labels.lookup(symbol='i')[0]
    print(f"Symbol 'i': height={i_details['height']}, closeness={i_details['closeness']}, openness={i_details['openness']}")
    assert i_details['height'] == 'close', "Expected height to be 'close'"
    assert i_details['closeness'] == 'close', "Expected closeness to be 'close'"
    assert i_details['openness'] == 'close', "Expected openness to be 'close'"

    # Test 6: Invalid fields fail clearly instead of silently returning no data
    print("\nTest 6: Validate invalid field handling...")
    try:
        ipa_labels.lookup(fields='not_a_real_field')
    except ValueError as exc:
        assert "not_a_real_field" in str(exc)
    else:
        raise AssertionError("Expected invalid output field to raise ValueError")

    try:
        ipa_labels.lookup(not_a_real_field='value')
    except ValueError as exc:
        assert "not_a_real_field" in str(exc)
    else:
        raise AssertionError("Expected invalid search field to raise ValueError")

    try:
        ipa_labels.lookup(criteria=['type', 'vowel'])
    except TypeError:
        pass
    else:
        raise AssertionError("Expected non-dictionary criteria to raise TypeError")

    try:
        ipa_labels.query('', fields='not_a_real_field')
    except ValueError as exc:
        assert "not_a_real_field" in str(exc)
    else:
        raise AssertionError("Expected empty query with invalid field to raise ValueError")
    print("Invalid field handling verified.")

    # Test 7: Custom CSV paths and runtime reloads
    print("\nTest 7: Verify custom CSV path and dynamic reload...")
    source_csv = os.path.join(pkg_dir, "ipa_labels", "data", "ipa_symbols.csv")
    with tempfile.TemporaryDirectory(dir=os.path.dirname(__file__)) as temp_dir:
        custom_csv = os.path.join(temp_dir, "ipa_symbols.csv")
        shutil.copy2(source_csv, custom_csv)
        custom_lookup = ipa_labels.IPALookup(csv_path=custom_csv)

        assert custom_lookup.lookup(symbol='p'), "Custom CSV path should load existing records"
        assert not custom_lookup.lookup(symbol='TEST_DYNAMIC_RECORD')

        with open(custom_csv, mode='r', encoding='utf-8', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            rows = list(reader)
            fieldnames = reader.fieldnames
        new_row = {field: '' for field in fieldnames}
        new_row.update({
            'symbol': 'TEST_DYNAMIC_RECORD',
            'ipa_name': 'Synthetic test record',
            'description': 'Synthetic test record'
        })
        with open(custom_csv, mode='w', encoding='utf-8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
            writer.writerow(new_row)

        reloaded = custom_lookup.lookup(symbol='TEST_DYNAMIC_RECORD')
        assert len(reloaded) == 1, "Lookup should reload changes made to the CSV"
    print("Custom path and dynamic reload verified.")
    
    print("\n=== All Python tests passed successfully! ===")

if __name__ == "__main__":
    run_tests()
