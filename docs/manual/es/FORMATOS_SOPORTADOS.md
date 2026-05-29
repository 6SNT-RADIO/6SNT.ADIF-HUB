# Formatos soportados

## ADI

Soporte basico para ADIF texto. Puede manejar campos comunes y extensiones `APP_*`.

## ADX

Soporte XML simple. La validacion XSD completa queda pendiente.

## Cabrillo

Soporta cabecera `CONTEST:` y varias plantillas frecuentes. Concursos con columnas especiales pueden requerir nuevas plantillas.

## CSV y TSV

Soporte con deteccion de columnas y mapper. Los delimitadores o comillas inconsistentes pueden requerir limpieza previa.

## XLSX

Soporte mediante lectura local de hojas de calculo. Hojas vacias, fechas serializadas raras o multiples tablas por hoja pueden necesitar preparacion manual.

## JSON

Soporta arreglo de objetos u objeto raiz compatible. La raiz invalida se reporta como error.

## Limitaciones conocidas

- No todos los campos ADIF estan cubiertos en UI.
- La deduplicacion es conservadora, no infalible.
- La beta no debe usarse para modificar tu unico log maestro sin backup.

