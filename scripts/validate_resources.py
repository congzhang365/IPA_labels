"""Compare the package CSV with the local reference resources.

This is intentionally a conservative validator.  It checks exact Unicode
identities and names where the source exposes them, and checks that the
package values can be found in the reference PDFs where the PDF layout is
not machine-readable enough for a reliable row-by-row comparison.
"""

from __future__ import annotations

import csv
import re
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESOURCES = ROOT / "resources"
CSV_PATH = ROOT / "ipa_symbols.csv"


def load_package_records() -> list[dict[str, str]]:
    with CSV_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class AccessibleChartParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.records: list[dict[str, str]] = []
        self._title: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "span":
            return
        title = dict(attrs).get("title")
        if title and title.startswith("U+"):
            self._title = title
            self._text = []

    def handle_data(self, data: str) -> None:
        if self._title is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag != "span" or self._title is None:
            return
        match = re.match(r"U\+([0-9A-F]+):\s*(.*)", self._title, re.I)
        if match:
            self.records.append(
                {
                    "hex_code": match.group(1).upper(),
                    "unicode_name": match.group(2).strip(),
                    "symbol": "".join(self._text).strip(),
                }
            )
        self._title = None
        self._text = []


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).casefold()


def check_accessible_chart(records: list[dict[str, str]]) -> tuple[int, int, int]:
    parser = AccessibleChartParser()
    parser.feed((RESOURCES / "accessiblechart.html").read_text(encoding="utf-8"))
    package = {row["hex_code"].upper(): row for row in records if "+" not in row["hex_code"]}
    matched = mismatched = missing = 0
    for source in parser.records:
        row = package.get(source["hex_code"])
        if row is None:
            missing += 1
            continue
        matched += 1
        if (
            row["symbol"] != source["symbol"]
            or normalize(row["unicode_name"]) != normalize(source["unicode_name"])
        ):
            mismatched += 1
    return len(parser.records), matched, mismatched + missing


def extract_pdf_text(filename: str) -> str:
    import fitz

    document = fitz.open(RESOURCES / filename)
    return "\n".join(page.get_text() for page in document)


def parse_unitipa_records(text: str) -> dict[str, dict[str, str]]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    records: dict[str, dict[str, str]] = {}
    keys = {
        "Name:": "description",
        "IPA name:": "ipa_name",
        "IPA number:": "ipa_number",
        "Unicode name:": "unicode_name",
        "Unicode range:": "unicode_range",
        "Hex value:": "hex_code",
        "TIPA code:": "tipa",
        "AFII code:": "af_ii",
    }
    current: dict[str, str] = {}
    last_key: str | None = None
    for line in lines:
        if line == "Name:" and current.get("hex_code"):
            records[current["hex_code"].upper()] = current
            current = {}
        if line in keys:
            last_key = keys[line]
        elif last_key:
            current[last_key] = line
            last_key = None
    if current.get("hex_code"):
        records[current["hex_code"].upper()] = current
    return records


def check_unitipa(records: list[dict[str, str]]) -> tuple[int, int, int]:
    source = parse_unitipa_records(extract_pdf_text("IPA_unitipa_sl.pdf"))
    checked = matched = mismatched = 0
    for row in records:
        hex_code = row["hex_code"].upper()
        if "+" in hex_code or hex_code not in source:
            continue
        checked += 1
        item = source[hex_code]
        if (
            normalize(row["ipa_name"]) != normalize(item.get("ipa_name", ""))
            or normalize(row["unicode_name"]) != normalize(item.get("unicode_name", ""))
        ):
            mismatched += 1
        else:
            matched += 1
    return checked, matched, mismatched


def check_pdf_presence(filename: str, records: list[dict[str, str]]) -> tuple[int, int]:
    text = extract_pdf_text(filename)
    checked = present = 0
    for row in records:
        hex_code = row["hex_code"].upper()
        if "+" in hex_code:
            continue
        checked += 1
        if re.search(rf"(?m)^{re.escape(hex_code)}\s*$", text, re.I):
            present += 1
    return checked, present


def check_derived_extracts() -> tuple[bool, bool, bool]:
    import fitz

    reference = fitz.open(RESOURCES / "iparef11.pdf")
    page1 = reference[0].get_text()
    pages2to4 = ""
    for index in range(1, 4):
        pages2to4 += f"\n--- PAGE {index + 1} ---\n"
        pages2to4 += reference[index].get_text()
    phonsymbol = fitz.open(RESOURCES / "phonsymbol.pdf")[0].get_text()
    return (
        (RESOURCES / "iparef11_page1.txt").read_text(encoding="utf-8") == page1,
        (RESOURCES / "iparef11_pages.txt").read_text(encoding="utf-8") == pages2to4,
        (RESOURCES / "phonsymbol_page1.txt").read_text(encoding="utf-8") == phonsymbol,
    )


def main() -> None:
    records = load_package_records()
    chart_total, chart_matched, chart_issues = check_accessible_chart(records)
    unitipa_checked, unitipa_matched, unitipa_issues = check_unitipa(records)
    iparef_checked, iparef_present = check_pdf_presence("iparef11.pdf", records)
    phonsymbol_checked, phonsymbol_present = check_pdf_presence("phonsymbol.pdf", records)
    extracts_match = check_derived_extracts()
    url_file = RESOURCES / "IPA Symbol Equivalents - Writing Systems Technical Resources.url"

    print(f"Package records: {len(records)}")
    print(
        "accessiblechart.html: "
        f"{chart_matched}/{chart_total} matched; issues={chart_issues}"
    )
    print(
        "IPA_unitipa_sl.pdf: "
        f"{unitipa_matched}/{unitipa_checked} matched; issues={unitipa_issues}"
    )
    print(f"iparef11.pdf: {iparef_present}/{iparef_checked} package codepoints present")
    print(
        f"phonsymbol.pdf: {phonsymbol_present}/{phonsymbol_checked} package codepoints present"
    )
    print(f"iparef11_page1.txt matches PDF page 1: {extracts_match[0]}")
    print(f"iparef11_pages.txt matches PDF pages 2-4: {extracts_match[1]}")
    print(f"phonsymbol_page1.txt matches PDF page 1: {extracts_match[2]}")
    print(f"Web resource shortcut recorded: {url_file.exists()}")

    if not all(extracts_match):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
