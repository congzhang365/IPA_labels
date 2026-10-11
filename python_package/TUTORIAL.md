# `ipa_labels` tutorial

`ipa_labels` provides two compatible interfaces: `lookup()` returns the original
flat dictionaries, while `get("p")` returns one structured `IPALabel` record.
The structured record has five groups.

## Start with the basic idea

Think of the package as a box of information cards. Each card describes one
IPA symbol. The card for `p`, for example, tells you that it is a voiceless
bilabial plosive and gives you its Unicode, TIPA, AFII, and transcription codes.

The symbol is the thing you are looking up. A group is a section on its card.
For example, `p.label.place` means “on the label section of the `p` card, show
me the place of articulation”. You can copy the following example and run it
line by line:

```python
import ipa_labels

p = ipa_labels.get("p")
print(p.label.place)   # bilabial
print(p.label.manner)  # plosive
print(p.code.unicode)  # U+0070
```

You do not need to learn every field before using the package. Start with one
symbol, ask one question, and then explore the other sections of its card.

| Group | Contents | Default |
| --- | --- | --- |
| `symbol` | `ipa`, `sampa`, `arpabet` | `ipa` |
| `code` | TIPA, IPA number, USV/Unicode, Unicode range, hex, decimal, AFII | `tipa` |
| `label` | readable type, voicing, place, manner, vowel dimensions | `full` |
| `features` | PHOIBLE segment features such as `consonantal`, `labial`, `nasal`, `high` | the complete feature mapping |
| `description` | IPA name, Unicode name, and text description | `ipa_name` |

`unicode` is an alias for `usv`; `closeness` and `openness` are aliases for
`height`; and `backness` is an alias for `frontness`. Missing values are
`None` in Python (and `NA` in R).

## Install and import

For the current GitHub version, run:

```powershell
py -m pip install "git+https://github.com/congzhang365/IPA_labels.git#subdirectory=python_package"
```

```python
import ipa_labels
```

## Structured access

```python
p = ipa_labels.get("p")

print(p.symbol.ipa)                 # p
print(p.code.unicode)               # U+0070
print(p.code.unicode_range)         # Basic Latin
print(p.code.afii)                  # E2A2, when available
print(p.label.full)                 # voiceless bilabial plosive
print(p.label.place)                # bilabial
print(p.features.consonantal)       # True
print(p.features.labial)            # True
print(p.features.nasal)             # False
print(p.description.ipa_name)       # Lower-case P
print(p.description.unicode_name)   # LATIN SMALL LETTER P
```

The vowel `ɘ` demonstrates names and vowel labels:

```python
schwa_like = ipa_labels.get("ɘ")
print(schwa_like.label.height)             # close-mid
print(schwa_like.label.frontness)          # central
print(schwa_like.label.roundedness)        # unrounded
print(schwa_like.description.ipa_name)     # Reversed E
print(schwa_like.description.unicode_name) # LATIN SMALL LETTER REVERSED E
```

Groups also support bracket access, so code can use a variable field name:

```python
group = "label"
field = "place"
print(p[group][field])
```

## Queries and compatibility

The existing flat API remains available:

```python
ipa_labels.get("p", "place")
ipa_labels.lookup(place="bilabial", fields="symbol")
ipa_labels.lookup(type="vowel", fields=["symbol", "height", "frontness"])
ipa_labels.values("place", type="consonant", unique=True)
ipa_labels.query("voiced bilabial plosive", fields="symbol")
```

Structured groups can be used in a query too:

```python
ipa_labels.lookup(code={"unicode": "U+0070"}, fields="symbol")
ipa_labels.lookup(label={"place": "bilabial"}, fields="symbol")
ipa_labels.lookup(symbol={"ipa": "p"})
```

Queries can return multiple records. Iterate over the list or narrow the query:

```python
for item in ipa_labels.lookup(type="vowel", height="close"):
    print(item["symbol"], item["frontness"], item["roundedness"])
```

For fields that have no value, the flat compatibility API returns an empty
string; the structured API converts that to `None`.

## PHOIBLE features and inventories

PHOIBLE features are separate from the package's readable IPA labels. They are
structured phonological feature values intended for comparison and analysis.
For example, `p.label.place` is the readable IPA description `bilabial`, while
`p.features.labial` is a PHOIBLE feature value. They answer related but
different questions:

```python
p = ipa_labels.get("p")
print(p.label.place)                 # bilabial
print(p.features["consonantal"])    # True
print(p.features["labial"])         # True
print(p.features["continuant"])     # False
print(p.features["spreadGlottis"])  # usually False or None, depending on symbol
print(p.features.default)            # all supplied PHOIBLE fields
```

The bundled PHOIBLE snapshot is version 2.0.1. Its feature values are converted
to Python booleans (`True`/`False`) and missing values to `None`. `None` means
that PHOIBLE does not provide a value; the package does not guess one. Feature
names include articulatory and laryngeal properties such as `consonantal`,
`sonorant`, `continuant`, `nasal`, `labial`, `coronal`, `dorsal`, `high`,
`low`, `front`, `back`, `spreadGlottis`, and `constrictedGlottis`. The exact
fields available can vary by record, so `p.features.default` is the safest way
to inspect the complete mapping.

Inventories retain language, doculect, ISO 639-3 code, Glottocode, source, URL,
marginal status, and segment membership. Inventories are not merged merely
because they share a language:

```python
english = ipa_labels.inventory(language="English")
english_iso = ipa_labels.inventory(iso639_3="eng")
one_inventory = ipa_labels.inventory(inventory_id=123)

for inv in english:
    print(inv["inventory_id"], inv["language"], inv["doculect"])
    print(inv["iso639_3"], inv["glottocode"], inv["source"])
    print("segments:", len(inv["segments"]))
    for segment in inv["segments"]:
        print(segment["symbol"], segment["marginal"])
```

There may be no matching inventory, one matching inventory, or several
matching inventories. Always loop over the returned list when you want to see
all results. A segment record can also include a parameter ID, allophone
information, and its own source.

## Updating data

Edit the root `ipa_symbols.csv`, then rebuild both packages:

```powershell
py -3.12 build_package_data.py
```

This regenerates IPA records, Unicode ranges, PHOIBLE features, and PHOIBLE
inventories in both package data directories. Run the tests afterward:

```powershell
py -3.12 test_python_package.py
& 'C:\Program Files\R\R-4.6.1\bin\Rscript.exe' test_r_package.R
```
