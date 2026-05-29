# Guia rapida

6SNT.ADIF-HUB es una app local para limpiar, normalizar, deduplicar y exportar logs hacia ADIF. No es un logger diario y no reemplaza LoTW, eQSL, ClubLog, QRZ, Log4OM, N1MM ni otros sistemas de registro.

## Antes de empezar

- Trabaja siempre con copias de tus logs originales.
- No importes archivos con datos sensibles si vas a compartir capturas.
- Conserva el archivo original sin modificar fuera de la carpeta del proyecto.

## Flujo rapido

1. Abre la app.
2. En `INGESTA`, arrastra archivos `ADI`, `ADX`, `CBR`, `CSV`, `TSV`, `XLSX` o `JSON`.
3. Revisa la cola de ingesta y los avisos por archivo.
4. En `PROCESO`, ajusta el mapper si alguna columna no fue detectada.
5. Ejecuta `PROCESAR_MAPEO`.
6. En `FUSION`, ejecuta `DEDUPLICAR`.
7. Revisa conflictos abiertos y elige estrategia: usar existente, usar entrante, fusionar, mas reciente o seleccion por campo.
8. En `EXPORTAR`, descarga el archivo `ADI` consolidado.
9. Revisa el resultado antes de subirlo a plataformas externas.

## Resultado esperado

Obtendras un archivo ADIF limpio para revisar y usar como entrada en otros sistemas. La beta puede tener limitaciones con concursos o formatos poco comunes, por lo que la revision manual sigue siendo obligatoria.

