# Resolucion de conflictos

## Estrategias

- `USAR_EXISTENTE`: conserva el registro que ya esta en la base local.
- `USAR_ENTRANTE`: reemplaza el contenido con el registro importado.
- `FUSIONAR`: rellena vacios, promueve confirmaciones utiles y combina comentarios cuando aplica.
- `MAS_RECIENTE`: usa el registro que parezca mas nuevo segun metadatos disponibles.
- Seleccion por campo: el operador elige valor entrante o existente para cada campo mostrado.

## Cuando usar cada una

Usa existente cuando confias mas en tu log maestro. Usa entrante cuando el archivo importado viene de una fuente mas cuidada. Usa fusionar cuando ambos registros aportan informacion. Usa mas reciente solo si las fechas de origen son confiables. Usa seleccion por campo para diferencias delicadas como `RST_SENT`, `RST_RCVD`, `COMMENT`, referencias POTA/SOTA o datos de concurso.

## Regla practica

Si el QSO sera subido a una plataforma externa, resuelve manualmente cualquier conflicto que afecte identidad del contacto: `CALL`, `QSO_DATE`, `TIME_ON`, `BAND`, `FREQ`, `MODE` o `CONTEST_ID`.

