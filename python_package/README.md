# ipa_labels

A comprehensive, multilayered phonetic database and lookup utility for the International Phonetic Alphabet (IPA).

Version 0.2 adds structured records, PHOIBLE segment features, Unicode block
names, and versioned PHOIBLE language inventories.

`ipa_labels` allows you to look up IPA symbols by their descriptions, names, Hex/Decimal values, TIPA LaTeX macros, AF II codes, SAMPA/X-SAMPA representation, and ARPABET mappings. It provides a simple API for both structured queries and free-text phonetic searches.

The package is released under the [MIT License](LICENSE).

## Installation

To install the package in editable mode locally, navigate to the `python_package` folder and run:

```bash
pip install -e .
```

The installed package exposes its release version as `ipa_labels.__version__`.

## Features

- **Compressed Database Loading**: Reads the generated UTF-8 compressed JSON database. The repository-level `ipa_symbols.csv` remains the editable source of truth.
- **Structured Searches (`lookup`)**: Find symbols by specifying values for columns like `voicing`, `place`, `manner`, `type`, `height`, `roundedness`, etc.
- **Free-Text Search (`query`)**: Search for multiple terms case-insensitively across all columns (e.g., searching `'voiced bilabial'` will find matching phonemes).
- **Flexible Field Selection**: Choose to return complete records, a single column as a list of values, or a subset of columns.
- **Convenience Accessors**: Use `get()` for one label or `values()` for a field across many matches.
- **Input Validation**: Unknown search or output fields raise `ValueError`, and `criteria` must be a dictionary or `None`, helping catch typing mistakes early.

---

## Usage

For a detailed step-by-step guide with copy-paste examples, see the
[full tutorial](TUTORIAL.md).

For quick label access:

```python
ipa_labels.get("p", "place")
# 'bilabial'

ipa_labels.values("place", type="consonant", unique=True)
```

The structured interface groups related information:

```python
p = ipa_labels.get("p")
p.symbol.ipa
p.code.unicode
p.label.place
p.features.labial
p.description.unicode_name
```

The five groups are `symbol`, `code`, `label`, `features`, and `description`.
See [TUTORIAL.md](TUTORIAL.md) for defaults, aliases, missing values, multiple
results, and PHOIBLE inventory examples.

### 1. Free-Text Queries (`query`)

Search for symbols using any description words:

```python
import ipa_labels

# Find symbols that contain both 'voiced' and 'implosive'
results = ipa_labels.query('voiced implosive')
for r in results:
    print(f"Symbol: {r['symbol']} | Description: {r['description']}")
# Output:
# Symbol: ɓ | Description: Voiced bilabial implosive
# Symbol: ɗ | Description: Voiced dental or alveolar implosive
# ...
```

#### Selecting Specific Output Fields
If you only want specific columns (e.g., TIPA LaTeX macro and Unicode name):

```python
# Requesting a single field returns a flat list of values:
symbols = ipa_labels.query('voiceless dental fricative', fields='symbol')
print(symbols)  # -> ['θ']

# Requesting multiple fields returns a list of dictionaries with only those keys:
info = ipa_labels.query('voiceless dental fricative', fields=['symbol', 'tipa', 'hex_code'])
print(info)
# Output:
# [{'symbol': 'θ', 'tipa': 'T', 'hex_code': '03B8'}]
```

### 2. Structured Lookup (`lookup`)

Search for entries using explicit key-value criteria:

```python
# Look up all voiceless velar plosives
results = ipa_labels.lookup(voicing='voiceless', place='velar', manner='plosive')
for r in results:
    print(r['symbol'], r['unicode_name'])
# Output:
# k LATIN SMALL LETTER K

# Using helper dictionary argument
criteria = {'type': 'vowel', 'frontness': 'front', 'roundedness': 'rounded'}
rounded_front_vowels = ipa_labels.lookup(criteria=criteria, fields='symbol')
print(rounded_front_vowels)
# Output:
# ['y', 'ø', 'œ', 'ɶ', 'ʏ']
```

---

## Database Schema

Every record in the dictionary contains the following fields:

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `symbol` | String | UTF-8 encoded IPA symbol |
| `ipa_number` | String | Official IPA Reference Number |
| `hex_code` | String | Unicode Hexadecimal / USV Code |
| `decimal_code`| String | Unicode Decimal Value |
| `tipa` | String | LaTeX TIPA code representation |
| `af_ii` | String | Association of Font Information Interchange code |
| `ipa_name` | String | Common phonetic name (e.g. 'Schwa', 'Esh') |
| `unicode_name`| String | Official Unicode character description |
| `type` | String | Category: `consonant`, `vowel`, `diacritic`, `suprasegmental`, `other` |
| `voicing` | String | For consonants: `voiced`, `voiceless` |
| `place` | String | For consonants: Place of articulation (e.g. `bilabial`, `alveolar`) |
| `manner` | String | For consonants: Manner of articulation (e.g. `plosive`, `fricative`) |
| `height` | String | For vowels: Height (e.g. `close`, `open-mid`, `mid`) |
| `closeness` | String | Synonym for vowel `height` |
| `openness` | String | Synonym for vowel `height` |
| `frontness` | String | For vowels: Frontness (e.g. `front`, `central`, `back`) |
| `roundedness` | String | For vowels: Roundedness (`rounded`, `unrounded`) |
| `description` | String | Full text description from official IPA guides |
| `sampa` | String | SAMPA / X-SAMPA ASCII phonetic code |
| `arpabet` | String | ARPABET phonetic transcription code (where applicable) |

## Input validation

Field names passed to `lookup()` or `query()` are checked against the database
schema. For example, a misspelled field raises a clear error instead of
silently returning an empty result:

```python
ipa_labels.lookup(fields="frontnes")
# ValueError: Unknown field: 'frontnes'
```

Structured criteria must be supplied as a dictionary:

```python
ipa_labels.lookup(criteria={"type": "vowel"})
```

## Custom databases and runtime updates

For a separate CSV or compressed JSON database file, create an `IPALookup`
instance with its path:

```python
from ipa_labels import IPALookup

custom = IPALookup(csv_path="path/to/my_ipa_symbols.csv")
results = custom.lookup(type="vowel", fields="symbol")
```

The instance reloads its data file before each lookup or query. To update the
packaged database, edit the repository-level `ipa_symbols.csv` and run
`py -3.12 build_package_data.py` from the repository root.

## Reference-resource checks

The current 318-record database has been checked against all reference files
kept in the repository's `resources/` folder, including the accessible IPA
HTML chart, the TIPA/Unicode PDF, the IPA reference chart, the SIL phonetic
symbol PDF, and the saved webpage reference. The checks compare Unicode
identities and names where the source formats allow a reliable comparison;
historical sources use different labels and cover different subsets of the
database. The reproducible check is:

```powershell
py -3.12 scripts/validate_resources.py
```

The source documents remain reference material; they are not bundled into the
installed package.
