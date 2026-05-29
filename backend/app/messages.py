from __future__ import annotations

Locale = str

MESSAGES: dict[str, dict[Locale, str]] = {
    "no_files_uploaded": {
        "es": "No se subieron archivos",
        "en": "No files were uploaded",
    },
    "batch_not_found": {
        "es": "Lote no encontrado",
        "en": "Batch not found",
    },
    "conflict_not_found": {
        "es": "Conflicto no encontrado",
        "en": "Conflict not found",
    },
}


def message(key: str, locale: Locale = "es") -> str:
    values = MESSAGES.get(key, {})
    return values.get(locale, values.get("es", key))

