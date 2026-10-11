# ipa.labels

A comprehensive, R-based phonetic database and lookup utility for the International Phonetic Alphabet (IPA).

`ipa.labels` allows you to look up IPA symbols by their descriptions, names, Hex/Decimal values, TIPA LaTeX macros, AF II codes, SAMPA/X-SAMPA representation, and ARPABET mappings.

Version 0.2 also provides a nested record interface with `ipaget("p")` and
PHOIBLE features and inventories.

## Installation

Install directly from GitHub:

```R
if (!requireNamespace("remotes", quietly = TRUE)) install.packages("remotes")
remotes::install_github("congzhang365/IPA_labels", subdir = "r_package/ipa.labels")
```

## Features

- **Compressed Database Loading**: Reads the generated UTF-8 compressed JSON database shipped with the package.
- **Structured Searches (`ipalookup`)**: Find symbols by specifying values for columns like `voicing`, `place`, `manner`, `type`, `height`, `roundedness`, etc.
- **Free-Text Search (`ipaquery`)**: Search for multiple terms case-insensitively across all columns (e.g., searching `'voiced bilabial'` will find matching phonemes).
- **Flexible Field Selection**: Choose to return complete records as a data frame, a single column as a flat vector, or a subset of columns.
- **Convenience Accessors**: Use `ipaget()` for one label or `ipavalues()` for a field across many matches.

---

## Usage

When the master CSV changes, run `py -3.12 build_package_data.py` from the
repository root. This regenerates the compressed database used by both the
Python and R packages.

Load the library in R:

```R
library(ipa.labels)
```

### 1. Free-Text Queries (`ipaquery`)

Search for symbols using any description words:

```R
# Find symbols that contain both 'voiced' and 'implosive'
results <- ipaquery("voiced implosive")
print(head(results[, c("symbol", "description")]))
# Output:
#   symbol                              description
# 1      ɓ                Voiced bilabial implosive
# 2      ɗ      Voiced dental or alveolar implosive
# 3      ʄ                  Voiced palatal implosive
# 4      ɠ                    Voiced velar implosive
# 5      ʛ                   Voiced uvular implosive
```

#### Selecting Specific Output Fields
If you only want specific columns:

```R
# Requesting a single field returns a flat vector:
symbols <- ipaquery("voiceless dental fricative", fields = "symbol")
print(symbols)  # [1] "θ"

# Requesting multiple fields returns a data frame with only those columns:
info <- ipaquery("voiceless dental fricative", fields = c("symbol", "tipa", "hex_code"))
print(info)
#   symbol tipa hex_code
# 1      θ    T     03B8
```

### 2. Structured Lookup (`ipalookup`)

Search for entries using explicit key-value criteria:

```R
# Look up all voiceless velar plosives
results <- ipalookup(voicing = "voiceless", place = "velar", manner = "plosive")
print(results[, c("symbol", "unicode_name")])
#   symbol         unicode_name
# 1      k LATIN SMALL LETTER K

# Using list criteria and specifying fields:
rounded_front_vowels <- ipalookup(
  criteria = list(type = "vowel", frontness = "front", roundedness = "rounded"), 
  fields = "symbol"
)
print(rounded_front_vowels)
# [1] "y" "ø" "œ" "ɶ" "ʏ"
```

For shorter common lookups:

```R
ipaget("p", "place")
# [1] "bilabial"

ipavalues("height", type = "vowel", unique = TRUE)
ipavalues("place", type = "consonant", unique = TRUE)
```

Structured access uses the five groups `symbol`, `code`, `label`, `features`,
and `description`:

```R
p <- ipaget("p")
p$symbol$ipa
p$code$unicode
p$label$place
p$features$labial
p$description$unicode_name

english <- ipainventory(iso639_3 = "eng")
```

### PHOIBLE features

The `features` group contains structured segment features from the bundled
PHOIBLE 2.0.1 snapshot. It is intentionally separate from the readable IPA
`label` group. For example, `p$label$place` is the human-readable label
“bilabial”, whereas `p$features$labial` is the PHOIBLE feature value `TRUE`.

```R
p <- ipaget("p")

p$features$consonantal
p$features$labial
p$features$nasal
p$features$spreadGlottis

# Inspect every feature supplied for this symbol
names(p$features)
unclass(p$features)
```

Feature values are normally `TRUE`, `FALSE`, or `NA`. `NA` means that the
bundled PHOIBLE snapshot does not provide a value; it does not mean that the
feature has been inferred to be false. Use `label` for readable phonetic
descriptions and `features` for structured analysis.

### PHOIBLE language inventories

`ipainventory()` returns a list. A language can have several PHOIBLE records,
for example because different doculects or sources were used. Each record
keeps its own inventory ID, language, doculect, ISO code, Glottocode, source,
URL, and segment list.

```R
english <- ipainventory(iso639_3 = "eng")

for (inv in english) {
  cat(inv$inventory_id, inv$language, inv$doculect, "\n")
  cat("Source:", inv$source, "\n")
  cat("Number of segments:", length(inv$segments), "\n")

  first_segment <- inv$segments[[1]]
  print(first_segment$symbol)
  print(first_segment$marginal)
}
```

Use `language`, `iso639_3`, `glottocode`, or `inventory_id` to narrow the
results. Because the function can return zero, one, or many records, do not
assume that the first result is the only inventory for a language.

## Reference-resource checks

The current database used by the Python and R packages has been checked
against all reference files kept in the repository's `resources/` folder,
including the accessible IPA HTML chart, the TIPA/Unicode PDF, the IPA
reference chart, the SIL phonetic symbol PDF, and the saved webpage reference.
The checks compare Unicode identities and names where the source formats allow
a reliable comparison; historical sources use different labels and cover
different subsets of the database. Run the reproducible check from the
repository root with:

```powershell
py -3.12 scripts/validate_resources.py
```

---

## Database Schema

Every record in the dictionary contains the following fields:

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `symbol` | character | UTF-8 encoded IPA symbol |
| `ipa_number` | character | Official IPA Reference Number |
| `hex_code` | character | Unicode Hexadecimal / USV Code |
| `decimal_code`| character | Unicode Decimal Value |
| `tipa` | character | LaTeX TIPA code representation |
| `af_ii` | character | Association of Font Information Interchange code |
| `ipa_name` | character | Common phonetic name (e.g. 'Schwa', 'Esh') |
| `unicode_name`| character | Official Unicode character description |
| `type` | character | Category: `consonant`, `vowel`, `diacritic`, `suprasegmental`, `other` |
| `voicing` | character | For consonants: `voiced`, `voiceless` |
| `place` | character | For consonants: Place of articulation (e.g. `bilabial`, `alveolar`) |
| `manner` | character | For consonants: Manner of articulation (e.g. `plosive`, `fricative`) |
| `height` | character | For vowels: Height (e.g. `close`, `open-mid`, `mid`) |
| `closeness` | character | Synonym for vowel `height` |
| `openness` | character | Synonym for vowel `height` |
| `frontness` | character | For vowels: Frontness (e.g. `front`, `central`, `back`) |
| `roundedness` | character | For vowels: Roundedness (`rounded`, `unrounded`) |
| `description` | character | Full text description from official IPA guides |
| `sampa` | character | SAMPA / X-SAMPA ASCII phonetic code |
| `arpabet` | character | ARPABET phonetic transcription code (where applicable) |
