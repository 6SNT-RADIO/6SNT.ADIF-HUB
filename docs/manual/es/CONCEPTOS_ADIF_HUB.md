# Conceptos ADIF-HUB

## No es un logger

La app no esta pensada para operar en vivo ni reemplazar tu logger principal. Su papel es actuar como hub local de limpieza, consolidacion y exportacion.

## ADI y ADX

- `ADI`: formato ADIF en texto plano con campos como `<CALL:5>EA1AA`.
- `ADX`: variante XML de ADIF, mas estructurada pero mas exigente con la forma del documento.

## Cabrillo

`Cabrillo` se usa en concursos. Es excelente para enviar resultados, pero su intercambio cambia segun el concurso. Por eso el parser usa plantillas y puede necesitar ajustes para eventos no cubiertos.

## CSV, TSV, XLSX y JSON

Estos formatos suelen venir de planillas, exports personalizados o herramientas propias. Requieren mapper porque los nombres de columnas no siempre siguen ADIF.

## Deduplicacion semantica

Dos registros pueden ser el mismo QSO aunque no sean identicos byte a byte. La app compara campos clave y tolerancias de tiempo para encontrar duplicados probables.

## ADIF 3.1.7

La normalizacion apunta a campos y convenciones compatibles con ADIF 3.1.7. No se promete cobertura completa de todos los campos o extensiones en beta.

