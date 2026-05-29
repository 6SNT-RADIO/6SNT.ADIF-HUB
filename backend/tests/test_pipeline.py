from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook

from app import pipeline


FIXTURES = Path(__file__).parent / "fixtures"


def read_fixture(name: str) -> bytes:
    return (FIXTURES / name).read_bytes()


def test_parsers_cover_supported_formats(tmp_path: Path) -> None:
    xlsx_path = tmp_path / "sample.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["Callsign", "Frequency", "Date", "Time", "Mode"])
    sheet.append(["LU1XYZ", "50.313", "2026-05-28", "1230", "FT8"])
    workbook.save(xlsx_path)

    samples = {
        "sample.adi": read_fixture("sample_adi.txt"),
        "sample.adx": read_fixture("sample.adx"),
        "sample.cbr": read_fixture("sample.cbr"),
        "sample.csv": read_fixture("sample.csv"),
        "sample.tsv": read_fixture("sample.tsv"),
        "sample.json": read_fixture("sample.json"),
        "sample.xlsx": xlsx_path.read_bytes(),
    }

    for filename, content in samples.items():
        parsed = pipeline.parse_file(filename, content)
        assert parsed.records, filename  # nosec B101 - pytest assertion
        assert parsed.columns, filename  # nosec B101 - pytest assertion


def test_normalization_infers_band_and_mode() -> None:
    records = [
        {
            "Indicativo": "k1abc",
            "Frecuencia": "14.260",
            "Fecha": "2026-05-28",
            "Hora_UTC": "1200",
            "Modo": "PH",
        }
    ]
    normalized = pipeline.normalize_records(
        records,
        {
            "Indicativo": "CALL",
            "Frecuencia": "FREQ",
            "Fecha": "QSO_DATE",
            "Hora_UTC": "TIME_ON",
            "Modo": "MODE",
        },
        {
            "infer_band_from_freq": True,
            "normalize_mode_submode": True,
            "normalize_dates": True,
        },
    )

    assert normalized[0]["CALL"] == "K1ABC"  # nosec B101 - pytest assertion
    assert normalized[0]["BAND"] == "20m"  # nosec B101 - pytest assertion
    assert normalized[0]["MODE"] == "SSB"  # nosec B101 - pytest assertion
    assert normalized[0]["QSO_DATE"] == "20260528"  # nosec B101 - pytest assertion
    assert normalized[0]["TIME_ON"] == "120000"  # nosec B101 - pytest assertion


def test_dedupe_detects_temporal_duplicate_and_pota_exception(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(pipeline, "DB_PATH", tmp_path / "adifhub.sqlite3")
    pipeline.init_db()
    batch = pipeline.create_batch([("sample.csv", read_fixture("sample.csv"))])
    mapping = {
        "Indicativo": "CALL",
        "Frecuencia": "FREQ",
        "Fecha": "QSO_DATE",
        "Hora_UTC": "TIME_ON",
        "Modo": "MODE",
    }
    pipeline.normalize_batch(
        batch["id"],
        mapping,
        {
            "infer_band_from_freq": True,
            "normalize_mode_submode": True,
            "normalize_dates": True,
        },
    )
    result = pipeline.dedupe_batch(batch["id"], tolerance_minutes=15)
    assert result["duplicate_records"] == 0  # nosec B101 - pytest assertion

    duplicate_batch = pipeline.create_batch(
        [
            (
                "dups.csv",
                b"Call,Freq,Date,Time,Mode\nK1ABC,14.260,2026-05-28,1200,PH\nK1ABC,14.260,2026-05-28,1205,PH\n",
            )
        ]
    )
    pipeline.normalize_batch(
        duplicate_batch["id"],
        {
            "Call": "CALL",
            "Freq": "FREQ",
            "Date": "QSO_DATE",
            "Time": "TIME_ON",
            "Mode": "MODE",
        },
        {
            "infer_band_from_freq": True,
            "normalize_mode_submode": True,
            "normalize_dates": True,
        },
    )
    result = pipeline.dedupe_batch(duplicate_batch["id"], tolerance_minutes=15)
    assert result["duplicate_records"] == 1  # nosec B101 - pytest assertion

    pota_batch = pipeline.create_batch(
        [
            (
                "dups.csv",
                b"Call,Freq,Date,Time,Mode,MY_POTA_REF\nK1ABC,14.260,2026-05-28,1200,PH,K-0001\nK1ABC,14.260,2026-05-28,1205,PH,K-0002\n",
            )
        ]
    )
    pipeline.normalize_batch(
        pota_batch["id"],
        {
            "Call": "CALL",
            "Freq": "FREQ",
            "Date": "QSO_DATE",
            "Time": "TIME_ON",
            "Mode": "MODE",
            "MY_POTA_REF": "MY_POTA_REF",
        },
        {
            "infer_band_from_freq": True,
            "normalize_mode_submode": True,
            "normalize_dates": True,
        },
    )
    result = pipeline.dedupe_batch(pota_batch["id"], tolerance_minutes=15)
    assert result["duplicate_records"] == 0  # nosec B101 - pytest assertion


def test_maidenhead_inference_from_latlon() -> None:
    records = [{"Call": "EA4XYZ", "Latitude": "40.4168", "Longitude": "-3.7038"}]
    normalized = pipeline.normalize_records(
        records,
        {"Call": "CALL", "Latitude": "LAT", "Longitude": "LON"},
        {"maidenhead_geoconversion": True},
    )
    # Madrid (40.42N, 3.70W) lives in grid square IN80.
    assert normalized[0]["GRIDSQUARE"].startswith("IN80")  # nosec B101
    assert len(normalized[0]["GRIDSQUARE"]) == 6  # nosec B101


def test_maidenhead_disabled_when_flag_off() -> None:
    records = [{"Call": "EA4XYZ", "Latitude": "40.4168", "Longitude": "-3.7038"}]
    normalized = pipeline.normalize_records(
        records,
        {"Call": "CALL", "Latitude": "LAT", "Longitude": "LON"},
        {"maidenhead_geoconversion": False},
    )
    assert "GRIDSQUARE" not in normalized[0]  # nosec B101


def test_state_from_exchange_maps_us_state() -> None:
    records = [{"Call": "K1ABC", "Exchange": "MA"}]
    normalized = pipeline.normalize_records(
        records,
        {"Call": "CALL", "Exchange": "SRX_STRING"},
        {"state_from_exchange": True},
    )
    assert normalized[0]["STATE"] == "MA"  # nosec B101


def test_contest_dedupe_ignores_clock_skew(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(pipeline, "DB_PATH", tmp_path / "adifhub.sqlite3")
    pipeline.init_db()
    batch = pipeline.create_batch(
        [
            (
                "contest.csv",
                b"Call,Freq,Date,Time,Mode,Contest\n"
                b"K1ABC,14.030,2026-05-28,1200,CW,CQ-WW\n"
                b"K1ABC,14.030,2026-05-28,1400,CW,CQ-WW\n",
            )
        ]
    )
    pipeline.normalize_batch(
        batch["id"],
        {
            "Call": "CALL",
            "Freq": "FREQ",
            "Date": "QSO_DATE",
            "Time": "TIME_ON",
            "Mode": "MODE",
            "Contest": "CONTEST_ID",
        },
        {"infer_band_from_freq": True},
    )
    # 2h apart but same contest/call/band/mode -> duplicate (contest rules prevail).
    result = pipeline.dedupe_batch(batch["id"], tolerance_minutes=15)
    assert result["duplicate_records"] == 1  # nosec B101


def test_cabrillo_template_cq_ww_zone() -> None:
    content = (
        b"CONTEST: CQ-WW-CW\n"
        b"QSO: 14000 CW 2026-05-28 0000 K1ABC 599 05 G3ZZZ 599 14\n"
    )
    parsed = pipeline.parse_file("ww.cbr", content)
    rec = parsed.records[0]
    assert rec["CALL"] == "G3ZZZ"  # nosec B101 - worked station
    assert rec["RST_RCVD"] == "599"  # nosec B101
    assert rec["CQZ"] == "14"  # nosec B101 - their CQ zone
    assert rec["STATION_CALLSIGN"] == "K1ABC"  # nosec B101 - own call


def test_cabrillo_template_sweepstakes_exchange() -> None:
    content = (
        b"CONTEST: ARRL-SS-CW\n"
        b"QSO: 21042 CW 1997-11-01 2102 N5KO 3 B 74 SCV N6TR 2 A 74 OR\n"
    )
    parsed = pipeline.parse_file("ss.cbr", content)
    rec = parsed.records[0]
    # Each side: call serial precedence check section.
    assert rec["STATION_CALLSIGN"] == "N5KO"  # nosec B101
    assert rec["STX"] == "3"  # nosec B101 - sent serial
    assert rec["CALL"] == "N6TR"  # nosec B101 - worked station
    assert rec["SRX"] == "2"  # nosec B101 - received serial
    assert rec["ARRL_SECT"] == "OR"  # nosec B101 - received section


def test_merge_field_rules() -> None:
    assert pipeline._merge_field("NAME", "Ana", "") == "Ana"  # nosec B101 - enrich empty
    assert pipeline._merge_field("LOTW_QSL_RCVD", "N", "Y") == "Y"  # nosec B101 - promote
    assert pipeline._merge_field("COMMENT", "POTA", "Field Day") == "Field Day | POTA"  # nosec B101 - concat
    assert pipeline._merge_field("RST_SENT", "559", "599") == "599"  # nosec B101 - keep


def test_interactive_conflict_resolution(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(pipeline, "DB_PATH", tmp_path / "adifhub.sqlite3")
    pipeline.init_db()
    batch = pipeline.create_batch(
        [
            (
                "rst.csv",
                b"Call,Freq,Date,Time,Mode,RST\n"
                b"K1ABC,14.030,2026-05-28,1200,CW,599\n"
                b"K1ABC,14.030,2026-05-28,1203,CW,559\n",
            )
        ]
    )
    pipeline.normalize_batch(
        batch["id"],
        {
            "Call": "CALL",
            "Freq": "FREQ",
            "Date": "QSO_DATE",
            "Time": "TIME_ON",
            "Mode": "MODE",
            "RST": "RST_SENT",
        },
        {"infer_band_from_freq": True},
    )
    deduped = pipeline.dedupe_batch(batch["id"], tolerance_minutes=15)
    assert deduped["conflict_records"] == 1  # nosec B101 - RST mismatch is a conflict
    conflict = deduped["conflicts"][0]
    assert conflict["status"] == "open"  # nosec B101
    assert conflict["summary"]["call"] == "K1ABC"  # nosec B101

    resolved = pipeline.resolve_conflict(
        batch["id"],
        conflict["id"],
        strategy="manual",
        field_choices={"RST_SENT": "incoming"},
    )
    assert resolved["conflict_records"] == 0  # nosec B101 - conflict cleared
    assert resolved["conflicts"][0]["status"] == "resolved"  # nosec B101
    survivors = [q for q in resolved["qsos"] if q["status"] == "unique"]
    assert len(survivors) == 1  # nosec B101 - only the consolidated QSO survives
    assert survivors[0]["record"]["RST_SENT"] == "559"  # nosec B101 - incoming chosen
