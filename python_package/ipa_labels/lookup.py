"""Flat and structured access to the IPA label database."""
import csv, gzip, json, os
from types import SimpleNamespace

GROUPS = {
    "symbol": ("ipa", "sampa", "arpabet"),
    "code": ("tipa", "ipa_number", "usv", "unicode", "unicode_range", "hex", "decimal", "afii"),
    "label": ("full", "type", "voicing", "place", "manner", "height", "closeness", "openness", "frontness", "backness", "roundedness"),
    "description": ("ipa_name", "unicode_name", "text"),
}
ALIASES = {"unicode": "usv_code", "usv": "usv_code", "hex": "hex_code", "decimal": "decimal_code", "afii": "af_ii", "closeness": "height", "openness": "height", "backness": "frontness"}

def _clean(value):
    return None if value in (None, "", "NA", "N/A") else value

class _Group(SimpleNamespace):
    def __getitem__(self, key): return getattr(self, key)

class IPALabel:
    """A structured IPA record; mapping access preserves the old flat API."""
    def __init__(self, row, features=None):
        self._row = row
        features = features or {}
        usv = _clean(row.get("usv", row.get("usv_code")))
        height = _clean(row.get("height")); frontness = _clean(row.get("frontness"))
        full = _clean(row.get("full")) or _full_label(row)
        self.symbol = _Group(ipa=_clean(row.get("symbol")), sampa=_clean(row.get("sampa")), arpabet=_clean(row.get("arpabet")), default=_clean(row.get("symbol")))
        self.code = _Group(tipa=_clean(row.get("tipa")), ipa_number=_clean(row.get("ipa_number")), usv=usv, unicode=usv, unicode_range=_clean(row.get("unicode_range")), hex=_clean(row.get("hex", row.get("hex_code"))), decimal=_clean(row.get("decimal", row.get("decimal_code"))), afii=_clean(row.get("afii", row.get("af_ii"))), default=_clean(row.get("tipa")))
        self.label = _Group(full=full, type=_clean(row.get("type")), voicing=_clean(row.get("voicing")), place=_clean(row.get("place")), manner=_clean(row.get("manner")), height=height, closeness=height, openness=height, frontness=frontness, backness=frontness, roundedness=_clean(row.get("roundedness")), default=full)
        self.features = _Group(**features); self.features.default = features.copy()
        self.description = _Group(ipa_name=_clean(row.get("ipa_name")), unicode_name=_clean(row.get("unicode_name")), text=_clean(row.get("text", row.get("description"))), default=_clean(row.get("ipa_name")))

    def __getitem__(self, key):
        if key in GROUPS: return getattr(self, key)
        key = ALIASES.get(key, key)
        if key in self._row: return _clean(self._row[key])
        for group in GROUPS:
            if key in GROUPS[group]: return getattr(getattr(self, group), key)
        raise KeyError(key)

    def get(self, key, default=None):
        try: return self[key]
        except KeyError: return default

    def to_dict(self): return dict(self._row)
    def __repr__(self): return f"IPALabel({self.symbol.ipa!r})"

def _full_label(row):
    parts = [row.get("voicing"), row.get("place"), row.get("manner")] if row.get("type") == "consonant" else [row.get("height"), row.get("frontness"), row.get("roundedness"), row.get("type")]
    return " ".join(str(part) for part in parts if part) or row.get("description") or row.get("ipa_name")

def _load_json_gz(path, default):
    if not os.path.exists(path): return default
    with gzip.open(path, "rt", encoding="utf-8") as stream: return json.load(stream)

class IPALookup:
    def __init__(self, csv_path=None):
        self.csv_path = csv_path or os.path.join(os.path.dirname(__file__), "data", "ipa_symbols.json.gz")
        self.data, self.features, self.inventories = [], {}, []
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.csv_path): raise FileNotFoundError(f"IPA database not found at {self.csv_path}")
        if self.csv_path.endswith(".json.gz"):
            with gzip.open(self.csv_path, "rt", encoding="utf-8") as stream: self.data = json.load(stream)
            data_dir = os.path.dirname(self.csv_path)
            self.features = _load_json_gz(os.path.join(data_dir, "ipa_features.json.gz"), {})
            self.inventories = _load_json_gz(os.path.join(data_dir, "phoible_inventories.json.gz"), [])
        else:
            with open(self.csv_path, encoding="utf-8", newline="") as stream: self.data = list(csv.DictReader(stream))
            self.features, self.inventories = {}, []

    def _filter_fields(self, results, fields):
        if fields is None: return results
        available = set(self.data[0]) if self.data else set()
        if isinstance(fields, str):
            if fields not in available: raise ValueError(f"Unknown field: {fields!r}")
            return [r.get(fields, "") for r in results]
        requested = list(fields); unknown = [f for f in requested if f not in available]
        if unknown: raise ValueError(f"Unknown field(s): {', '.join(repr(f) for f in unknown)}")
        return [{f: r.get(f, "") for f in requested} for r in results]

    def lookup(self, criteria=None, fields=None, **kwargs):
        self.load_data()
        if criteria is not None and not isinstance(criteria, dict): raise TypeError("criteria must be a dictionary or None")
        search = dict(criteria or {}); search.update(kwargs); flattened = {}
        for key, value in search.items():
            if key in GROUPS and isinstance(value, dict):
                flattened.update({ALIASES.get(k, k): v for k, v in value.items()})
            else: flattened[ALIASES.get(key, key)] = value
        unknown = [k for k in flattened if k not in self.data[0]] if self.data else []
        if unknown: raise ValueError(f"Unknown search field(s): {', '.join(repr(f) for f in unknown)}")
        if not flattened: return self._filter_fields(self.data, fields)
        case_sensitive = {"symbol", "hex_code", "sampa", "arpabet", "usv_code"}
        results = []
        for row in self.data:
            if all((row.get(k, "").strip() == str(v).strip()) if k in case_sensitive else (row.get(k, "").strip().lower() == str(v).strip().lower()) for k, v in flattened.items()): results.append(row)
        return self._filter_fields(results, fields)

    def query(self, search_term, fields=None):
        self.load_data(); words = str(search_term).strip().lower().split()
        results = [row for row in self.data if words and all(word in " ".join(row.values()).lower() for word in words)]
        return self._filter_fields(results, fields)

    def structured(self, symbol): return [IPALabel(row, self.features.get(row.get("symbol"), {})) for row in self.lookup(symbol=symbol)]

_instance = IPALookup()
def lookup(criteria=None, fields=None, **kwargs): return _instance.lookup(criteria=criteria, fields=fields, **kwargs)
def query(search_term, fields=None): return _instance.query(search_term=search_term, fields=fields)
def get(symbol, field=None, default=None):
    records = _instance.structured(symbol)
    if not records: return default
    return records[0] if field is None else records[0].get(field, default)
def values(field, criteria=None, unique=False, **kwargs):
    key = ALIASES.get(field, field); records = _instance.lookup(criteria=criteria, **kwargs)
    if _instance.data and key not in _instance.data[0]: raise ValueError(f"Unknown field: {field!r}")
    result = [r.get(key, "") for r in records if r.get(key, "") not in ("", None)]
    return list(dict.fromkeys(result)) if unique else result
def inventory(language=None, iso639_3=None, glottocode=None, inventory_id=None):
    _instance.load_data(); result = _instance.inventories
    if language is not None: result = [x for x in result if str(x.get("language", "")).lower() == str(language).lower()]
    if iso639_3 is not None: result = [x for x in result if x.get("iso639_3") == iso639_3]
    if glottocode is not None: result = [x for x in result if x.get("glottocode") == glottocode]
    if inventory_id is not None: result = [x for x in result if str(x.get("inventory_id")) == str(inventory_id)]
    return result
