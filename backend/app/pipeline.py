from __future__ import annotations

import csv
import io
import json
import re
import sqlite3
import sys
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from defusedxml import ElementTree as ET


ADIF_VERSION = "3.1.7"


def _default_db_path() -> Path:
    """Writable SQLite location: next to the bundled .exe when frozen, else repo data/."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent / "data" / "adifhub.sqlite3"
    return Path(__file__).resolve().parents[2] / "data" / "adifhub.sqlite3"


DB_PATH = _default_db_path()

CORE_FIELDS = [
    "CALL",
    "QSO_DATE",
    "TIME_ON",
    "BAND",
    "FREQ",
    "MODE",
    "SUBMODE",
    "CONTEST_ID",
    "MY_POTA_REF",
    "POTA_REF",
]

ADIF_FIELD_OPTIONS = [
    "CALL",
    "STATION_CALLSIGN",
    "QSO_DATE",
    "TIME_ON",
    "TIME_OFF",
    "BAND",
    "FREQ",
    "MODE",
    "SUBMODE",
    "RST_SENT",
    "RST_RCVD",
    "STX",
    "STX_STRING",
    "SRX",
    "SRX_STRING",
    "NAME",
    "QTH",
    "STATE",
    "VE_PROV",
    "CQZ",
    "ITUZ",
    "ARRL_SECT",
    "GRIDSQUARE",
    "LAT",
    "LON",
    "CONTEST_ID",
    "MY_POTA_REF",
    "POTA_REF",
    "COMMENT",
]

ALIASES = {
    "call": "CALL",
    "callsign": "CALL",
    "indicativo": "CALL",
    "station": "CALL",
    "qso_date": "QSO_DATE",
    "date": "QSO_DATE",
    "fecha": "QSO_DATE",
    "freq": "FREQ",
    "frequency": "FREQ",
    "frecuencia": "FREQ",
    "mhz": "FREQ",
    "mode": "MODE",
    "modo": "MODE",
    "time": "TIME_ON",
    "time_on": "TIME_ON",
    "hora": "TIME_ON",
    "hora_utc": "TIME_ON",
    "utc": "TIME_ON",
    "rst_sent": "RST_SENT",
    "rst_rcvd": "RST_RCVD",
    "contest": "CONTEST_ID",
    "contest_id": "CONTEST_ID",
    "pota": "POTA_REF",
    "pota_ref": "POTA_REF",
    "my_pota_ref": "MY_POTA_REF",
    "lat": "LAT",
    "latitude": "LAT",
    "latitud": "LAT",
    "lon": "LON",
    "lng": "LON",
    "long": "LON",
    "longitude": "LON",
    "longitud": "LON",
    "grid": "GRIDSQUARE",
    "gridsquare": "GRIDSQUARE",
    "locator": "GRIDSQUARE",
    "state": "STATE",
    "estado": "STATE",
    "prov": "VE_PROV",
    "province": "VE_PROV",
    "ve_prov": "VE_PROV",
    "srx": "SRX",
    "srx_string": "SRX_STRING",
    "stx": "STX",
    "stx_string": "STX_STRING",
    "exch": "SRX_STRING",
    "exchange": "SRX_STRING",
    "intercambio": "SRX_STRING",
}

# US state / Canadian province abbreviations recognised in contest exchanges.
US_STATES = {
    "AL",
    "AK",
    "AZ",
    "AR",
    "CA",
    "CO",
    "CT",
    "DE",
    "FL",
    "GA",
    "HI",
    "ID",
    "IL",
    "IN",
    "IA",
    "KS",
    "KY",
    "LA",
    "ME",
    "MD",
    "MA",
    "MI",
    "MN",
    "MS",
    "MO",
    "MT",
    "NE",
    "NV",
    "NH",
    "NJ",
    "NM",
    "NY",
    "NC",
    "ND",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VT",
    "VA",
    "WA",
    "WV",
    "WI",
    "WY",
    "DC",
}
CA_PROVINCES = {
    "AB",
    "BC",
    "MB",
    "NB",
    "NL",
    "NS",
    "NT",
    "NU",
    "ON",
    "PE",
    "QC",
    "SK",
    "YT",
}

# Cabrillo contest templates: positional layout of the QSO line exchange after
# "QSO: freq mode date time". Each entry lists the ADIF field for each sent token
# then each received token. Empty string ("") skips a token. The worked station's
# call (CALL) is not always the first received token (e.g. ARRL Sweepstakes).
_T_SERIAL = {  # RST + serial (CQ WPX, many sprints)
    "sent": ["STATION_CALLSIGN", "RST_SENT", "STX"],
    "rcvd": ["CALL", "RST_RCVD", "SRX"],
}
_T_CQ_ZONE = {  # RST + CQ zone (CQ WW)
    "sent": ["STATION_CALLSIGN", "RST_SENT", "APP_CABRILLO_MY_CQZ"],
    "rcvd": ["CALL", "RST_RCVD", "CQZ"],
}
_T_ITU_ZONE = {  # RST + ITU zone / HQ multiplier (IARU HF)
    "sent": ["STATION_CALLSIGN", "RST_SENT", "APP_CABRILLO_MY_ITUZ"],
    "rcvd": ["CALL", "RST_RCVD", "SRX_STRING"],
}
_T_RST_TEXT = {  # RST + free text (ARRL DX: state/prov or power)
    "sent": ["STATION_CALLSIGN", "RST_SENT", "STX_STRING"],
    "rcvd": ["CALL", "RST_RCVD", "SRX_STRING"],
}
_T_FIELD_DAY = {  # class + ARRL/RAC section (ARRL Field Day)
    "sent": ["STATION_CALLSIGN", "STX_STRING", "APP_CABRILLO_MY_SECT"],
    "rcvd": ["CALL", "APP_CABRILLO_CLASS", "ARRL_SECT"],
}
_T_SWEEPSTAKES = {  # call, serial, precedence, check, section
    "sent": [
        "STATION_CALLSIGN",
        "STX",
        "APP_CABRILLO_MY_PREC",
        "APP_CABRILLO_MY_CHK",
        "APP_CABRILLO_MY_SECT",
    ],
    "rcvd": ["CALL", "SRX", "APP_CABRILLO_PREC", "APP_CABRILLO_CHK", "ARRL_SECT"],
}
_T_NAME_LOCATION = {  # name + state/prov (NAQP, SST)
    "sent": ["STATION_CALLSIGN", "APP_CABRILLO_MY_NAME", "APP_CABRILLO_MY_SPC"],
    "rcvd": ["CALL", "NAME", "STATE"],
}

# Matched by normalised CONTEST_ID prefix (longest prefix wins).
CONTEST_TEMPLATE_PREFIXES: list[tuple[str, dict[str, list[str]]]] = [
    ("ARRL-SS", _T_SWEEPSTAKES),
    ("ARRL-SWEEPSTAKES", _T_SWEEPSTAKES),
    ("ARRL-FD", _T_FIELD_DAY),
    ("ARRL-FIELD-DAY", _T_FIELD_DAY),
    ("FIELD-DAY", _T_FIELD_DAY),
    ("ARRL-DX", _T_RST_TEXT),
    ("CQ-WW", _T_CQ_ZONE),
    ("CQWW", _T_CQ_ZONE),
    ("CQ-WPX", _T_SERIAL),
    ("CQWPX", _T_SERIAL),
    ("WPX", _T_SERIAL),
    ("IARU", _T_ITU_ZONE),
    ("NAQP", _T_NAME_LOCATION),
    ("NA-SPRINT", _T_NAME_LOCATION),
    ("K1USN-SST", _T_NAME_LOCATION),
]


def lookup_contest_template(contest_id: str) -> dict[str, list[str]] | None:
    key = re.sub(r"[\s_]+", "-", contest_id.strip().upper())
    best: dict[str, list[str]] | None = None
    best_len = -1
    for prefix, template in CONTEST_TEMPLATE_PREFIXES:
        if key.startswith(prefix) and len(prefix) > best_len:
            best, best_len = template, len(prefix)
    return best


@dataclass
class ParsedFile:
    filename: str
    fmt: str
    records: list[dict[str, Any]]
    columns: list[str]
    automap: dict[str, str]
    warnings: list[str]


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS import_batches (
                id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                source_count INTEGER NOT NULL DEFAULT 0,
                total_records INTEGER NOT NULL DEFAULT 0,
                normalized_records INTEGER NOT NULL DEFAULT 0,
                duplicate_records INTEGER NOT NULL DEFAULT 0,
                conflict_records INTEGER NOT NULL DEFAULT 0,
                export_path TEXT
            );

            CREATE TABLE IF NOT EXISTS source_files (
                id TEXT PRIMARY KEY,
                batch_id TEXT NOT NULL,
                filename TEXT NOT NULL,
                format TEXT NOT NULL,
                status TEXT NOT NULL,
                record_count INTEGER NOT NULL,
                columns_json TEXT NOT NULL,
                automap_json TEXT NOT NULL,
                warnings_json TEXT NOT NULL,
                preview_json TEXT NOT NULL,
                raw_text TEXT,
                FOREIGN KEY(batch_id) REFERENCES import_batches(id)
            );

            CREATE TABLE IF NOT EXISTS normalized_qsos (
                id TEXT PRIMARY KEY,
                batch_id TEXT NOT NULL,
                source_file_id TEXT NOT NULL,
                station_callsign TEXT,
                call TEXT,
                qso_date TEXT,
                time_on TEXT,
                band TEXT,
                freq TEXT,
                mode TEXT,
                submode TEXT,
                contest_id TEXT,
                my_pota_ref TEXT,
                pota_ref TEXT,
                status TEXT NOT NULL,
                record_json TEXT NOT NULL,
                FOREIGN KEY(batch_id) REFERENCES import_batches(id)
            );

            CREATE INDEX IF NOT EXISTS idx_qso_core
            ON normalized_qsos(call, band, mode, qso_date, time_on);

            CREATE TABLE IF NOT EXISTS conflicts (
                id TEXT PRIMARY KEY,
                batch_id TEXT NOT NULL,
                incoming_qso_id TEXT NOT NULL,
                existing_qso_id TEXT,
                reason TEXT NOT NULL,
                fields_json TEXT NOT NULL,
                status TEXT NOT NULL
            );
            """
        )


def row_to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    return dict(row) if row is not None else None


def detect_format(filename: str, content: bytes) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix in {".adi", ".adif"}:
        return "ADI"
    if suffix == ".adx":
        return "ADX"
    if suffix in {".cbr", ".log"}:
        return "CABRILLO"
    if suffix == ".tsv":
        return "TSV"
    if suffix == ".csv":
        return "CSV"
    if suffix == ".xlsx":
        return "XLSX"
    if suffix == ".json":
        return "JSON"
    head = content[:256].decode("utf-8", errors="ignore").lstrip()
    if head.startswith("{") or head.startswith("["):
        return "JSON"
    if head.startswith("<"):
        return "ADX"
    if "QSO:" in head:
        return "CABRILLO"
    if "<eor>" in head.lower():
        return "ADI"
    return "CSV"


def parse_file(filename: str, content: bytes) -> ParsedFile:
    fmt = detect_format(filename, content)
    warnings: list[str] = []
    if fmt == "XLSX":
        records = parse_xlsx(content)
    else:
        text = content.decode("utf-8-sig", errors="replace")
        if fmt == "ADI":
            records = parse_adi(text)
        elif fmt == "ADX":
            records = parse_adx(text)
        elif fmt == "CABRILLO":
            records, warnings = parse_cabrillo(text)
        elif fmt in {"CSV", "TSV"}:
            records = parse_delimited(text, delimiter="\t" if fmt == "TSV" else None)
        elif fmt == "JSON":
            records = parse_json(text)
        else:
            records = parse_delimited(text)
    columns = sorted({key for record in records for key in record.keys()})
    return ParsedFile(
        filename=filename,
        fmt=fmt,
        records=records,
        columns=columns,
        automap=auto_map(columns),
        warnings=warnings,
    )


def parse_adi(text: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for chunk in re.split(r"<eor\s*>", text, flags=re.IGNORECASE):
        cursor = 0
        record: dict[str, str] = {}
        while cursor < len(chunk):
            match = re.search(
                r"<([^:>\s]+):(\d+)(?::[^>]*)?>", chunk[cursor:], re.IGNORECASE
            )
            if not match:
                break
            field = match.group(1).upper()
            length = int(match.group(2))
            value_start = cursor + match.end()
            value = chunk[value_start : value_start + length]
            if field != "EOH":
                record[field] = value.strip()
            cursor = value_start + length
        if record:
            records.append(record)
    return records


def parse_adx(text: str) -> list[dict[str, str]]:
    root = ET.fromstring(text)
    records: list[dict[str, str]] = []
    for record_node in root.iter():
        if _local_name(record_node.tag).lower() != "record":
            continue
        record: dict[str, str] = {}
        for child in list(record_node):
            record[_local_name(child.tag).upper()] = (child.text or "").strip()
        if record:
            records.append(record)
    if not records:
        record = {
            _local_name(child.tag).upper(): (child.text or "").strip()
            for child in list(root)
            if len(list(child)) == 0
        }
        if record:
            records.append(record)
    return records


def _local_name(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def parse_cabrillo(text: str) -> tuple[list[dict[str, str]], list[str]]:
    records: list[dict[str, str]] = []
    warnings: list[str] = []
    contest_id = ""
    template: dict[str, list[str]] | None = None
    for line in text.splitlines():
        clean = line.strip()
        upper = clean.upper()
        if upper.startswith("CONTEST:"):
            contest_id = clean.split(":", 1)[1].strip()
            template = lookup_contest_template(contest_id)
            continue
        if not upper.startswith("QSO:"):
            continue
        parts = clean.split()
        if len(parts) < 5:
            warnings.append(
                f"Linea QSO de Cabrillo demasiado corta, omitida: {clean[:80]}"
            )
            continue
        # QSO: freq mode date time <sent exchange tokens> <received exchange tokens>
        record: dict[str, str] = {
            "FREQ": parts[1],
            "MODE": parts[2],
            "QSO_DATE": parts[3],
            "TIME_ON": parts[4],
            "CONTEST_ID": contest_id,
        }
        tokens = parts[5:]
        layout = (
            template["sent"] + template["rcvd"]
            if template is not None
            # Generic fallback: own call, RST, exch, their call, RST, exch.
            else [
                "STATION_CALLSIGN",
                "RST_SENT",
                "STX_STRING",
                "CALL",
                "RST_RCVD",
                "SRX_STRING",
            ]
        )
        for index, field in enumerate(layout):
            if field and index < len(tokens):
                record[field] = tokens[index]
        if template is None and "CALL" not in record and tokens:
            record["CALL"] = tokens[-1]
        if template is not None and len(tokens) != len(layout):
            warnings.append(
                f"Cabrillo {contest_id}: {len(tokens)} tokens vs {len(layout)} esperados: {clean[:80]}"
            )
        records.append({key: value for key, value in record.items() if value != ""})
    return records, warnings


def parse_delimited(text: str, delimiter: str | None = None) -> list[dict[str, str]]:
    sample = text[:2048]
    if delimiter is None:
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
            delimiter = dialect.delimiter
        except csv.Error:
            delimiter = ","
    reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
    return [
        {str(k).strip(): str(v or "").strip() for k, v in row.items()} for row in reader
    ]


def parse_xlsx(content: bytes) -> list[dict[str, str]]:
    from openpyxl import load_workbook

    workbook = load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    sheet = workbook.active
    rows = list(sheet.iter_rows(values_only=True))
    if not rows:
        return []
    headers = [
        str(value).strip() if value is not None else f"COL_{index + 1}"
        for index, value in enumerate(rows[0])
    ]
    records: list[dict[str, str]] = []
    for row in rows[1:]:
        record = {
            headers[index]: "" if value is None else str(value).strip()
            for index, value in enumerate(row)
            if index < len(headers)
        }
        if any(record.values()):
            records.append(record)
    return records


def parse_json(text: str) -> list[dict[str, Any]]:
    payload = json.loads(text)
    if isinstance(payload, dict):
        for key in ("records", "qsos", "qso", "data"):
            if isinstance(payload.get(key), list):
                payload = payload[key]
                break
        else:
            payload = [payload]
    if not isinstance(payload, list):
        raise ValueError("La raiz del JSON debe ser un objeto o un arreglo")
    return [flatten_json(item) for item in payload if isinstance(item, dict)]


def flatten_json(value: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    flat: dict[str, Any] = {}
    for key, item in value.items():
        next_key = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(item, dict):
            flat.update(flatten_json(item, next_key))
        else:
            flat[next_key] = item
    return flat


def auto_map(columns: list[str]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for column in columns:
        normalized = re.sub(r"[^a-z0-9]+", "_", column.lower()).strip("_")
        if column.upper() in ADIF_FIELD_OPTIONS or column.upper().startswith("APP_"):
            mapping[column] = column.upper()
        elif normalized in ALIASES:
            mapping[column] = ALIASES[normalized]
    return mapping


def normalize_records(
    records: list[dict[str, Any]],
    mapping: dict[str, str] | None = None,
    inference: dict[str, bool] | None = None,
) -> list[dict[str, str]]:
    mapping = mapping or {}
    inference = inference or {
        "infer_band_from_freq": True,
        "maidenhead_geoconversion": True,
        "state_from_exchange": True,
    }
    # Mode/date/time normalisation is mandatory cleanup (not an optional toggle);
    # it can be disabled explicitly but defaults to on.
    do_mode = inference.get("normalize_mode_submode", True)
    do_dates = inference.get("normalize_dates", True)
    normalized: list[dict[str, str]] = []
    for record in records:
        output: dict[str, str] = {}
        for key, value in record.items():
            target = mapping.get(key) or (
                key.upper()
                if key.upper() in ADIF_FIELD_OPTIONS or key.upper().startswith("APP_")
                else None
            )
            if not target:
                continue
            output[target] = clean_value(value)
        if "MODE" in output and do_mode:
            mode, submode = normalize_mode(output["MODE"], output.get("SUBMODE"))
            output["MODE"] = mode
            if submode:
                output["SUBMODE"] = submode
        if "FREQ" in output:
            output["FREQ"] = normalize_freq(output["FREQ"])
            if inference.get("infer_band_from_freq", True) and not output.get("BAND"):
                output["BAND"] = band_from_freq(output["FREQ"])
        if "QSO_DATE" in output and do_dates:
            output["QSO_DATE"] = normalize_date(output["QSO_DATE"])
        if "TIME_ON" in output:
            output["TIME_ON"] = normalize_time(output["TIME_ON"])
        if inference.get("maidenhead_geoconversion", True) and not output.get(
            "GRIDSQUARE"
        ):
            lat = parse_coordinate(output.get("LAT", ""), is_lat=True)
            lon = parse_coordinate(output.get("LON", ""), is_lat=False)
            if lat is not None and lon is not None:
                output["GRIDSQUARE"] = maidenhead(lat, lon)
        if inference.get("state_from_exchange", True) and not output.get("STATE"):
            exchange = output.get("SRX_STRING") or output.get("SRX") or ""
            if exchange:
                state, ve_prov = state_from_exchange(exchange)
                if state:
                    output["STATE"] = state
                elif ve_prov and not output.get("VE_PROV"):
                    output["VE_PROV"] = ve_prov
        normalize_booleans(output)
        if output.get("CALL"):
            output["CALL"] = output["CALL"].upper()
        if output.get("GRIDSQUARE"):
            output["GRIDSQUARE"] = (
                output["GRIDSQUARE"][:4].upper() + output["GRIDSQUARE"][4:].lower()
            )
        normalized.append(output)
    return normalized


def clean_value(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_mode(mode: str, submode: str | None = None) -> tuple[str, str | None]:
    raw = mode.strip().upper().replace(" ", "")
    mapping = {
        "PH": ("SSB", None),
        "PHONE": ("SSB", None),
        "RY": ("RTTY", None),
        "RTTY": ("RTTY", None),
        "C4FM": ("DIGITALVOICE", "C4FM"),
        "DMR": ("DIGITALVOICE", "DMR"),
        "DSTAR": ("DIGITALVOICE", "DSTAR"),
        "VARAHF": ("DYNAMIC", "VARA HF"),
        "VARAFM": ("DYNAMIC", "VARA FM"),
    }
    return mapping.get(raw, (raw, submode.strip().upper() if submode else None))


def normalize_freq(freq: str) -> str:
    value = freq.strip().lower().replace("mhz", "").replace(",", ".")
    try:
        number = float(value)
        if number > 100000:
            number = number / 1_000_000
        elif number > 1000:
            number = number / 1000
        return f"{number:.6f}".rstrip("0").rstrip(".")
    except ValueError:
        return freq.strip()


def band_from_freq(freq: str) -> str:
    try:
        mhz = float(freq)
    except ValueError:
        return ""
    bands = [
        (1.8, 2.0, "160m"),
        (3.5, 4.0, "80m"),
        (5.0, 5.5, "60m"),
        (7.0, 7.3, "40m"),
        (10.1, 10.15, "30m"),
        (14.0, 14.35, "20m"),
        (18.068, 18.168, "17m"),
        (21.0, 21.45, "15m"),
        (24.89, 24.99, "12m"),
        (28.0, 29.7, "10m"),
        (50.0, 54.0, "6m"),
        (144.0, 148.0, "2m"),
        (420.0, 450.0, "70cm"),
    ]
    for low, high, band in bands:
        if low <= mhz <= high:
            return band
    return ""


def parse_coordinate(value: str, is_lat: bool) -> float | None:
    """Accept decimal degrees ("40.43", "-74.0") or ADIF format ("N040 26.000")."""
    clean = value.strip()
    if not clean:
        return None
    try:
        return float(clean.replace(",", "."))
    except ValueError:
        pass
    match = re.match(
        r"^([NSEW])\s*(\d{1,3})\s+(\d{1,2}(?:[.,]\d+)?)$", clean, re.IGNORECASE
    )
    if not match:
        return None
    hemisphere, degrees, minutes = match.groups()
    decimal = int(degrees) + float(minutes.replace(",", ".")) / 60.0
    if hemisphere.upper() in {"S", "W"}:
        decimal = -decimal
    limit = 90.0 if is_lat else 180.0
    return decimal if -limit <= decimal <= limit else None


def maidenhead(lat: float, lon: float) -> str:
    """Convert decimal lat/lon to a 6-character Maidenhead locator (ADIF GRIDSQUARE)."""
    lat = min(max(lat, -90.0), 90.0) + 90.0
    lon = min(max(lon, -180.0), 180.0) + 180.0
    field_lon = chr(ord("A") + int(lon // 20))
    field_lat = chr(ord("A") + int(lat // 10))
    square_lon = str(int((lon % 20) // 2))
    square_lat = str(int((lat % 10) // 1))
    sub_lon = chr(ord("a") + int((lon % 2) / (2 / 24)))
    sub_lat = chr(ord("a") + int((lat % 1) / (1 / 24)))
    return f"{field_lon}{field_lat}{square_lon}{square_lat}{sub_lon}{sub_lat}"


def state_from_exchange(value: str) -> tuple[str | None, str | None]:
    """Map a contest exchange token to (STATE, VE_PROV) when recognisable."""
    token = re.sub(r"[^A-Za-z]", "", value).upper()
    if token in US_STATES:
        return token, None
    if token in CA_PROVINCES:
        return None, token
    return None, None


def normalize_date(value: str) -> str:
    clean = value.strip()
    if re.fullmatch(r"\d{8}", clean):
        return clean
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(clean, fmt).strftime("%Y%m%d")
        except ValueError:
            continue
    return clean


def normalize_time(value: str) -> str:
    clean = value.strip().replace(":", "")
    if re.fullmatch(r"\d{4}", clean):
        return f"{clean}00"
    if re.fullmatch(r"\d{6}", clean):
        return clean
    return clean


def normalize_booleans(record: dict[str, str]) -> None:
    for key, value in list(record.items()):
        if (
            key.endswith("_QSL_RCVD")
            or key.endswith("_QSL_SENT")
            or key in {"QSL_RCVD", "QSL_SENT"}
        ):
            upper = value.upper()
            if upper in {"TRUE", "YES", "1", "Y"}:
                record[key] = "Y"
            elif upper in {"FALSE", "NO", "0", "N"}:
                record[key] = "N"


def create_batch(files: list[tuple[str, bytes]]) -> dict[str, Any]:
    batch_id = str(uuid.uuid4())
    now = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    parsed_files = [parse_file(filename, content) for filename, content in files]
    total_records = sum(len(item.records) for item in parsed_files)
    with connect() as conn:
        conn.execute(
            "INSERT INTO import_batches(id, status, created_at, source_count, total_records) VALUES(?,?,?,?,?)",
            (batch_id, "waiting_mapper", now, len(parsed_files), total_records),
        )
        for parsed in parsed_files:
            source_id = str(uuid.uuid4())
            conn.execute(
                """
                INSERT INTO source_files(
                    id, batch_id, filename, format, status, record_count, columns_json,
                    automap_json, warnings_json, preview_json, raw_text
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    source_id,
                    batch_id,
                    parsed.filename,
                    parsed.fmt,
                    "parsed",
                    len(parsed.records),
                    json.dumps(parsed.columns),
                    json.dumps(parsed.automap),
                    json.dumps(parsed.warnings),
                    json.dumps(parsed.records[:20]),
                    json.dumps(parsed.records),
                ),
            )
    return get_batch(batch_id)


def get_batch(batch_id: str) -> dict[str, Any]:
    with connect() as conn:
        batch = row_to_dict(
            conn.execute(
                "SELECT * FROM import_batches WHERE id = ?", (batch_id,)
            ).fetchone()
        )
        if batch is None:
            raise KeyError(batch_id)
        sources = [
            dict(row)
            for row in conn.execute(
                "SELECT * FROM source_files WHERE batch_id = ?", (batch_id,)
            )
        ]
        qsos = [
            dict(row)
            for row in conn.execute(
                "SELECT * FROM normalized_qsos WHERE batch_id = ?", (batch_id,)
            )
        ]
        conflicts = [
            dict(row)
            for row in conn.execute(
                "SELECT * FROM conflicts WHERE batch_id = ?", (batch_id,)
            )
        ]
    for source in sources:
        source["columns"] = json.loads(source.pop("columns_json"))
        source["automap"] = json.loads(source.pop("automap_json"))
        source["warnings"] = json.loads(source.pop("warnings_json"))
        source["preview"] = json.loads(source.pop("preview_json"))
        source.pop("raw_text", None)
    for qso in qsos:
        qso["record"] = json.loads(qso.pop("record_json"))
    qso_index = {qso["id"]: qso for qso in qsos}
    for conflict in conflicts:
        conflict["fields"] = json.loads(conflict.pop("fields_json"))
        base = qso_index.get(conflict.get("incoming_qso_id")) or qso_index.get(
            conflict.get("existing_qso_id")
        )
        conflict["summary"] = {
            "call": base.get("call") if base else None,
            "band": base.get("band") if base else None,
            "mode": base.get("mode") if base else None,
            "qso_date": base.get("qso_date") if base else None,
            "time_on": base.get("time_on") if base else None,
        }
    batch["sources"] = sources
    batch["qsos"] = qsos[:100]
    batch["conflicts"] = conflicts
    batch["adif_version"] = ADIF_VERSION
    batch["field_options"] = ADIF_FIELD_OPTIONS
    return batch


def normalize_batch(
    batch_id: str, mapping: dict[str, str], inference: dict[str, bool]
) -> dict[str, Any]:
    with connect() as conn:
        sources = [
            dict(row)
            for row in conn.execute(
                "SELECT * FROM source_files WHERE batch_id = ?", (batch_id,)
            )
        ]
        conn.execute("DELETE FROM normalized_qsos WHERE batch_id = ?", (batch_id,))
        total = 0
        for source in sources:
            records = json.loads(source["raw_text"] or "[]")
            source_mapping = json.loads(source["automap_json"])
            source_mapping.update(mapping)
            normalized = normalize_records(records, source_mapping, inference)
            for record in normalized:
                qso_id = str(uuid.uuid4())
                conn.execute(
                    """
                    INSERT INTO normalized_qsos(
                        id, batch_id, source_file_id, station_callsign, call, qso_date,
                        time_on, band, freq, mode, submode, contest_id, my_pota_ref,
                        pota_ref, status, record_json
                    ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        qso_id,
                        batch_id,
                        source["id"],
                        record.get("STATION_CALLSIGN"),
                        record.get("CALL"),
                        record.get("QSO_DATE"),
                        record.get("TIME_ON"),
                        record.get("BAND"),
                        record.get("FREQ"),
                        record.get("MODE"),
                        record.get("SUBMODE"),
                        record.get("CONTEST_ID"),
                        record.get("MY_POTA_REF"),
                        record.get("POTA_REF"),
                        "normalized",
                        json.dumps(record),
                    ),
                )
            total += len(normalized)
        conn.execute(
            "UPDATE import_batches SET status = ?, normalized_records = ? WHERE id = ?",
            ("normalized", total, batch_id),
        )
    return get_batch(batch_id)


def dedupe_batch(batch_id: str, tolerance_minutes: int = 15) -> dict[str, Any]:
    with connect() as conn:
        conn.execute("DELETE FROM conflicts WHERE batch_id = ?", (batch_id,))
        current = [
            dict(row)
            for row in conn.execute(
                "SELECT * FROM normalized_qsos WHERE batch_id = ?", (batch_id,)
            )
        ]
        duplicate_count = 0
        conflict_count = 0
        seen: list[dict[str, Any]] = []
        for record in current:
            duplicate = find_duplicate(record, seen, tolerance_minutes)
            if duplicate is not None:
                duplicate_count += 1
                status = "duplicate"
                reason = "temporal_core_match"
                if has_conflict(record, duplicate):
                    conflict_count += 1
                    status = "conflict"
                    conn.execute(
                        "INSERT INTO conflicts(id,batch_id,incoming_qso_id,existing_qso_id,reason,fields_json,status) VALUES(?,?,?,?,?,?,?)",
                        (
                            str(uuid.uuid4()),
                            batch_id,
                            record["id"],
                            duplicate.get("id"),
                            reason,
                            json.dumps(diff_fields(record, duplicate)),
                            "open",
                        ),
                    )
                conn.execute(
                    "UPDATE normalized_qsos SET status = ? WHERE id = ?",
                    (status, record["id"]),
                )
            else:
                seen.append(record)
                conn.execute(
                    "UPDATE normalized_qsos SET status = ? WHERE id = ?",
                    ("unique", record["id"]),
                )
        conn.execute(
            "UPDATE import_batches SET status = ?, duplicate_records = ?, conflict_records = ? WHERE id = ?",
            ("deduped", duplicate_count, conflict_count, batch_id),
        )
    return get_batch(batch_id)


def dedup_profile(record: dict[str, Any], candidate: dict[str, Any]) -> str:
    """Select the contextual matching policy for a candidate pair.

    Per INVESTIGACION.MD: contest rules prevail over park exceptions; POTA
    activations get a same-UTC-day window with a park-reference exception; all
    other contacts fall back to the configurable ClubLog-style window.
    """
    if record.get("contest_id") and candidate.get("contest_id"):
        return "contest"
    if any(
        (
            record.get("pota_ref"),
            candidate.get("pota_ref"),
            record.get("my_pota_ref"),
            candidate.get("my_pota_ref"),
        )
    ):
        return "pota"
    return "general"


def same_utc_day(record: dict[str, Any], candidate: dict[str, Any]) -> bool:
    return bool(record.get("qso_date")) and record.get("qso_date") == candidate.get(
        "qso_date"
    )


def find_duplicate(
    record: dict[str, Any], candidates: list[dict[str, Any]], tolerance_minutes: int
) -> dict[str, Any] | None:
    for candidate in candidates:
        if record.get("call") != candidate.get("call"):
            continue
        if record.get("band") != candidate.get("band") or record.get(
            "mode"
        ) != candidate.get("mode"):
            continue
        profile = dedup_profile(record, candidate)
        if profile == "contest":
            # Contest rules prevail absolutely: same call/band/mode within the
            # same CONTEST_ID is a duplicate regardless of clock skew, and park
            # exceptions are ignored.
            if record.get("contest_id") != candidate.get("contest_id"):
                continue
            return candidate
        if profile == "pota":
            # A change in either park reference makes the contact legitimate.
            if record.get("pota_ref") != candidate.get("pota_ref"):
                continue
            if record.get("my_pota_ref") != candidate.get("my_pota_ref"):
                continue
            if same_utc_day(record, candidate):
                return candidate
            continue
        if within_time_window(
            record.get("qso_date"),
            record.get("time_on"),
            candidate.get("qso_date"),
            candidate.get("time_on"),
            tolerance_minutes,
        ):
            return candidate
    return None


def within_time_window(
    date_a: str | None,
    time_a: str | None,
    date_b: str | None,
    time_b: str | None,
    minutes: int,
) -> bool:
    try:
        dt_a = datetime.strptime(
            f"{date_a or ''}{(time_a or '000000')[:6]}", "%Y%m%d%H%M%S"
        )
        dt_b = datetime.strptime(
            f"{date_b or ''}{(time_b or '000000')[:6]}", "%Y%m%d%H%M%S"
        )
    except ValueError:
        return date_a == date_b
    return abs(dt_a - dt_b) <= timedelta(minutes=minutes)


def has_conflict(record: dict[str, Any], duplicate: dict[str, Any]) -> bool:
    left = json.loads(record["record_json"])
    right = json.loads(duplicate["record_json"])
    for field in ("RST_SENT", "RST_RCVD", "NAME", "QTH", "STATE"):
        if left.get(field) and right.get(field) and left.get(field) != right.get(field):
            return True
    return False


def diff_fields(
    record: dict[str, Any], duplicate: dict[str, Any]
) -> dict[str, dict[str, str]]:
    left = json.loads(record["record_json"])
    right = json.loads(duplicate["record_json"])
    fields: dict[str, dict[str, str]] = {}
    for field in sorted(set(left) | set(right)):
        if left.get(field) != right.get(field):
            fields[field] = {
                "incoming": left.get(field, ""),
                "existing": right.get(field, ""),
            }
    return fields


def _is_qsl_field(field: str) -> bool:
    return (
        field.endswith("_QSL_RCVD")
        or field.endswith("_QSL_SENT")
        or field in {"QSL_RCVD", "QSL_SENT"}
    )


def _merge_field(field: str, incoming: str, existing: str) -> str:
    """Enriched incremental merge for a single field (estrategia 'merge')."""
    if not existing and incoming:
        return incoming
    if not incoming:
        return existing
    if _is_qsl_field(field):
        # Promote to the strongest confirmation.
        return "Y" if "Y" in (incoming.upper(), existing.upper()) else existing
    if field in {"COMMENT", "NOTES"} and incoming != existing:
        return f"{existing} | {incoming}"
    return existing  # keep the persisted value as source of truth


def _qso_timestamp(record: dict[str, str]) -> datetime | None:
    stamp = f"{record.get('QSO_DATE', '')}{(record.get('TIME_ON') or '000000')[:6]}"
    try:
        return datetime.strptime(stamp, "%Y%m%d%H%M%S")
    except ValueError:
        return None


def _newer_side(incoming: dict[str, str], existing: dict[str, str]) -> str:
    """Best-effort 'use newer': compare QSO timestamps, prefer incoming on ties."""
    ts_in = _qso_timestamp(incoming)
    ts_ex = _qso_timestamp(existing)
    if ts_in is None or ts_ex is None:
        return "incoming"
    return "existing" if ts_ex > ts_in else "incoming"


def _write_qso_record(
    conn: sqlite3.Connection, qso_id: str, record: dict[str, str], status: str
) -> None:
    conn.execute(
        """
        UPDATE normalized_qsos SET
            status = ?, record_json = ?, station_callsign = ?, call = ?, qso_date = ?,
            time_on = ?, band = ?, freq = ?, mode = ?, submode = ?, contest_id = ?,
            my_pota_ref = ?, pota_ref = ?
        WHERE id = ?
        """,
        (
            status,
            json.dumps(record),
            record.get("STATION_CALLSIGN"),
            record.get("CALL"),
            record.get("QSO_DATE"),
            record.get("TIME_ON"),
            record.get("BAND"),
            record.get("FREQ"),
            record.get("MODE"),
            record.get("SUBMODE"),
            record.get("CONTEST_ID"),
            record.get("MY_POTA_REF"),
            record.get("POTA_REF"),
            qso_id,
        ),
    )


def resolve_conflict(
    batch_id: str,
    conflict_id: str,
    strategy: str = "merge",
    field_choices: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Resolve one conflict and consolidate into the surviving (existing) QSO.

    Strategies: use_existing, use_incoming (replace), merge (enriched), use_newer.
    `field_choices` maps a field to 'incoming'/'existing' and overrides the
    strategy per field (interfaz interactiva estilo merge de codigo).
    """
    field_choices = field_choices or {}
    with connect() as conn:
        conflict = row_to_dict(
            conn.execute(
                "SELECT * FROM conflicts WHERE id = ? AND batch_id = ?",
                (conflict_id, batch_id),
            ).fetchone()
        )
        if conflict is None:
            raise KeyError(conflict_id)
        incoming_row = row_to_dict(
            conn.execute(
                "SELECT * FROM normalized_qsos WHERE id = ?",
                (conflict["incoming_qso_id"],),
            ).fetchone()
        )
        existing_row = row_to_dict(
            conn.execute(
                "SELECT * FROM normalized_qsos WHERE id = ?",
                (conflict["existing_qso_id"],),
            ).fetchone()
        )
        if incoming_row is None or existing_row is None:
            raise KeyError(conflict_id)

        incoming = json.loads(incoming_row["record_json"])
        existing = json.loads(existing_row["record_json"])
        diff = json.loads(conflict["fields_json"])
        newer = _newer_side(incoming, existing) if strategy == "use_newer" else None

        merged = dict(existing)
        for field, values in diff.items():
            inc = values.get("incoming", "")
            exi = values.get("existing", "")
            if field in field_choices:
                merged[field] = inc if field_choices[field] == "incoming" else exi
            elif strategy == "use_incoming":
                merged[field] = inc
            elif strategy == "use_existing":
                merged[field] = exi
            elif strategy == "use_newer":
                merged[field] = inc if newer == "incoming" else exi
            elif strategy == "merge":
                merged[field] = _merge_field(field, inc, exi)
            else:  # manual without an explicit choice keeps the survivor value
                merged[field] = exi
        merged = {key: value for key, value in merged.items() if value != ""}

        _write_qso_record(conn, existing_row["id"], merged, "unique")
        conn.execute(
            "UPDATE normalized_qsos SET status = 'duplicate' WHERE id = ?",
            (incoming_row["id"],),
        )
        conn.execute(
            "UPDATE conflicts SET status = 'resolved' WHERE id = ?",
            (conflict_id,),
        )
        open_conflicts = conn.execute(
            "SELECT COUNT(*) FROM conflicts WHERE batch_id = ? AND status = 'open'",
            (batch_id,),
        ).fetchone()[0]
        duplicates = conn.execute(
            "SELECT COUNT(*) FROM normalized_qsos WHERE batch_id = ? AND status = 'duplicate'",
            (batch_id,),
        ).fetchone()[0]
        conn.execute(
            "UPDATE import_batches SET conflict_records = ?, duplicate_records = ? WHERE id = ?",
            (open_conflicts, duplicates, batch_id),
        )
    return get_batch(batch_id)


def export_adi(batch_id: str) -> str:
    with connect() as conn:
        rows = [
            dict(row)
            for row in conn.execute(
                "SELECT * FROM normalized_qsos WHERE batch_id = ? AND status NOT IN ('duplicate', 'conflict')",
                (batch_id,),
            )
        ]
        path = DB_PATH.parent / f"{batch_id}.adi"
        with path.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(
                f"Generated by 6SNT.ADIF-HUB <ADIF_VER:5>{ADIF_VERSION}<EOH>\n"
            )
            for row in rows:
                record = json.loads(row["record_json"])
                handle.write(format_adi_record(record) + "\n")
        conn.execute(
            "UPDATE import_batches SET status = ?, export_path = ? WHERE id = ?",
            ("ready_to_export", str(path), batch_id),
        )
    return str(path)


def format_adi_record(record: dict[str, str]) -> str:
    parts = []
    for key, value in record.items():
        if value == "":
            continue
        parts.append(f"<{key}:{len(value)}>{value}")
    parts.append("<EOR>")
    return "".join(parts)
