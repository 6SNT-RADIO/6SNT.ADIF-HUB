# Plan de validacion beta

## Objetivo

Validar si 6SNT.ADIF-HUB ayuda a operadores reales a limpiar, deduplicar y exportar logs sin perder control sobre sus datos.

## Alcance

Beta cerrada de 10 a 20 operadores durante 2 a 4 semanas. No se contacta a usuarios desde este documento y no se publica en comunidades hasta tener artefactos listos.

## Criterios de entrada

- App instalable o ejecutable local disponible.
- Documentacion minima ES/EN lista.
- Fixtures saneados para pruebas internas.
- Aviso claro de backup obligatorio.

## Criterios de exito

- Operadores completan importacion, mapeo, dedupe y export.
- Confianza declarada suficiente para revisar el ADI generado.
- Errores reproducibles quedan documentados con datos saneados.
- No aparecen riesgos de privacidad no controlados.

## Criterios de bloqueo

- Export ADIF corrupto.
- Perdida de registros sin aviso.
- Conflictos resueltos de forma ambigua.
- UI impide revisar datos antes de exportar.
- Manejo inseguro de logs reales o bases SQLite.

## Metricas

- Formatos probados.
- QSOs aproximados por lote.
- Tiempo hasta primera exportacion.
- Numero de conflictos y decisiones manuales.
- Nivel de confianza en escala 1-5.
- Errores por area.

