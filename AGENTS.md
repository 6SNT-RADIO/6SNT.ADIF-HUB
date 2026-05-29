# AGENTS.md - 6SNT.ADIF-HUB

Estas reglas complementan las reglas globales de Luis para esta carpeta.

- Proyecto local-first para ingesta, normalizacion, deduplicacion y export ADIF.
- No versionar ADIF reales, bases SQLite reales, logs completos, exports privados ni capturas sensibles.
- Usar solo fixtures pequenos y saneados bajo `backend/tests/fixtures`.
- Mantener `index.html` raiz como maqueta visual de referencia; la app implementada vive en `frontend/`.
- Backend local en FastAPI/SQLite bajo `backend/`; frontend en React/Vite/Tailwind bajo `frontend/`.
- No agregar servicios cloud, login, pagos ni sincronizacion externa sin autorizacion explicita.
- Este proyecto no controla radio ni transmite; si se agrega CAT/PTT/TX en el futuro, aplicar reglas radio 6SNT antes de habilitarlo.

