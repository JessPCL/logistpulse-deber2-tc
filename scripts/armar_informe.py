"""Arma el INFORME final juntando los documentos de los tres integrantes, en orden.

  docs/generado/INFORME.md     (siempre)
  docs/generado/INFORME.docx   (si hay pandoc; en Colab: !pip install pypandoc_binary)

Para el PDF: abrir INFORME.docx en Word o Google Docs → Descargar / Exportar como PDF,
y guardarlo como docs/INFORME_Deber2_LOGISTPULSE.pdf (verificar_entrega.py lo busca).

Uso:  python scripts/armar_informe.py
"""

import re
import shutil
import subprocess

import _bootstrap  # noqa: F401
from _bootstrap import RAIZ

from logistpulse.casos import CASOS

DOCS = RAIZ / "docs"
SALIDA = DOCS / "generado"


def leer(rel: str) -> str:
    p = RAIZ / rel
    return p.read_text(encoding="utf-8") if p.exists() else f"_(falta {rel})_\n"


def bajar_titulos(texto: str, niveles: int = 1) -> str:
    """# → ## fuera de los bloques de código, para que cada documento quede como subsección."""
    out, en_codigo = [], False
    for linea in texto.splitlines():
        if linea.startswith("```"):
            en_codigo = not en_codigo
        if not en_codigo and re.match(r"^#{1,5} ", linea):
            linea = "#" * niveles + linea
        out.append(linea)
    return "\n".join(out) + "\n"


NOTAS_INTERNAS = re.compile(r"^> ((\u2705 )?FICHA MODELO|Esqueleto generado|Formato y profundidad|Las secciones marcadas|"
                            r"Lo que debe establecer|PENDIENTE: redactar)", re.M)


def sin_notas_internas(texto: str) -> str:
    """Quita las instrucciones para el equipo (no van en el informe que se entrega)."""
    return "\n".join(l for l in texto.splitlines()
                     if not NOTAS_INTERNAS.match(l) and not l.startswith(("_Generada por", "_Generado por", "_Generadas desde"))) + "\n"


EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50\u25B6\u2139\uFE0F]")


def sin_emojis(texto: str) -> str:
    """El informe que se entrega no lleva emojis (las marcas pendientes se cuentan aparte)."""
    return EMOJI.sub("", texto)


def sin_mermaid(texto: str, imagen: str = "") -> str:
    """Los bloques Mermaid no se ven en Word/PDF: se reemplazan por la imagen PNG del caso."""
    reemplazo = f"![]({imagen})\n" if imagen else ""
    return re.sub(r"```mermaid\n.*?```\n", reemplazo, texto, flags=re.S)


def seccion_readme(titulo: str) -> str:
    t = leer("README.md")
    m = re.search(rf"## [^\n]*{titulo}[^\n]*\n(.*?)(?=\n## |\Z)", t, re.S)
    return m.group(1).strip() + "\n" if m else "_(sección no encontrada en el README)_\n"


def main() -> None:
    partes = [
        "---\ntitle: \"Deber 2 · Teoría de la Computación — LOGISTPULSE: decisiones, algoritmos y límites computacionales\"\n"
        "subtitle: \"Universidad San Francisco de Quito · Colegio Politécnico\"\n"
        "author: [\"Camila\", \"Luis\", \"Jessica\"]\n---\n",
        "# 1. Introducción, regla conceptual y supuestos\n",
        "P ⊆ NP y NP-completo ⊆ NP; la separación P ≠ NP no está demostrada. Cada correo se clasifica según la evidencia: "
        "(A) algoritmo polinómico conocido, (B) certificado + verificador polinómico sin afirmar NP-completitud, "
        "(C) NP-completo con reducción desde un problema conocido.\n",
        bajar_titulos("## 1. Decisiones de modelado" + leer("docs/DECISIONES_Y_HALLAZGOS.md")
                      .split("## 1. Decisiones de modelado", 1)[1].split("## 4. Qué seleccionar en el simulador")[0]),
        "# 2. Fase A · Autómatas\n",
        bajar_titulos(leer("docs/fase_A_automatas.md")),
        "".join(f"![AFD {k}](../diagramas/afd_{k}.png)\n\n" for k in ("pedido", "reserva", "orden_compra")),
        bajar_titulos(leer("docs/generado/tablas_transiciones.md")),
        "# 3. Fase B · Planta y rutas\n",
        "![Planta con la ruta encontrada](../diagramas/planta_ruta.png)\n\n",
        bajar_titulos(leer("docs/fase_B_rutas.md")),
        "# 4. Fase C · FEFO y reposición\n",
        bajar_titulos(leer("docs/fase_C_fefo_reposicion.md")),
        "# 5. Fase D · Clasificación de los diez correos\n",
        bajar_titulos(leer("docs/generado/tabla_resumen.md")),
    ]
    for c in CASOS:
        img = f"../diagramas/caso_{c.id}.png" if (DOCS / "diagramas" / f"caso_{c.id}.png").exists() else ""
        partes.append(bajar_titulos(sin_mermaid(leer(f"docs/fichas/{c.id}.md"), img)))
    partes += [
        "# 6. Fase E · Implementación y validación\n",
        bajar_titulos(leer("docs/fase_E_implementacion.md")),
        bajar_titulos(leer("docs/generado/crecimiento.md")),
        "# 7. Fase F · Decidibilidad y el problema de la parada\n",
        bajar_titulos(leer("docs/fase_F_nota_parada.md")),
        "# 8. Gestión del proyecto\n",
        bajar_titulos(leer("docs/sprints/backlog.md")),
        *(bajar_titulos(leer(f"docs/sprints/sprint_{i}.md")) for i in (1, 2, 3)),
        "# 9. Supuestos, límites y conclusiones\n",
        bajar_titulos(leer("docs/conclusiones.md")),
        "# 10. Declaración de uso de IA\n",
        seccion_readme("Declaración de uso de IA"),
        "# Anexo A · Inventario de pruebas\n",
        bajar_titulos(leer("docs/generado/inventario_pruebas.md")),
        "# Anexo B · Salidas observadas\n",
        bajar_titulos(leer("docs/generado/salidas_observadas.md")),
    ]
    texto = sin_emojis(sin_notas_internas("\n".join(partes)))
    SALIDA.mkdir(parents=True, exist_ok=True)
    md = SALIDA / "INFORME.md"
    md.write_text(texto, encoding="utf-8")
    print(f"OK {md.relative_to(RAIZ)} ({len(texto.split())} palabras)")

    marcas = len(re.findall(r"^\s*(-\s*)?\[POR REDACTAR\]", texto, re.M)) + texto.count("PENDIENTE") + texto.count("- [ ]")
    if marcas:
        print(f"AVISO El informe todavía tiene {marcas} marcas pendientes ([POR REDACTAR] / PENDIENTE / casillas). "
              "Corre scripts/verificar_entrega.py para ver cuáles.")

    pandoc = shutil.which("pandoc")
    if pandoc is None:
        try:
            import pypandoc  # noqa: F401  (pip install pypandoc_binary)
            pandoc = pypandoc.get_pandoc_path()
        except Exception:
            pandoc = None
    if pandoc is None:
        print("INFO No hay pandoc: abre INFORME.md en Google Docs (Archivo → Abrir) o instala `pip install pypandoc_binary`.")
        return
    docx = SALIDA / "INFORME.docx"
    r = subprocess.run([pandoc, str(md), "-o", str(docx), "--toc", "--toc-depth=2", "-M", "toc-title=Índice",
                        f"--resource-path={SALIDA}", "-f", "markdown-yaml_metadata_block+yaml_metadata_block"],
                       capture_output=True, text=True)
    if r.returncode == 0:
        print(f"OK {docx.relative_to(RAIZ)} → ábrelo en Word/Google Docs y expórtalo a PDF "
              "como docs/INFORME_Deber2_LOGISTPULSE.pdf")
    else:
        print(f"AVISO pandoc falló: {r.stderr.strip()[:300]}")


if __name__ == "__main__":
    main()
