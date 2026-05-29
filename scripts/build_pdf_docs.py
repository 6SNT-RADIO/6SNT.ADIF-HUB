from __future__ import annotations

import html
import re
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PDF = DOCS / "pdf"
HTML = PDF / "html"
ASSETS = PDF / "assets"
AUTHOR = "Diseñado y desarrollado por Luis Soto, CA6SNT, Valdivia, Region de los Rios, Chile-FF30"


CHROME_CANDIDATES = [
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
]


def inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def table(lines: list[str]) -> str:
    rows = []
    for index, line in enumerate(lines):
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if index == 1 and all(set(cell) <= {"-", ":", " "} for cell in cells):
            continue
        tag = "th" if index == 0 else "td"
        rows.append("<tr>" + "".join(f"<{tag}>{inline(cell)}</{tag}>" for cell in cells) + "</tr>")
    return "<table>" + "".join(rows) + "</table>"


def markdown_to_html(markdown: str) -> str:
    output: list[str] = []
    paragraph: list[str] = []
    bullets: list[str] = []
    table_lines: list[str] = []
    code_lines: list[str] = []
    in_code = False

    def flush_paragraph() -> None:
        if paragraph:
            output.append(f"<p>{inline(' '.join(paragraph))}</p>")
            paragraph.clear()

    def flush_bullets() -> None:
        if bullets:
            output.append("<ul>" + "".join(f"<li>{inline(item)}</li>" for item in bullets) + "</ul>")
            bullets.clear()

    def flush_table() -> None:
        if table_lines:
            output.append(table(table_lines))
            table_lines.clear()

    for raw in markdown.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            if in_code:
                output.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines.clear()
                in_code = False
            else:
                flush_paragraph()
                flush_bullets()
                flush_table()
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if line.startswith("|") and line.endswith("|"):
            flush_paragraph()
            flush_bullets()
            table_lines.append(line)
            continue
        flush_table()
        if not line.strip():
            flush_paragraph()
            flush_bullets()
            continue
        if line.startswith("#"):
            flush_paragraph()
            flush_bullets()
            level = min(len(line) - len(line.lstrip("#")), 3)
            text = line[level:].strip()
            output.append(f"<h{level}>{inline(text)}</h{level}>")
        elif line.startswith("- "):
            flush_paragraph()
            bullets.append(line[2:].strip())
        elif re.match(r"^\d+\. ", line):
            flush_paragraph()
            bullets.append(re.sub(r"^\d+\. ", "", line).strip())
        else:
            paragraph.append(line.strip())

    flush_paragraph()
    flush_bullets()
    flush_table()
    return "\n".join(output)


def read_sections(paths: list[Path]) -> str:
    sections = []
    for path in paths:
        sections.append(f'<section class="doc-section" data-source="{path.as_posix()}">')
        sections.append(markdown_to_html(path.read_text(encoding="utf-8")))
        sections.append("</section>")
    return "\n".join(sections)


def render_html(title: str, subtitle: str, screenshot: str, paths: list[Path]) -> str:
    screenshot_src = "../assets/" + screenshot
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <style>
    @page {{ size: A4; margin: 16mm 14mm; }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: #f4f7f6;
      color: #17201d;
      font-family: Arial, Helvetica, sans-serif;
      font-size: 10.5pt;
      line-height: 1.45;
    }}
    .cover {{
      min-height: 220mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      page-break-after: always;
      background: #07100d;
      color: #e8fff3;
      padding: 14mm;
      border: 1px solid #1f5a45;
    }}
    .brand {{ color: #5cff96; font-size: 13pt; font-weight: 800; letter-spacing: .04em; }}
    h1 {{ font-size: 30pt; line-height: 1.05; margin: 18mm 0 4mm; color: #ffffff; }}
    .subtitle {{ color: #a9d8c2; font-size: 13pt; max-width: 150mm; }}
    .author {{ color: #6fffb1; font-size: 10.5pt; border-top: 1px solid #245640; padding-top: 5mm; }}
    .screenshot {{ margin-bottom: 8mm; }}
    .screenshot img {{ width: 100%; border: 1px solid #143828; box-shadow: 0 3mm 10mm rgba(0,0,0,.18); }}
    .caption {{ color: #455a50; font-size: 9pt; margin-top: 3mm; }}
    .doc-section {{ page-break-inside: auto; }}
    h1, h2, h3 {{ color: #0d3c2d; letter-spacing: .01em; break-after: avoid; }}
    h1 {{ font-size: 22pt; margin-top: 0; }}
    h2 {{ font-size: 15pt; margin-top: 8mm; border-bottom: 1px solid #c9d8d0; padding-bottom: 2mm; }}
    h3 {{ font-size: 12pt; margin-top: 5mm; }}
    p {{ margin: 2mm 0; }}
    ul {{ margin: 1.5mm 0 3mm 6mm; padding-left: 5mm; }}
    li {{ margin: .8mm 0; }}
    code {{ background: #e2ece7; padding: .4mm 1mm; border-radius: 1mm; }}
    pre {{ background: #0b1411; color: #e8fff3; padding: 4mm; white-space: pre-wrap; }}
    table {{ width: 100%; border-collapse: collapse; margin: 4mm 0; font-size: 9.4pt; }}
    th, td {{ border: 1px solid #bfd0c7; padding: 2mm; vertical-align: top; }}
    th {{ background: #dce9e3; color: #0d3c2d; }}
    .footer-note {{ margin-top: 12mm; color: #5b6f66; font-size: 9pt; }}
  </style>
</head>
<body>
  <section class="cover">
    <div>
      <div class="brand">6SNT.ADIF-HUB</div>
      <h1>{html.escape(title)}</h1>
      <div class="subtitle">{html.escape(subtitle)}</div>
    </div>
    <div class="author">{html.escape(AUTHOR)}</div>
  </section>
  <section class="screenshot">
    <h1>Captura de la aplicacion</h1>
    <img src="{screenshot_src}" alt="6SNT.ADIF-HUB screenshot">
    <div class="caption">Vista generada desde la app local con selector ES/EN visible.</div>
  </section>
  {read_sections(paths)}
  <section class="doc-section">
    <h1>Credito</h1>
    <p>{html.escape(AUTHOR)}</p>
  </section>
</body>
</html>"""


def chrome_path() -> Path:
    for candidate in CHROME_CANDIDATES:
        if candidate.exists():
            return candidate
    raise RuntimeError("No Chrome or Edge executable found for PDF generation")


def build_pdf(name: str, title: str, subtitle: str, screenshot: str, docs: list[str]) -> None:
    HTML.mkdir(parents=True, exist_ok=True)
    paths = [DOCS / path for path in docs]
    html_path = HTML / f"{name}.html"
    pdf_path = PDF / f"{name}.pdf"
    html_path.write_text(render_html(title, subtitle, screenshot, paths), encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="adifhub-pdf-") as profile:
        subprocess.run(
            [
                str(chrome_path()),
                "--headless=new",
                "--disable-gpu",
                "--no-pdf-header-footer",
                f"--user-data-dir={profile}",
                f"--print-to-pdf={pdf_path}",
                html_path.as_uri(),
            ],
            check=True,
            cwd=ROOT,
        )


def main() -> None:
    PDF.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    builds = [
        (
            "6SNT_ADIF_HUB_MANUAL_ES",
            "Manual de usuario",
            "Guia operativa para ingesta, mapeo, deduplicacion, conflictos y export ADIF.",
            "adif-hub-es.png",
            [
                "manual/es/GUIA_RAPIDA.md",
                "manual/es/GUIA_USUARIO.md",
                "manual/es/CONCEPTOS_ADIF_HUB.md",
                "manual/es/FLUJO_DE_TRABAJO.md",
                "manual/es/RESOLUCION_DE_CONFLICTOS.md",
                "manual/es/FORMATOS_SOPORTADOS.md",
                "manual/es/PRIVACIDAD_Y_DATOS_LOCALES.md",
            ],
        ),
        (
            "6SNT_ADIF_HUB_USER_MANUAL_EN",
            "User manual",
            "Operational guide for ingest, mapping, deduplication, conflicts and ADIF export.",
            "adif-hub-en.png",
            [
                "manual/en/QUICK_START.md",
                "manual/en/USER_GUIDE.md",
                "manual/en/ADIF_HUB_CONCEPTS.md",
                "manual/en/WORKFLOW.md",
                "manual/en/CONFLICT_RESOLUTION.md",
                "manual/en/SUPPORTED_FORMATS.md",
                "manual/en/PRIVACY_AND_LOCAL_DATA.md",
            ],
        ),
        (
            "6SNT_ADIF_HUB_VALIDACION_BETA_ES",
            "Kit de validacion beta",
            "Plan, perfiles, entrevista, formulario y matriz para beta cerrada.",
            "adif-hub-es.png",
            [
                "validation/es/PLAN_VALIDACION_BETA.md",
                "validation/es/PERFIL_OPERADORES_OBJETIVO.md",
                "validation/es/GUION_ENTREVISTA.md",
                "validation/es/FORMULARIO_FEEDBACK.md",
                "validation/es/MATRIZ_FEEDBACK.md",
            ],
        ),
        (
            "6SNT_ADIF_HUB_BETA_VALIDATION_EN",
            "Beta validation kit",
            "Plan, profiles, interview script, feedback form and matrix for closed beta.",
            "adif-hub-en.png",
            [
                "validation/en/BETA_VALIDATION_PLAN.md",
                "validation/en/TARGET_OPERATOR_PROFILES.md",
                "validation/en/INTERVIEW_SCRIPT.md",
                "validation/en/FEEDBACK_FORM.md",
                "validation/en/FEEDBACK_MATRIX.md",
            ],
        ),
        (
            "6SNT_ADIF_HUB_NARRATIVA_DISTRIBUCION_ES",
            "Narrativa y distribucion",
            "Posicionamiento interno, mensajes, FAQ, estrategia de comunidades y checklist.",
            "adif-hub-es.png",
            [
                "marketing/NARRATIVA_PRODUCTO_ES.md",
                "marketing/POSICIONAMIENTO.md",
                "marketing/MENSAJES_CLAVE.md",
                "marketing/NO_DECIR.md",
                "marketing/FAQ_PRELANZAMIENTO_ES.md",
                "distribution/ESTRATEGIA_COMUNIDADES_ES.md",
                "distribution/MATRIZ_CANALES.md",
                "distribution/CALENDARIO_60_DIAS_ES.md",
                "distribution/PLANTILLAS_POSTS_ES.md",
                "distribution/REGLAS_DE_PUBLICACION.md",
                "distribution/CHECKLIST_PRE_PUBLICACION.md",
            ],
        ),
        (
            "6SNT_ADIF_HUB_NARRATIVE_DISTRIBUTION_EN",
            "Narrative and distribution",
            "Internal narrative, FAQ, community strategy, content calendar and post templates.",
            "adif-hub-en.png",
            [
                "marketing/PRODUCT_NARRATIVE_EN.md",
                "marketing/PRELAUNCH_FAQ_EN.md",
                "distribution/COMMUNITY_DISTRIBUTION_STRATEGY_EN.md",
                "distribution/MATRIZ_CANALES.md",
                "distribution/60_DAY_CONTENT_CALENDAR_EN.md",
                "distribution/POST_TEMPLATES_EN.md",
                "distribution/REGLAS_DE_PUBLICACION.md",
                "distribution/CHECKLIST_PRE_PUBLICACION.md",
            ],
        ),
    ]
    for build in builds:
        build_pdf(*build)


if __name__ == "__main__":
    main()
