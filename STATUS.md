# STATUS

## 2026-06-13 (landing GitHub Pages alineada a Micro Apps)

- Reemplazadas `docs/index.html` y `docs/es/index.html` por una ficha de producto alineada con el formato actual de `6SNT.MicroApps`: hero de app, captura, chips de versión/plataforma, matriz SHA256, workflow, límites de seguridad y aviso de distribución AS IS.
- Agregado `docs/assets/page.css` como hoja visual compartida para la landing EN/ES y `docs/assets/6snt-icon.png` como favicon servido por GitHub Pages.
- El botón principal de descarga ahora apunta directamente al asset `6SNT.ADIF-HUB.exe` del release `v0.1.0-beta`, no solo a la página del release.
- Actualizados los botones de descarga en `docs/about.html` y `docs/es/about.html` para apuntar también al `.exe` directo.

## 2026-05-29 (preparacion publica GitHub + README landing)

- Preparado el repositorio local para primera publicacion publica sin commit, remoto ni push.
- Endurecido `.gitignore` para excluir datos locales, logs reales, bases SQLite, builds, `.venv`, `node_modules`, caches, auditorias temporales, HTML intermedio de PDFs, `screen.png` legado y `tsbuildinfo`.
- Creados `LICENSE` Apache-2.0, `SECURITY.md`, `CONTRIBUTING.md` y `CHANGELOG.md`.
- `README.md` convertido en landing tecnica publica: problema, publico objetivo, formatos, local-first, no logger, workflow, docs ES/EN, estado beta/MVP, screenshots saneados y guia para desarrolladores.
- Creada estructura publica `assets/` con screenshots saneados ES/EN e icono.
- Validacion: `pytest` 11/11 OK usando temp local `.tmp/pytest` por permisos del Temp de Windows; `ruff check app tests` OK; `npm run build` OK. Frontend no tiene script `lint`.
- Git local inicializado en rama `main`. `git add -n .` revisado sin `data/`, `.venv`, `node_modules`, builds, `.exe`, SQLite reales ni artefactos temporales.

## 2026-05-29 (PDFs documentales con capturas)

- Creada carpeta `docs/pdf/` con PDFs consolidados para manual ES/EN, kit de validacion beta ES/EN y narrativa/distribucion ES/EN.
- Capturas limpias generadas desde la app local en `docs/pdf/assets/`, con selector `ES/EN` visible.
- Portadas y cierre de los PDFs incluyen: "Diseñado y desarrollado por Luis Soto, CA6SNT, Valdivia, Region de los Rios, Chile-FF30".
- Creado generador reproducible `scripts/build_pdf_docs.py`, usando Chrome/Edge headless desde los `.md` existentes y HTML intermedio en `docs/pdf/html/`.
- Actualizado `docs/INDEX.md` con enlaces a los PDFs.
- PDFs regenerados en formato compacto, sin saltos de pagina forzados entre cada seccion.

## 2026-05-29 (pre-beta internacional: documentacion, validacion, narrativa y distribucion)

- **Fase 2 - Documentacion**: creada documentacion manual ES/EN bajo `docs/manual/` con guia rapida, guia de usuario, conceptos ADIF-HUB, flujo recomendado, resolucion de conflictos, formatos soportados y privacidad/datos locales.
- **Fase 3 - Validacion beta**: creado kit ES/EN bajo `docs/validation/` con plan de beta cerrada, perfiles de operadores, guion de entrevista, formulario de feedback y matriz de severidad/area.
- **Fase 4 - Narrativa**: creada documentacion interna bajo `docs/marketing/` con narrativa ES/EN, posicionamiento, mensajes clave, limites de comunicacion y FAQ pre-lanzamiento.
- **Fase 5 - Distribucion**: creada estrategia bajo `docs/distribution/` con comunidades objetivo, matriz de canales, calendario 60 dias, plantillas ES/EN, reglas de publicacion y checklist pre-publicacion. No se publico nada ni se contacto a usuarios.
- **Fase 6 - Trazabilidad**: creado `docs/INDEX.md` como indice documental interno con referencias cruzadas. `README.md` no fue modificado.
- **Validacion**: `npm run build` OK; `pytest` 11/11 OK con warnings de permisos en cache `.pytest_cache`; `ruff check app tests` OK. Escaneo simple de secretos en `docs`, `frontend/src` y `backend/app` sin hallazgos reales; unico match fue variable local `token` en `backend/app/pipeline.py`.
- **Git**: esta carpeta no contiene `.git`; `git status` no aplica desde `E:\6SNT.ADIFHUB`. No se hicieron commits ni push.

## 2026-05-29 (pre-beta internacional: i18n ES/EN)

- **Internacionalizacion UI**: agregada capa local ES/EN en `frontend/src/i18n/` con React Context, selector visible `ES/EN` en `TopNav`, cambio sin recarga y persistencia en `localStorage["6snt.adifhub.locale"]`. El idioma inicial usa preferencia guardada, navegador `en*` si aplica, y fallback a espanol.
- **Textos migrados**: navegacion, encabezados por vista, botones, estados vacios, busqueda, cola de ingesta, mapper, inferencias, revision de conflictos, exportacion, footer y estados visibles pasan por `t(...)`. Se mantienen tokens tecnicos y formatos estandar (`ADIF`, `ADI`, `ADX`, `Cabrillo`, `CSV`, `XLSX`, `JSON`, `QSO`, campos ADIF) sin traducir.
- **Backend**: mensajes HTTP visibles centralizados en `backend/app/messages.py` con catalogo ES/EN; la API sigue respondiendo en espanol hasta que exista negociacion de idioma.
- **Documentacion**: creado `docs/I18N.md` con estructura, uso, persistencia, tokens no traducidos y validacion manual recomendada.
- **Validacion**: `npm run build` OK; `pytest` 11/11 OK con warnings de permisos de cache `.pytest_cache`; `ruff check app tests` OK. La prueba visual del switch queda pendiente para operador.
- **Git**: esta carpeta no contiene `.git`; `git status`/`git diff --stat` no aplican desde `E:\6SNT.ADIFHUB`. No se hicieron commits ni push.

## 2026-05-29 (V2: navegación por vistas + backend en español)

- **UX/escalabilidad**: la nav lateral ahora **cambia de vista** (INGESTA / PROCESO / FUSION / EXPORTAR) en lugar de apilar todo en una página con scroll gigante. Cada vista está acotada y con scroll interno (cola de ingesta, vista previa hasta 100 filas con cabecera fija, conflictos hasta 50) — soporta cargas grandes (cientos de archivos) sin desbordar.
- El título/subtítulo del encabezado cambia según la vista activa. `NUEVA_IMPORTACION` usa un input propio (funciona desde cualquier vista) y lleva a INGESTA. Vistas sin datos muestran un aviso guía.
- **Backend en español**: mensajes HTTP (`No se subieron archivos`, `Lote no encontrado`, `Conflicto no encontrado`) y avisos del parser (Cabrillo corto, raíz JSON inválida).

## 2026-05-29 (V2: localización total a castellano neutro)

- Todos los nombres de sección/UI traducidos: `INGEST_QUEUE`→`COLA_DE_INGESTA`, `SEMANTIC_INFERENCE`→`INFERENCIA_SEMANTICA`, `COLUMN_MAPPER`→`MAPEO_DE_COLUMNAS`, `NORMALIZED_QSO_PREVIEW`→`VISTA_PREVIA_QSO`, `CONFLICT_REVIEW`→`REVISION_DE_CONFLICTOS`, `EXPORT_ADIF`→`EXPORTAR_ADIF`.
- Nav: INGESTA/PROCESO/FUSION/EXPORTAR (id interno EN preservado para anclas). Toggles: INFERIR_BANDA_POR_FRECUENCIA, GEOCONVERSION_MAIDENHEAD, ESTADO_DESDE_INTERCAMBIO. Botón dedupe→`DEDUPLICAR`.
- Cabeceras de la tabla de vista previa en español (INDICATIVO/FECHA/HORA/BANDA/FRECUENCIA/MODO); sub-etiquetas de formato (ADIF_EST/ADIF_XML/SEP_COMA/EXCEL/ESQUEMA).
- Se conservan en su forma estándar solo: nombres de **campo ADIF** (CALL, FREQ, MODE…), **códigos de formato** (ADI/ADX/CBR/CSV/XLSX/JSON), el término **QSO** y la marca. `.exe` reconstruido.

## 2026-05-29 (V2: limpieza de controles placeholder)

- Eliminados controles sin función (eran del asset): `DASHBOARD`, `REPORTS`, iconos `settings`/`terminal`, botón `AJUSTES` (sidebar) e `IGNORAR_NO_MAPEADAS` (mapper).
- **Búsqueda funcional**: el campo del TopNav (`FILTRAR_QSOS`) filtra en vivo la tabla `NORMALIZED_QSO_PREVIEW` por call/fecha/hora/banda/freq/modo/estado, con contador de coincidencias y mensaje de "sin coincidencias".
- **Nav lateral funcional**: `INGEST/PROCESS/MERGE/EXPORT` hacen scroll suave a su sección (anclas `sec-*`) y resaltan la activa.
- Eliminado el preset de estación falso (`STATION_ALPHA / 144.200 MHz / CW`): la app no tiene estación ni configuración de radio, solo carga y procesa. El encabezado del sidebar ahora es identidad honesta `PROCESADOR_ADIF · ADIF 3.1.7 · LOCAL` (icono `hub`) y el título principal pasó de `INGESTION_STATION_01` a `INGESTA_MULTIFORMATO` (sin instancias/presets numerados).

## 2026-05-29 (V2: plantillas de concurso Cabrillo)

- Parser Cabrillo ahora reconoce el concurso por la cabecera `CONTEST:` y mapea posicionalmente el intercambio enviado/recibido a campos ADIF.
- Plantillas: CQ WW (RST+CQZ), CQ WPX/sprints (RST+serial STX/SRX), ARRL DX (RST+texto), ARRL Field Day (clase+ARRL_SECT), ARRL Sweepstakes (call+serial+prec+check+sección), IARU (RST+ITU/HQ), NAQP/SST (nombre+ubicación→NAME/STATE). Coincidencia por prefijo de `CONTEST_ID` (prefijo más largo gana); respaldo genérico si no hay plantilla.
- Nuevos campos ADIF soportados: `CQZ`, `ITUZ`, `ARRL_SECT` (sobreviven a la normalización); extras del concurso van a campos `APP_CABRILLO_*` (precedencia, check, sección/zona propia), válidos en ADIF.
- Verificado: `pytest` 11/11 (incl. CQ WW y Sweepstakes), round-trip parse→normalize→export ADIF con `CALL/CQZ/STX/SRX/ARRL_SECT` correctos. `.exe` reconstruido.

## 2026-05-29 (V2: resolución interactiva de conflictos)

- **Backend** `resolve_conflict`: estrategias `use_existing` / `use_incoming` (replace) / `merge` (enriquecida: rellena vacíos, promueve QSL a confirmación más fuerte, concatena COMMENT) / `use_newer`, más **elección por campo** (`field_choices` entrante/existente). El registro existente sobrevive y conserva su `id`; el entrante pasa a `duplicate`; el conflicto a `resolved`.
- Export ADIF ahora excluye conflictos abiertos (`status NOT IN ('duplicate','conflict')`), evitando duplicar registros sin resolver.
- `get_batch` enriquece cada conflicto con `summary` (call/band/mode/fecha/hora) y recalcula `conflict_records` abiertos.
- Endpoint `POST /api/imports/{batch_id}/conflicts/{conflict_id}/resolve`.
- **Frontend** `ConflictReview` interactivo: resumen del QSO, selección por campo (ENTRANTE/EXISTENTE estilo merge de código), botones de estrategia (USAR_EXISTENTE/USAR_ENTRANTE/FUSIONAR/MAS_RECIENTE), `RESOLVER_SELECCION`, y estado `RESUELTO`.
- Verificado: `pytest` 9/9 (incl. unidades de `_merge_field` y resolución integral), round-trip HTTP upload→normalize→dedupe→resolve→export (export consolida a 1 registro), `.exe` reconstruido con la ruta de resolución.

## 2026-05-29 (inicio V2: español + app de escritorio)

- UI **localizada a español** (prosa, estados vacíos, botones, footer, tooltips); se mantienen campos ADIF, códigos de formato y tokens técnicos en inglés. Mapa de estados backend→español en `frontend/src/lib/labels.ts`.
- **Eliminados los datos sintéticos**: la app arranca en estado vacío real (sin lote demo, cola vacía, footer en 0, progreso real).
- **Icono de marca propio** (`scripts/make_icon.py` → `branding/6snt-icon.ico` + favicons): chasis obsidiana, marco esmeralda, ondas cian, monograma `6S`, LED ámbar. Embebido en el `.exe` y como favicon.
- **App de escritorio encapsulada**: `backend/desktop.py` sirve uvicorn en un hilo y abre una **ventana nativa pywebview/WebView2** (con respaldo al navegador). Verificado: proceso `6SNT.ADIF-HUB` con ventana titulada y WebView2 activo.
- `.exe` final: `dist_exe\6SNT.ADIF-HUB.exe` (~30 MB). `pytest` 7/7, `ruff` OK, `vite build` OK.

### Veredicto de madurez
Sigue siendo **MVP** evolucionando a producto. Pendiente para V2 final: resolución interactiva de conflictos, estrategias de fusión (Use Existing/Replace/Merge/Newer), plantillas de concurso Cabrillo, enriquecimiento DXCC/CQZ/ITUZ, y dar función real a la nav/búsqueda/secciones (hoy decorativas).

## 2026-05-29 (refactor visual + funcional)

- Frontend refactorizado para fidelidad 1:1 con el asset `index.html` y los tokens de `DESIGN.md`.
- Tokens de diseno completos en `tailwind.config.ts` (paleta, tipografia incl. `display-frequency`, glows esmeralda/cian/ambar).
- Iconografia migrada de `lucide-react` a **Material Symbols Outlined** (paquete local `material-symbols`, sin CDN) por mandato del brandbook.
- Panel `SEMANTIC_INFERENCE` alineado al asset: `INFER_BAND_FROM_FREQ`, `MAIDENHEAD_GEOCONVERSION`, `STATE_FROM_EXCHANGE`.
- Layout del grid principal corregido (filas automaticas) para evitar solapamiento mapper/inferencia.
- `NEW_LOG_IMPORT` abre el selector de archivos; navegacion lateral selecciona seccion.
- Backend: dedupe contextual (Contest estricto por `CONTEST_ID`, POTA mismo dia UTC con excepcion de parque, general/ClubLog +-15 min).
- Backend: inferencia Maidenhead (LAT/LON -> `GRIDSQUARE`) y `STATE`/`VE_PROV` desde intercambio; captura de exchange Cabrillo (STX/SRX) y `STATION_CALLSIGN`.
- Verificado: `pytest` 7/7, `ruff check`/`format` OK, `vite build` OK, round-trip HTTP upload->mapping->dedupe->export y screenshot a 1477x964 contra `screen.png`.

## Decision de branding

`6snt.adif_hub_brandbook_specs.md` y `DESIGN.md`/`index.html` difieren en hex exactos (p. ej. fondo `#05080c` vs `#101418`, primario esmeralda vs blanco+`primary-fixed`). Se adopta el **asset concreto `index.html` + `DESIGN.md` como fuente de verdad visual**; el brandbook queda como guia conceptual de alto nivel.

## 2026-05-29

- Se implemento scaffold local React/Vite/Tailwind y FastAPI/SQLite.
- `index.html` raiz queda como referencia visual.
- Backend incluye parsers basicos para ADI, ADX, Cabrillo, CSV/TSV, XLSX y JSON.
- Frontend incluye cockpit operativo con drop zone, cola, inferencias, mapper, preview, conflictos y export.
- Pendiente: iteracion visual con screenshot y expansion de reglas Cabrillo/ADIF completas.
