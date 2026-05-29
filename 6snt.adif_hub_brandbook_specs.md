# 6SNT.ADIF-HUB — Brandbook & Especificaciones Técnicas

## 1. Visión General
6SNT.ADIF-HUB es una herramienta de instrumentación técnica de alta precisión diseñada para la ingesta, normalización y deduplicación de registros de radioafición (QSOs). Su diseño sigue el estándar **Tactical Instrumentation / Hardware-Grade UI**, optimizado para entornos de baja luminosidad y máxima densidad de datos.

---

## 2. Paleta de Colores (Obsidian Tactical)

| Categoría | Token | Hex | Uso |
| :--- | :--- | :--- | :--- |
| **Fondo** | `background` | `#05080c` | Chasis principal. |
| **Superficie** | `surface-panel` | `#0a0e17` | Paneles y Wells recesados. |
| **Primario** | `primary` | `#10b981` | Estados OK, procesos completados (Esmeralda). |
| **Secundario** | `secondary` | `#20c7f3` | Información, VFO, datos activos (Cian). |
| **Terciario** | `tertiary` | `#ffae00` | Alertas, modos especiales, branding (Ámbar). |
| **Error** | `status-red` | `#ef4444` | Alertas críticas, conflictos detectados. |
| **Bordes** | `border-active` | `#162438` | Separación de módulos físicos. |

---

## 3. Tipografía (Strict Monospace)
El sistema utiliza una estrategia de **espaciado fijo** para garantizar la alineación vertical de telemetría y timestamps.

*   **Fuente Principal:** `JetBrains Mono` (Google Fonts).
*   **Fuente Auxiliar:** `Geist Mono` (para etiquetas de UI).
*   **Escala:**
    *   `Display:` 38px (VFO / Grandes Títulos).
    *   `UI Labels:` 10px (Uppercase, tracking 0.12em).
    *   `Data:` 12px - 14px.

---

## 4. Iconografía
Se utilizan **Material Symbols Outlined** (Google) con un grosor de trazo (stroke) de 1.75 para mantener la visibilidad sobre fondos negros.
*   `settings`: Configuración.
*   `terminal`: Consola de logs.
*   `cloud_upload`: Ingesta.
*   `layers`: Procesamiento.
*   `call_merge`: Deduplicación.

---

## 5. Especificaciones Técnicas (Stack)

*   **Frontend:** React 18 + Tailwind CSS.
*   **Layout:** Grid de hardware de 1px (gutters de fondo asomando entre paneles).
*   **Efectos:** Inset shadows para simular profundidad (wells), Neon Glows para estados activos (0px blur, 6-10px spread).
*   **Motor de Datos:** SQLite local para indexación rápida de archivos ADIF/Cabrillo masivos.

---

## 6. HTML Inicial (Estructura Base)
El contenedor principal utiliza un layout de `grid` con una barra lateral fija (`sidebar-w: 260px`) y un área de trabajo fluida, rematado por un `TopNavBar` de 48px con efecto `glassmorphism`.