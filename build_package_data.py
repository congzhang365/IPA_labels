"""Build the distributable compressed IPA database for both packages.

The repository-level ipa_symbols.csv is the source of truth. This script
generates the compressed JSON database consumed by the Python and R packages.
Run it after editing the CSV.
"""

import csv
import gzip
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE_CSV = ROOT / "ipa_symbols.csv"
DESTINATIONS = (
    ROOT / "python_package" / "ipa_labels" / "data" / "ipa_symbols.json.gz",
    ROOT / "r_package" / "ipa_labels" / "inst" / "extdata" / "ipa_symbols.json.gz",
)
FEATURE_DESTINATIONS = (
    ROOT / "python_package" / "ipa_labels" / "data" / "ipa_features.json.gz",
    ROOT / "r_package" / "ipa_labels" / "inst" / "extdata" / "ipa_features.json.gz",
)
INVENTORY_DESTINATIONS = (
    ROOT / "python_package" / "ipa_labels" / "data" / "phoible_inventories.json.gz",
    ROOT / "r_package" / "ipa_labels" / "inst" / "extdata" / "phoible_inventories.json.gz",
)
METADATA_DESTINATIONS = (
    ROOT / "python_package" / "ipa_labels" / "data" / "data_metadata.json",
    ROOT / "r_package" / "ipa_labels" / "inst" / "extdata" / "data_metadata.json",
)
PHOIBLE_DIR = ROOT / "resources" / "phoible-extracted" / "phoible-2.0.1" / "cldf"
BLOCKS_FILE = ROOT / "resources" / "Blocks- latest.txt"


def _unicode_ranges():
    ranges = []
    if not BLOCKS_FILE.exists():
        return ranges
    for line in BLOCKS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or ";" not in line:
            continue
        span, name = [part.strip() for part in line.split(";", 1)]
        start, end = [int(part, 16) for part in span.split("..")]
        ranges.append((start, end, name))
    return ranges


def _unicode_range(usv, ranges):
    if not usv:
        return None
    first = usv.strip().split(" + ", 1)[0].removeprefix("U+")
    try:
        codepoint = int(first, 16)
    except ValueError:
        return None
    for start, end, name in ranges:
        if start <= codepoint <= end:
            return name
    return "No_Block"


def _phoible_feature_data():
    """Return symbol -> PHOIBLE feature values, preserving missing values."""
    import csv

    path = PHOIBLE_DIR / "parameters.csv"
    if not path.exists():
        return {}
    with path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    feature_fields = [field for field in rows[0] if field not in {"ID", "Name", "Description"}]
    result = {}
    for row in rows:
        values = {}
        for field in feature_fields:
            value = row.get(field, "")
            values[field] = None if value in {"", "0"} else value == "+" if value in {"+", "-"} else value
        # PHOIBLE can contain a small number of repeated segment names. Keep
        # the first deterministic parameter row and record the source release.
        result.setdefault(row["Name"], values)
    return result


def _clean_afii(value):
    """Keep the actual AFII token and discard PDF extraction spillover."""
    value = (value or "").strip()
    if value.upper() in {"N/A", "NA"}:
        return ""
    match = re.search(r"\b([A-Fa-f0-9]{4,6})\b", value)
    return match.group(1).upper() if match else ""


def _phoible_inventory_data():
    """Build compact inventory records from the PHOIBLE CLDF snapshot."""
    import csv
    from collections import defaultdict

    required = [PHOIBLE_DIR / name for name in ("languages.csv", "contributions.csv", "parameters.csv", "values.csv")]
    if not all(path.exists() for path in required):
        return []
    def read(name):
        with (PHOIBLE_DIR / name).open(encoding="utf-8", newline="") as stream:
            return list(csv.DictReader(stream))
    languages = {row["ID"]: row for row in read("languages.csv")}
    contributions = {row["ID"]: row for row in read("contributions.csv")}
    parameters = {row["ID"]: row for row in read("parameters.csv")}
    grouped = defaultdict(list)
    for row in read("values.csv"):
        grouped[(row["Contribution_ID"], row["Language_ID"])].append(row)
    inventories = []
    for (contribution_id, language_id), rows in sorted(grouped.items()):
        contribution = contributions.get(contribution_id, {})
        language = languages.get(language_id, {})
        segments = []
        for row in rows:
            parameter = parameters.get(row["Parameter_ID"], {})
            segments.append({
                "symbol": parameter.get("Name", row.get("Value", "")),
                "parameter_id": row.get("Parameter_ID"),
                "marginal": row.get("Marginal") or None,
                "allophones": row.get("Allophones") or None,
                "source": row.get("Source") or None,
            })
        inventories.append({
            "inventory_id": int(contribution_id) if contribution_id.isdigit() else contribution_id,
            "language_id": language_id,
            "language": contribution.get("Name") or language.get("Name"),
            "doculect": contribution.get("Name") or language.get("Name"),
            "iso639_3": language.get("ISO639P3code") or None,
            "glottocode": language.get("Glottocode") or None,
            "source": contribution.get("Source") or None,
            "url": contribution.get("URL") or None,
            "segments": segments,
        })
    return inventories


def build_database():
    with SOURCE_CSV.open("r", encoding="utf-8", newline="") as source:
        records = list(csv.DictReader(source))

    if not records:
        raise ValueError(f"The source CSV is empty: {SOURCE_CSV}")

    ranges = _unicode_ranges()
    for record in records:
        record["unicode_range"] = _unicode_range(record.get("usv_code", ""), ranges)
        record["af_ii"] = _clean_afii(record.get("af_ii"))

    for destination in DESTINATIONS:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with gzip.open(destination, "wt", encoding="utf-8", newline="") as output:
            # ASCII-safe JSON avoids locale-dependent decoding problems in R
            # while preserving the original Unicode characters after parsing.
            json.dump(records, output, ensure_ascii=True, separators=(",", ":"))

    print(f"Generated {len(records)} records from {SOURCE_CSV.name}")
    for destination in DESTINATIONS:
        print(f"  {destination.relative_to(ROOT)}")

    features = _phoible_feature_data()
    inventories = _phoible_inventory_data()
    for destinations, payload in ((FEATURE_DESTINATIONS, features), (INVENTORY_DESTINATIONS, inventories)):
        for destination in destinations:
            destination.parent.mkdir(parents=True, exist_ok=True)
            with gzip.open(destination, "wt", encoding="utf-8", newline="") as output:
                json.dump(payload, output, ensure_ascii=True, separators=(",", ":"))
            print(f"  {destination.relative_to(ROOT)}")
    print(f"PHOIBLE features: {len(features)}; inventories: {len(inventories)}")
    metadata = {
        "phoible": {
            "version": "2.0.1",
            "source": "https://github.com/cldf-datasets/phoible/releases/tag/v2.0.1",
            "license": "CC BY 4.0",
            "citation": "Moran, Steven and Daniel McCloy (eds.). 2019. PHOIBLE 2.0.",
        },
        "unicode_blocks": {
            "source": "https://www.unicode.org/Public/UCD/latest/ucd/Blocks.txt",
            "description": "Unicode Character Database Blocks.txt",
        },
    }
    for destination in METADATA_DESTINATIONS:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build_database()
