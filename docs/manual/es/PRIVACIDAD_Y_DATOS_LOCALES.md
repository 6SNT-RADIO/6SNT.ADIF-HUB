# Privacidad y datos locales

6SNT.ADIF-HUB es local-first. Los archivos se procesan en la maquina del operador y la base de trabajo usa SQLite local.

## No versionar

No subas a Git:

- ADIF reales.
- Bases SQLite reales.
- Logs completos.
- Exports privados.
- Capturas con indicativos, nombres, emails, ubicaciones o notas sensibles.
- Credenciales, cookies o tokens.

## Capturas

Antes de compartir una captura, revisa que no aparezcan indicativos reales, comentarios privados, rutas locales sensibles o datos de estacion.

## Backups

Mantener al menos:

- copia original sin tocar;
- copia de trabajo usada para importar;
- export `ADI` final;
- nota de version/fecha de la app.

