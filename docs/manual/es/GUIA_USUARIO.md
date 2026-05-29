# Guia de usuario

## Que hace la app

6SNT.ADIF-HUB toma logs dispersos, los transforma a una representacion comun, permite revisar el mapeo, detecta duplicados semanticos y exporta un `ADI` consolidado. La base de trabajo es local y usa SQLite.

## Navegacion

- `INGESTA`: carga archivos y muestra la cola.
- `PROCESO`: mapea columnas y normaliza registros hacia campos ADIF.
- `FUSION`: detecta duplicados y resuelve conflictos.
- `EXPORTAR`: genera el ADIF final.

## Ingesta

Arrastra uno o mas archivos a la zona de carga. La app intenta detectar formato, cantidad de registros, columnas y mapeo inicial. Si aparecen warnings, revisalos antes de avanzar.

## Mapper

El mapper conecta columnas de entrada con campos ADIF como `CALL`, `QSO_DATE`, `TIME_ON`, `BAND`, `FREQ` y `MODE`. Si el automapeo queda incompleto, selecciona manualmente el campo correcto.

## Normalizacion

Al procesar el mapeo, la app aplica reglas de limpieza: formatos de fecha/hora, modos conocidos, bandas derivadas de frecuencia si esta activo, datos Maidenhead y campos de concurso cuando el parser los reconoce.

## Preview

La tabla de preview permite inspeccionar hasta 100 filas normalizadas. Usa la busqueda superior para filtrar por indicativo, fecha, hora, banda, frecuencia, modo o estado.

## Deduplicacion

La deduplicacion compara QSOs por criterios contextuales. Para contactos generales usa indicativo, banda, modo y ventana temporal. Para concursos prioriza `CONTEST_ID`. Para POTA/SOTA puede considerar referencias de actividad cuando existan.

## Conflictos

Un conflicto aparece cuando dos registros parecen representar el mismo QSO pero contienen diferencias relevantes. Puedes resolver con una estrategia global o elegir por campo.

## Exportacion

Cuando hay QSOs normalizados, la vista `EXPORTAR` permite descargar un archivo `ADI`. Los conflictos abiertos no deben mezclarse sin revision.

