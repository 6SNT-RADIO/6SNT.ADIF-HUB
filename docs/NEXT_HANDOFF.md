# NEXT_HANDOFF

## Estado

El primer hito funcional esta implementado como app local. La UI conserva la maqueta del `index.html` inicial y la convierte en componentes React. El backend procesa archivos y guarda resultados en SQLite local.

El refactor 2026-05-29 dejo la UI alineada 1:1 con `index.html` (Material Symbols,
tokens de `DESIGN.md`, toggles de inferencia del asset) y el pipeline funcional
end-to-end (dedupe contextual + Maidenhead + exchange Cabrillo). Ver `STATUS.md`.

## Proximo Paso

1. Mas plantillas de concurso y deteccion fina por modo (CW/SSB/RTTY) donde el exchange cambie.
2. Enriquecer STATE_FROM_EXCHANGE / secciones con DXCC/CQZ/ITUZ derivados.
3. Endurecer parsers ADIF/Cabrillo con mas casos reales saneados; validacion XSD para ADX.
4. Dar funcion real a nav/busqueda/secciones del cromo (hoy decorativas).
5. Persistir preferencia de estrategia de fusion por defecto y resolucion masiva (resolver todos con una estrategia).

## Hecho en V2

- Resolucion interactiva de conflictos: estrategias (Use Existing/Replace/Merge/Use Newer) + eleccion por campo. Ver `STATUS.md`.
- Plantillas de concurso Cabrillo por `CONTEST_ID` (CQ WW/WPX, ARRL DX/FD/SS, IARU, NAQP) con respaldo generico.

## Riesgos

- Cabrillo usa parser generico posicional; concursos con columnas especiales necesitaran plantillas.
- ADX soporta XML simple; validacion XSD queda fuera del hito actual.
- XLSX depende de `openpyxl`.
- `STATE_FROM_EXCHANGE` solo reconoce abreviaturas US/CA conocidas; no infiere DXCC/zonas todavia.

