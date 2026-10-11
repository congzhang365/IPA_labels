# ipa-labels

![ipa-labels logo](docs/assets/ipa-labels-logo.svg)

[![Python package](https://img.shields.io/badge/Python-package-3776AB?logo=python&logoColor=white)](python_package/README.md)
[![R package](https://img.shields.io/badge/R-package-276DC3?logo=r&logoColor=white)](r_package/ipa_labels/README.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](python_package/LICENSE)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-222222?logo=github)](docs/index.html)

`ipa-labels` is a bilingual Python and R toolkit for exploring IPA symbols,
Unicode and transcription codes, articulatory labels, PHOIBLE features, and
language-specific phoneme inventories.

It is designed for linguists, phoneticians, speech researchers, and students
who need to move between a symbol and the information attached to it.

## Start here

- [Python manual](docs/python/index.html) · [Python package README](python_package/README.md)
- [R manual](docs/r/index.html) · [R package README](r_package/ipa_labels/README.md)
- [Beginner tutorial](python_package/TUTORIAL.md)
- [Data and provenance](resources/README.md)

## Quick example

```python
import ipa_labels

p = ipa_labels.get("p")
print(p.label.full)          # voiceless bilabial plosive
print(p.code.unicode)        # U+0070
print(p.features.labial)     # True
```

The R equivalent is:

```r
library(ipa_labels)

p <- ipaget("p")
p$label$full
p$code$unicode
p$features$labial
```

## What is included?

Each structured record has five groups: `symbol`, `code`, `label`,
`features`, and `description`. The package preserves the original flat lookup
API as well, so it can be introduced gradually into existing scripts.

The generated data includes Unicode block names, cleaned AFII values, and a
versioned PHOIBLE 2.0.1 snapshot with segment features and inventories.

## Development

The public repository contains the generated package data, so users can
install and use both packages without access to the private source CSV. The
source CSV and data-generation scripts remain in the maintainer's local
working directory and are intentionally excluded from GitHub.

The manuals are plain HTML in `docs/`, so they can be published with GitHub
Pages without a documentation build step.
