# CODEX.md - 6SNT.ADIF-HUB

## Objetivo

Construir un cockpit local para consolidar logs de radioaficion en multiples formatos, normalizarlos hacia ADIF 3.1.7, detectar duplicados y exportar un ADI limpio.

## Stack

- Frontend: React + TypeScript + Vite + Tailwind local.
- Backend: FastAPI + SQLite local.
- Tests: pytest para backend; build Vite para frontend.

## Comandos

```powershell
cd backend
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pytest
uvicorn app.main:app --reload
```

```powershell
cd frontend
npm install
npm run build
npm run dev
```

## Notas Operativas

- `index.html` raiz es referencia visual heredada, no el runtime final.
- El runtime frontend usa `frontend/index.html`.
- El backend escribe SQLite y exports bajo `data/`, ignorado por Git.
- La API espera archivos locales y no sube datos a servicios externos.

