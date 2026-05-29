"""Genera un set de prueba con datos FICTICIOS en varios formatos y estructuras.

Salida: carpeta sample_logs/ con ADI, ADIF, ADX (XML), Cabrillo (varios concursos),
CSV (cabeceras en español), TSV, JSON (anidado + APP_) y XLSX. Incluye duplicados y
un conflicto deliberados entre archivos para probar dedupe y resolución.

Todos los indicativos y datos son inventados (estilo N0CALL/...TEST).
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sample_logs"


def adi_record(rec: dict[str, str]) -> str:
    parts = []
    for key, value in rec.items():
        text = str(value)
        parts.append(f"<{key}:{len(text.encode('utf-8'))}>{text}")
    parts.append("<EOR>")
    return "".join(parts)


def write_adi(path: Path, note: str, records: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(f"{note}\n<ADIF_VER:5>3.1.7<PROGRAMID:13>6SNT.ADIF-HUB<EOH>\n")
        for rec in records:
            fh.write(adi_record(rec) + "\n")


def write_adx(path: Path, records: list[dict[str, str]]) -> None:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', "<ADX>", "  <HEADER>", "    <ADIF_VER>3.1.7</ADIF_VER>", "  </HEADER>", "  <RECORDS>"]
    for rec in records:
        lines.append("    <RECORD>")
        for key, value in rec.items():
            lines.append(f"      <{key}>{value}</{key}>")
        lines.append("    </RECORD>")
    lines += ["  </RECORDS>", "</ADX>", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_cabrillo(path: Path, contest: str, callsign: str, qso_lines: list[str]) -> None:
    body = [
        "START-OF-LOG: 3.0",
        f"CONTEST: {contest}",
        f"CALLSIGN: {callsign}",
        "CATEGORY-OPERATOR: SINGLE-OP",
        *[f"QSO: {line}" for line in qso_lines],
        "END-OF-LOG:",
        "",
    ]
    path.write_text("\n".join(body), encoding="utf-8")


def write_delimited(path: Path, headers: list[str], rows: list[list[str]], sep: str) -> None:
    lines = [sep.join(headers)] + [sep.join(str(c) for c in row) for row in rows]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(exist_ok=True)

    # 1) ADI estándar (10) — modos variados, RST, nombre, QTH, grid.
    adi = [
        {"CALL": "WW1AAA", "QSO_DATE": "20260528", "TIME_ON": "1200", "BAND": "20m", "FREQ": "14.030", "MODE": "CW", "RST_SENT": "599", "RST_RCVD": "599", "NAME": "Ana", "QTH": "Madrid"},
        {"CALL": "K9TEST", "QSO_DATE": "20260528", "TIME_ON": "1215", "BAND": "40m", "FREQ": "7.120", "MODE": "PH", "RST_SENT": "59", "RST_RCVD": "57", "NAME": "Bob"},
        {"CALL": "N0CALL", "QSO_DATE": "20260528", "TIME_ON": "1230", "BAND": "20m", "FREQ": "14.250", "MODE": "PH", "RST_SENT": "59", "RST_RCVD": "59"},
        {"CALL": "G3FAKE", "QSO_DATE": "20260528", "TIME_ON": "1242", "BAND": "15m", "FREQ": "21.030", "MODE": "CW", "RST_SENT": "599", "RST_RCVD": "589"},
        {"CALL": "VE3MOCK", "QSO_DATE": "20260528", "TIME_ON": "1305", "BAND": "20m", "FREQ": "14.074", "MODE": "FT8", "RST_SENT": "-12", "RST_RCVD": "-08", "GRIDSQUARE": "FN03"},
        {"CALL": "LU1ZZZ", "QSO_DATE": "20260528", "TIME_ON": "1320", "BAND": "10m", "FREQ": "28.480", "MODE": "PH", "RST_SENT": "59", "RST_RCVD": "55"},
        {"CALL": "JA1TEST", "QSO_DATE": "20260528", "TIME_ON": "1338", "BAND": "20m", "FREQ": "14.205", "MODE": "RY", "RST_SENT": "599", "RST_RCVD": "599"},
        {"CALL": "DL0FAKE", "QSO_DATE": "20260528", "TIME_ON": "1402", "BAND": "40m", "FREQ": "7.040", "MODE": "CW", "RST_SENT": "559", "RST_RCVD": "569"},
        {"CALL": "PY2MOCK", "QSO_DATE": "20260528", "TIME_ON": "1420", "BAND": "17m", "FREQ": "18.100", "MODE": "CW", "RST_SENT": "599", "RST_RCVD": "599"},
        {"CALL": "ZL4TEST", "QSO_DATE": "20260528", "TIME_ON": "1455", "BAND": "20m", "FREQ": "14.180", "MODE": "C4FM", "RST_SENT": "59", "RST_RCVD": "59"},
    ]
    write_adi(OUT / "adif_standard.adi", "6SNT.ADIF-HUB demo log (datos ficticios)", adi)

    # 2) ADIF tipo WSJT-X (8) — digitales, grids, QSL flags.
    wsjtx = [
        {"CALL": "EA4TEST", "QSO_DATE": "20260527", "TIME_ON": "0901", "BAND": "20m", "FREQ": "14.074", "MODE": "FT8", "RST_SENT": "-05", "RST_RCVD": "-10", "GRIDSQUARE": "IN80", "LOTW_QSL_RCVD": "Y"},
        {"CALL": "F5MOCK", "QSO_DATE": "20260527", "TIME_ON": "0915", "BAND": "30m", "FREQ": "10.136", "MODE": "FT8", "RST_SENT": "+02", "RST_RCVD": "-03", "GRIDSQUARE": "JN18"},
        {"CALL": "OH2FAKE", "QSO_DATE": "20260527", "TIME_ON": "0930", "BAND": "40m", "FREQ": "7.074", "MODE": "FT4", "RST_SENT": "-15", "RST_RCVD": "-12", "GRIDSQUARE": "KP20"},
        {"CALL": "I0TEST", "QSO_DATE": "20260527", "TIME_ON": "0948", "BAND": "20m", "FREQ": "14.074", "MODE": "FT8", "RST_SENT": "-01", "RST_RCVD": "+05", "GRIDSQUARE": "JN61", "EQSL_QSL_RCVD": "Y"},
        {"CALL": "SP9MOCK", "QSO_DATE": "20260527", "TIME_ON": "1003", "BAND": "15m", "FREQ": "21.074", "MODE": "FT8", "RST_SENT": "-08", "RST_RCVD": "-08", "GRIDSQUARE": "JO90"},
        {"CALL": "CT1FAKE", "QSO_DATE": "20260527", "TIME_ON": "1019", "BAND": "20m", "FREQ": "14.080", "MODE": "RTTY", "RST_SENT": "599", "RST_RCVD": "599", "GRIDSQUARE": "IM58"},
        {"CALL": "SV1TEST", "QSO_DATE": "20260527", "TIME_ON": "1031", "BAND": "10m", "FREQ": "28.074", "MODE": "FT8", "RST_SENT": "-18", "RST_RCVD": "-20", "GRIDSQUARE": "KM18"},
        {"CALL": "9A1MOCK", "QSO_DATE": "20260527", "TIME_ON": "1044", "BAND": "12m", "FREQ": "24.915", "MODE": "FT8", "RST_SENT": "-02", "RST_RCVD": "+01", "GRIDSQUARE": "JN85"},
    ]
    write_adi(OUT / "wsjtx_export.adif", "WSJT-X (ficticio)", wsjtx)

    # 3) ADX / XML (6)
    adx = [
        {"CALL": "OZ1TEST", "QSO_DATE": "20260526", "TIME_ON": "2000", "BAND": "80m", "FREQ": "3.573", "MODE": "FT8", "RST_SENT": "-10", "RST_RCVD": "-12"},
        {"CALL": "SM5FAKE", "QSO_DATE": "20260526", "TIME_ON": "2015", "BAND": "40m", "FREQ": "7.030", "MODE": "CW", "RST_SENT": "599", "RST_RCVD": "579"},
        {"CALL": "LA9MOCK", "QSO_DATE": "20260526", "TIME_ON": "2031", "BAND": "20m", "FREQ": "14.060", "MODE": "CW", "RST_SENT": "559", "RST_RCVD": "559"},
        {"CALL": "EI4TEST", "QSO_DATE": "20260526", "TIME_ON": "2050", "BAND": "20m", "FREQ": "14.240", "MODE": "PH", "RST_SENT": "59", "RST_RCVD": "58"},
        {"CALL": "GM3FAKE", "QSO_DATE": "20260526", "TIME_ON": "2102", "BAND": "40m", "FREQ": "7.160", "MODE": "PH", "RST_SENT": "59", "RST_RCVD": "59"},
        {"CALL": "ON4MOCK", "QSO_DATE": "20260526", "TIME_ON": "2118", "BAND": "30m", "FREQ": "10.118", "MODE": "CW", "RST_SENT": "599", "RST_RCVD": "599"},
    ]
    write_adx(OUT / "adx_log.adx", adx)

    # 4) Cabrillo CQ WPX CW (6) — RST + serial
    write_cabrillo(
        OUT / "cqwpx_cw.cbr",
        "CQ-WPX-CW",
        "EA4TEST",
        [
            "14030 CW 2026-05-25 1200 EA4TEST 599 001 K9TEST 599 058",
            "14030 CW 2026-05-25 1201 EA4TEST 599 002 G3FAKE 599 102",
            "21030 CW 2026-05-25 1230 EA4TEST 599 003 JA1TEST 599 233",
            "7030 CW 2026-05-25 1305 EA4TEST 599 004 PY2MOCK 599 017",
            "14030 CW 2026-05-25 1402 EA4TEST 599 005 DL0FAKE 599 311",
            "28030 CW 2026-05-25 1500 EA4TEST 599 006 ZL4TEST 599 044",
        ],
    )

    # 5) Cabrillo CQ WW SSB (6) — RST + zona CQ
    write_cabrillo(
        OUT / "cqww_ssb.cbr",
        "CQ-WW-SSB",
        "EA4TEST",
        [
            "14250 PH 2026-05-24 0000 EA4TEST 59 14 K9TEST 59 05",
            "14250 PH 2026-05-24 0003 EA4TEST 59 14 LU1ZZZ 59 11",
            "21250 PH 2026-05-24 0030 EA4TEST 59 14 JA1TEST 59 25",
            "7150 PH 2026-05-24 0105 EA4TEST 59 14 VE3MOCK 59 04",
            "28450 PH 2026-05-24 0200 EA4TEST 59 14 ZL4TEST 59 32",
            "14250 PH 2026-05-24 0233 EA4TEST 59 14 PY2MOCK 59 11",
        ],
    )

    # 6) Cabrillo ARRL Sweepstakes CW (5) — call serial prec check section
    write_cabrillo(
        OUT / "arrl_ss_cw.log",
        "ARRL-SS-CW",
        "N5KOTEST",
        [
            "21042 CW 2026-11-07 2102 N5KOTEST 3 B 74 SCV K9TEST 2 A 74 IL",
            "21042 CW 2026-11-07 2108 N5KOTEST 4 B 74 SCV G3FAKE 8 U 99 DX",
            "14042 CW 2026-11-07 2200 N5KOTEST 5 B 74 SCV VE3MOCK 1 A 70 ONE",
            "7042 CW 2026-11-07 2300 N5KOTEST 6 B 74 SCV W1XYZ 9 Q 65 EMA",
            "14042 CW 2026-11-07 2330 N5KOTEST 7 B 74 SCV K0ABC 3 A 80 MN",
        ],
    )

    # 7) Cabrillo ARRL Field Day (4) — clase + sección
    write_cabrillo(
        OUT / "arrl_fd.log",
        "ARRL-FD",
        "W1AWTEST",
        [
            "14250 PH 2026-06-27 1801 W1AWTEST 2A CT K9TEST 1D IL",
            "7040 CW 2026-06-27 1830 W1AWTEST 2A CT G3FAKE 1B DX",
            "14040 CW 2026-06-27 1905 W1AWTEST 2A CT VE3MOCK 3A ONE",
            "21250 PH 2026-06-27 2000 W1AWTEST 2A CT N0CALL 2A CO",
        ],
    )

    # 8) CSV con cabeceras en español (8) — fuerza el mapeo manual e inferencias.
    write_delimited(
        OUT / "cuaderno_es.csv",
        ["Indicativo", "Fecha", "Hora_UTC", "Frecuencia", "Modo", "RST_Env", "RST_Rec"],
        [
            ["WW1AAA", "2026-05-28", "1210", "14.030", "CW", "599", "599"],
            ["EA7MOCK", "2026-05-28", "1530", "7.090", "PH", "59", "57"],
            ["K2FAKE", "2026-05-28", "1545", "21.300", "PH", "59", "59"],
            ["VK3TEST", "2026-05-28", "1600", "28.490", "PH", "59", "55"],
            ["UA9MOCK", "2026-05-28", "1622", "14.030", "RY", "599", "599"],
            ["HB9FAKE", "2026-05-28", "1640", "10.130", "CW", "559", "559"],
            ["PA3TEST", "2026-05-28", "1701", "3.560", "CW", "599", "589"],
            ["CE3MOCK", "2026-05-28", "1733", "14.250", "PH", "59", "58"],
        ],
        ",",
    )

    # 9) TSV con otras cabeceras (6)
    write_delimited(
        OUT / "portatil.tsv",
        ["Callsign", "Date", "Time", "Band", "Mode", "Comment"],
        [
            ["XE1TEST", "2026/05/23", "1400", "20m", "SSB", "POTA activation"],
            ["KP4MOCK", "2026/05/23", "1410", "40m", "CW", "rough copy"],
            ["TI2FAKE", "2026/05/23", "1425", "15m", "SSB", ""],
            ["YV5TEST", "2026/05/23", "1440", "10m", "FM", "repeater echo test"],
            ["CO2MOCK", "2026/05/23", "1455", "20m", "DSTAR", "digital voice"],
            ["HK3FAKE", "2026/05/23", "1510", "17m", "CW", ""],
        ],
        "\t",
    )

    # 10) JSON anidado con campos APP_ y lat/lon (6) — prueba Maidenhead.
    json_doc = {
        "source": "logger-ficticio-v4",
        "records": [
            {"call": "WW1AAA", "date": "2026-05-28", "time": "1205", "freq": "14.030", "mode": "CW", "rst_sent": "599", "rst_rcvd": "559", "station": {"lat": "40.4168", "lon": "-3.7038"}},
            {"call": "EA1MOCK", "date": "2026-05-22", "time": "1100", "freq": "14.200", "mode": "PH", "rst_sent": "59", "rst_rcvd": "59", "station": {"lat": "43.36", "lon": "-8.41"}},
            {"call": "DK7FAKE", "date": "2026-05-22", "time": "1112", "freq": "7.030", "mode": "CW", "rst_sent": "599", "rst_rcvd": "599", "app": {"PROGRAMNAME_NOTE": "test"}},
            {"call": "IK2TEST", "date": "2026-05-22", "time": "1130", "freq": "21.074", "mode": "FT8", "rst_sent": "-07", "rst_rcvd": "-09", "gridsquare": "JN45"},
            {"call": "SP1MOCK", "date": "2026-05-22", "time": "1148", "freq": "10.136", "mode": "FT8", "rst_sent": "-03", "rst_rcvd": "-01"},
            {"call": "OK1FAKE", "date": "2026-05-22", "time": "1205", "freq": "3.573", "mode": "FT8", "rst_sent": "-14", "rst_rcvd": "-16"},
        ],
    }
    (OUT / "export_custom.json").write_text(json.dumps(json_doc, indent=2, ensure_ascii=False), encoding="utf-8")

    # 11) POTA: dos contactos con el mismo corresponsal pero distinto parque (NO duplicado).
    write_delimited(
        OUT / "pota_activacion.csv",
        ["Call", "QSO_DATE", "TIME_ON", "FREQ", "MODE", "MY_POTA_REF", "POTA_REF"],
        [
            ["AA1POTA", "20260521", "1300", "14.060", "CW", "K-0001", ""],
            ["AA1POTA", "20260521", "1305", "14.060", "CW", "K-0002", ""],
            ["BB2PARK", "20260521", "1320", "7.032", "CW", "K-0001", "K-1111"],
            ["CC3HUNT", "20260521", "1340", "14.285", "SSB", "K-0001", ""],
        ],
        ",",
    )

    # 12) XLSX (6) — requiere openpyxl; fechas y celdas vacías.
    try:
        from openpyxl import Workbook

        wb = Workbook()
        ws = wb.active
        ws.title = "Log"
        ws.append(["Callsign", "Date", "Time", "Frequency", "Mode", "Name", "Exchange"])
        xlsx_rows = [
            ["RA3TEST", "2026-05-20", "0800", "14.180", "PH", "Igor", "MA"],
            ["BG2MOCK", "2026-05-20", "0815", "21.300", "PH", "", "CA"],
            ["VU2FAKE", "2026-05-20", "0830", "28.500", "PH", "Raj", ""],
            ["ZS6TEST", "2026-05-20", "0845", "7.060", "PH", "Pieter", "TX"],
            ["LU8MOCK", "2026-05-20", "0901", "14.030", "CW", "", "QC"],
            ["4X4FAKE", "2026-05-20", "0920", "10.120", "CW", "Avi", ""],
        ]
        for row in xlsx_rows:
            ws.append(row)
        wb.save(OUT / "planilla_excel.xlsx")
        xlsx_ok = True
    except Exception as exc:  # noqa: BLE001
        xlsx_ok = False
        print(f"XLSX omitido ({exc})")

    files = sorted(p.name for p in OUT.glob("*") if p.name != "README.md")
    print(f"Generados {len(files)} archivos en {OUT}:")
    for name in files:
        print(f"  - {name}")
    if not xlsx_ok:
        print("  (instala openpyxl para regenerar el .xlsx)")


if __name__ == "__main__":
    main()
