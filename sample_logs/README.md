# sample_logs — set de prueba (datos FICTICIOS)

Logs inventados para probar 6SNT.ADIF-HUB. Todos los indicativos y datos son falsos
(estilo `N0CALL` / sufijos `...TEST`/`...MOCK`/`...FAKE`). Regenerables con:

```powershell
python scripts\make_sample_logs.py
```

## Archivos y qué ejercitan

| Archivo | Formato | Regs | Prueba |
| :-- | :-- | :-- | :-- |
| `adif_standard.adi` | ADI (etiquetas) | 10 | ADIF clásico; modos `PH`/`RY`/`C4FM` → normalización a SSB/RTTY/DIGITALVOICE |
| `wsjtx_export.adif` | ADI (WSJT-X) | 8 | Digitales FT8/FT4, `GRIDSQUARE`, flags `LOTW_QSL_RCVD`/`EQSL_QSL_RCVD` |
| `adx_log.adx` | ADX (XML) | 6 | Parser XML |
| `cqwpx_cw.cbr` | Cabrillo | 6 | Plantilla CQ WPX → RST + serial (`STX`/`SRX`) |
| `cqww_ssb.cbr` | Cabrillo | 6 | Plantilla CQ WW → RST + zona CQ (`CQZ`) |
| `arrl_ss_cw.log` | Cabrillo | 5 | Plantilla Sweepstakes → serial/precedencia/check/`ARRL_SECT` |
| `arrl_fd.log` | Cabrillo | 4 | Plantilla Field Day → clase + `ARRL_SECT` |
| `cuaderno_es.csv` | CSV | 8 | Cabeceras en español → mapeo asistido/manual |
| `portatil.tsv` | TSV | 6 | Tabulado, cabeceras distintas, fecha `YYYY/MM/DD` |
| `export_custom.json` | JSON | 6 | Anidado (`station.lat/lon`), campos `app.*`, lat/lon → Maidenhead |
| `pota_activacion.csv` | CSV | 4 | POTA: mismo indicativo, distinto `MY_POTA_REF` → NO duplicado |
| `planilla_excel.xlsx` | XLSX | 6 | Excel, celdas vacías, `Exchange` (estado) → `STATE` |

Total: ~75 registros.

## Casos sembrados a propósito

- **Duplicados:** `WW1AAA` aparece en `adif_standard.adi`, `export_custom.json` y `cuaderno_es.csv`
  (20m CW, ~12:00–12:10 UTC) → el dedupe marca 2 duplicados.
- **Conflicto:** entre esas copias el `RST_RCVD` difiere (599 vs 559) → se abre 1 conflicto
  para probar la resolución interactiva (por campo o por estrategia).
- **Excepción POTA:** `AA1POTA` dos veces misma banda/modo/día pero distinto parque → NO duplicado.
- **Inferencias:** banda desde frecuencia, Maidenhead desde lat/lon (JSON), `STATE` desde
  intercambio (XLSX `Exchange`).

## Cómo probar

1. Abre la app (`6SNT.ADIF-HUB.exe` o `npm run dev`).
2. Arrastra **todos** los archivos de esta carpeta a la zona de carga (o varios a la vez).
3. Revisa/ajusta el mapeo de columnas (sobre todo el CSV/TSV/XLSX) y pulsa `PROCESAR_MAPEO`.
4. Pulsa `EJECUTAR_DEDUPE` y resuelve el conflicto de `WW1AAA`.
5. Descarga el ADI consolidado.
