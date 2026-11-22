"""Arma el informe PDF del deber juntando los documentos de los tres integrantes, en orden.

Por defecto sale UN informe legible (el enunciado pide "el enlace al repositorio y el informe PDF"):
secciones 1-10 con el análisis completo de cada fase y, en la Fase D, la tabla resumen y una ficha
resumida por correo (respuesta, clasificación y evidencia, "¿Qué concluimos?"). Lo que ya vive en el
repositorio (fichas completas, código, pruebas, salidas observadas, JFLAP, datos) se referencia con
enlaces a GitHub en vez de copiarlo.

  docs/generado/INFORME.md / .docx

Con --completo sale todo dentro del mismo documento (fichas completas + inventario de pruebas +
salidas observadas, unas 110 páginas).

Para el PDF: abrir INFORME.docx en Word o Google Docs → Descargar / Exportar como PDF y guardarlo
como docs/INFORME_Deber2_LOGISTPULSE.pdf (verificar_entrega.py lo busca).

Uso:  python scripts/armar_informe.py              (informe con enlaces al repositorio)
      python scripts/armar_informe.py --completo   (todo dentro del PDF)
En Colab, si no hay pandoc: !pip install pypandoc_binary
"""

import argparse
import re
import shutil
import subprocess
from urllib.parse import quote

import _bootstrap  # noqa: F401
from _bootstrap import RAIZ

from logistpulse.casos import CASOS

DOCS = RAIZ / "docs"
SALIDA = DOCS / "generado"

AUTORES = ["Camila Granda", "Luis Borja", "Jessica Pijal"]
REPO = "https://github.com/JessPCL/logistpulse-deber2-tc"
TITULO = "Deber 2 · Teoría de la Computación — LOGISTPULSE: decisiones, algoritmos y límites computacionales"
PDF_INFORME = "docs/INFORME_Deber2_LOGISTPULSE.pdf"


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


CHECKLIST = re.compile(r"^(#{1,6}) (Checklist|Lista de verificación)\b")


def sin_checklists(texto: str) -> str:
    """Quita las secciones "Checklist" / "Lista de verificación": son control interno del equipo,
    no contenido del informe (verificar_entrega.py las sigue revisando en los .md)."""
    out, nivel_cortado, en_codigo = [], None, False
    for linea in texto.splitlines():
        if linea.startswith("```"):
            en_codigo = not en_codigo
        m = CHECKLIST.match(linea) if not en_codigo else None
        if m:
            nivel_cortado = len(m.group(1))
            continue
        if nivel_cortado is not None:
            t = re.match(r"^(#{1,6}) ", linea) if not en_codigo else None
            if t and len(t.group(1)) <= nivel_cortado:
                nivel_cortado = None
            else:
                continue
        out.append(linea)
    return "\n".join(out) + "\n"


EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50\u25B6\u2139\uFE0F]")


def sin_emojis(texto: str) -> str:
    """El informe que se entrega no lleva emojis (las marcas pendientes se cuentan aparte)."""
    return EMOJI.sub("", texto)


def sin_mermaid(texto: str, imagen: str = "") -> str:
    """Los bloques Mermaid no se ven en Word/PDF: se reemplazan por la imagen PNG del caso."""
    reemplazo = f"![]({imagen})\n" if imagen else ""
    return re.sub(r"```mermaid\n.*?```\n", reemplazo, texto, flags=re.S)


IMAGENES = (".png", ".jpg", ".jpeg")
ETAPAS = {"s1": "Sprint 1", "s2": "Sprint 2", "s3": "Sprint 3", "final": "Entrega final"}


def pie_de_foto(nombre: str) -> str:
    """s1_04_pr_sin_emojis → 'Sprint 1 · pr sin emojis' (el pie sale del nombre del archivo)."""
    partes = nombre.split("_")
    etapa = ETAPAS.get(partes[0].lower(), "")
    resto = [p for p in (partes[1:] if etapa else partes) if not re.fullmatch(r"\d+[a-z]?", p)]
    texto = " ".join(resto) or nombre
    return f"{etapa} · {texto}" if etapa else texto


def evidencias_gestion() -> str:
    """Capturas de docs/evidencias/ (ruleset, Issues, PR aprobados, Actions, release), en orden."""
    carpeta = DOCS / "evidencias"
    orden = list(ETAPAS)  # s1, s2, s3 y al final "final" (no alfabético)

    def clave(p):
        etapa = p.stem.split("_")[0].lower()
        return (orden.index(etapa) if etapa in orden else len(orden), p.name.lower())
    imgs = sorted((p for p in carpeta.iterdir() if p.suffix.lower() in IMAGENES), key=clave) if carpeta.exists() else []
    if not imgs:
        return "## Evidencias de gestión\n\n_(todavía no hay capturas en docs/evidencias)_\n"
    return "## Evidencias de gestión\n\n" + "\n".join(
        f"![{pie_de_foto(p.stem)}](../evidencias/{quote(p.name)})\n" for p in imgs)


def sin_titulo(texto: str) -> str:
    """Quita el título "# ..." de la primera línea: el informe ya pone su propio encabezado numerado."""
    lineas = texto.splitlines()
    return "\n".join(lineas[1:] if lineas and lineas[0].startswith("# ") else lineas) + "\n"


def seccion_readme(titulo: str) -> str:
    t = leer("README.md")
    m = re.search(rf"## [^\n]*{titulo}[^\n]*\n(.*?)(?=\n## |\Z)", t, re.S)
    return m.group(1).strip() + "\n" if m else "_(sección no encontrada en el README)_\n"



def solo_secciones(texto: str, prefijos: tuple) -> str:
    """Deja el encabezado del documento (lo que va antes del primer "## ") y solo las secciones "## "
    cuyo título empieza con alguno de los prefijos (fuera de los bloques de código)."""
    out, dentro, en_codigo, antes_del_primero = [], True, False, True
    for linea in texto.splitlines():
        if linea.startswith("```"):
            en_codigo = not en_codigo
        if not en_codigo and linea.startswith("## "):
            antes_del_primero = False
            dentro = linea[3:].lstrip().startswith(prefijos)
        if antes_del_primero or dentro:
            out.append(linea)
    return "\n".join(out) + "\n"


def enlace(rel: str, texto: str = "") -> str:
    """Enlace a un archivo o carpeta del repositorio en GitHub (rama main)."""
    tipo = "tree" if (RAIZ / rel).is_dir() else "blob"
    return f"[{texto or rel}]({REPO}/{tipo}/main/{rel})"


RESUMEN_FICHA = ("0.", "3.", "¿Qué concluimos?")


def ficha(cid: str, resumida: bool) -> str:
    """Ficha de un correo. Resumida: respuesta, clasificación y evidencia, y "¿Qué concluimos?"
    (decidibilidad, computabilidad y complejidad), con el enlace a la ficha completa del repositorio."""
    rel = f"docs/fichas/{cid}.md"
    texto = leer(rel)
    if resumida:
        return bajar_titulos(sin_mermaid(solo_secciones(texto, RESUMEN_FICHA))) + (
            f"\n**Ficha completa** (resumen del correo, entrada y salida, decidibilidad y computabilidad, "
            f"algoritmo, Big-O, código, pruebas y salida observada): {enlace(rel)}\n")
    img = f"../diagramas/caso_{cid}.png" if (DOCS / "diagramas" / f"caso_{cid}.png").exists() else ""
    return bajar_titulos(sin_mermaid(texto, img))


DONDE_ESTA = [
    ("Fichas completas de los diez correos (incluyen código, pruebas y salida observada)", "docs/fichas"),
    ("Código fuente (autómatas, rutas, FEFO, reposición, los diez casos, verificadores)", "logistpulse"),
    ("Pruebas reproducibles (casos normales, límite e inválidos)", "tests"),
    ("Inventario de pruebas", "docs/generado/inventario_pruebas.md"),
    ("Salidas observadas de las demos", "docs/generado/salidas_observadas.md"),
    ("Modelos JFLAP (.jff), secuencias de prueba y capturas", "jflap"),
    ("Tablas de transiciones generadas desde el código", "docs/generado/tablas_transiciones.md"),
    ("Datos de prueba (planta, inventario, casos)", "data"),
    ("Backlog y registro de los tres sprints", "docs/sprints"),
    ("Respuestas del simulador y reporte de los diez correos", "docs/simulador"),
    ("Instrucciones de ejecución", "README.md"),
]


def donde_esta() -> str:
    filas = "\n".join(f"| {que} | {enlace(rel)} |" for que, rel in DONDE_ESTA if (RAIZ / rel).exists())
    return ("## Dónde está cada cosa\n\n"
            f"Este informe resume el análisis; el material completo y ejecutable está en el repositorio público "
            f"{REPO} (versión etiquetada `v1.0`).\n\n"
            "| Material | En el repositorio |\n|---|---|\n" + filas + "\n")


def evidencia_jflap() -> str:
    """Las tres capturas de Multiple Run de JFLAP (las demás capturas quedan en jflap/capturas/)."""
    imgs = [(k, f"jflap/capturas/{k}_multiple_run.png") for k in ("pedido", "reserva", "orden_compra")]
    imgs = [(k, rel) for k, rel in imgs if (RAIZ / rel).exists()]
    if not imgs:
        return ""
    return ("## Evidencia JFLAP (Multiple Run)\n\n" +
            "".join(f"![JFLAP · {k.replace('_', ' ')} · Multiple Run](../../{rel})\n\n" for k, rel in imgs) +
            f"Determinismo y trazas válidas/inválidas de cada autómata: {enlace('jflap/capturas')}.\n")


def portada(titulo: str = TITULO) -> str:
    autores = ", ".join(f'"{a}"' for a in AUTORES)
    return (f'---\ntitle: "{titulo}"\n'
            'subtitle: "Universidad San Francisco de Quito · Colegio Politécnico"\n'
            f"author: [{autores}]\n---\n")


def cuerpo(completo: bool) -> list:
    """Secciones 1-10. Sin --completo: fichas resumidas y enlaces al repositorio en vez de copias."""
    return [
        "# 1. Introducción, regla conceptual y supuestos\n",
        "P ⊆ NP y NP-completo ⊆ NP; la separación P ≠ NP no está demostrada. Cada correo se clasifica según la evidencia: "
        "(A) algoritmo polinómico conocido, (B) certificado + verificador polinómico sin afirmar NP-completitud, "
        "(C) NP-completo con reducción desde un problema conocido.\n",
        donde_esta(),
        bajar_titulos("## 1. Decisiones de modelado" + leer("docs/DECISIONES_Y_HALLAZGOS.md")
                      .split("## 1. Decisiones de modelado", 1)[1].split("## 4. Qué seleccionar en el simulador")[0]),
        "# 2. Fase A · Autómatas\n",
        bajar_titulos(sin_titulo(leer("docs/fase_A_automatas.md"))),
        "".join(f"![AFD {k}](../diagramas/afd_{k}.png)\n\n" for k in ("pedido", "reserva", "orden_compra")),
        evidencia_jflap(),
        bajar_titulos(leer("docs/generado/tablas_transiciones.md")) if completo else "",
        "# 3. Fase B · Planta y rutas\n",
        "![Planta con la ruta encontrada](../diagramas/planta_ruta.png)\n\n",
        bajar_titulos(sin_titulo(leer("docs/fase_B_rutas.md"))),
        "# 4. Fase C · FEFO y reposición\n",
        bajar_titulos(sin_titulo(leer("docs/fase_C_fefo_reposicion.md"))),
        "# 5. Fase D · Clasificación de los diez correos\n",
        bajar_titulos(leer("docs/generado/tabla_resumen.md")),
        *(ficha(c.id, resumida=not completo) for c in CASOS),
        "# 6. Fase E · Implementación y validación\n",
        bajar_titulos(sin_titulo(leer("docs/fase_E_implementacion.md"))),
        bajar_titulos(leer("docs/generado/crecimiento.md")),
        "# 7. Fase F · Decidibilidad y el problema de la parada\n",
        bajar_titulos(sin_titulo(leer("docs/fase_F_nota_parada.md"))),
        "# 8. Gestión del proyecto\n",
        bajar_titulos(leer("docs/sprints/backlog.md")),
        *(bajar_titulos(leer(f"docs/sprints/sprint_{i}.md")) for i in (1, 2, 3)),
        evidencias_gestion(),
        "# 9. Supuestos, límites y conclusiones\n",
        bajar_titulos(sin_titulo(leer("docs/conclusiones.md"))),
        "# 10. Declaración de uso de IA\n",
        seccion_readme("Declaración de uso de IA"),
    ]


def anexos() -> list:
    """Solo con --completo: el inventario de pruebas y las salidas observadas dentro del PDF."""
    return ["# Anexo A · Inventario de pruebas\n", bajar_titulos(leer("docs/generado/inventario_pruebas.md")),
            "# Anexo B · Salidas observadas\n", bajar_titulos(leer("docs/generado/salidas_observadas.md"))]


def buscar_pandoc():
    pandoc = shutil.which("pandoc")
    if pandoc is None:
        try:
            import pypandoc  # noqa: F401  (pip install pypandoc_binary)
            pandoc = pypandoc.get_pandoc_path()
        except Exception:
            pandoc = None
    return pandoc


LIMPIEZA = [  # títulos pensados para el equipo → título para el profesor
    ("2. Hallazgos (úsenlos en el informe y en la exposición: suman puntos)", "2. Hallazgos"),
    ("3. Convenciones de redacción", "3. Modelo de cómputo y convenciones"),
    ("Backlog del producto · lo mantiene quien tenga el rol de Coordinación en cada sprint", "Backlog del producto"),
]


def escribir(nombre: str, partes: list, pandoc, pdf: str) -> str:
    """Escribe docs/generado/<nombre>.md (y .docx si hay pandoc). Devuelve el texto sin checklists."""
    completo = sin_emojis(sin_notas_internas("\n".join(partes)))
    for viejo, nuevo in LIMPIEZA:
        completo = completo.replace(viejo, nuevo)
    texto = sin_checklists(completo)
    SALIDA.mkdir(parents=True, exist_ok=True)
    md = SALIDA / f"{nombre}.md"
    md.write_text(texto, encoding="utf-8")
    print(f"OK {md.relative_to(RAIZ)} ({len(texto.split())} palabras)")
    if pandoc is None:
        return completo
    docx = SALIDA / f"{nombre}.docx"
    r = subprocess.run([pandoc, str(md), "-o", str(docx), "--toc", "--toc-depth=2", "-M", "toc-title=Índice",
                        f"--resource-path={SALIDA}", "-f", "markdown-yaml_metadata_block+yaml_metadata_block+lists_without_preceding_blankline"],
                       capture_output=True, text=True)
    if r.returncode == 0:
        print(f"OK {docx.relative_to(RAIZ)} → ábrelo en Word (muestra bien las fórmulas) y expórtalo a PDF como {pdf}")
    else:
        print(f"AVISO pandoc falló con {nombre}: {r.stderr.strip()[:300]}")
    return completo


def main() -> None:
    ap = argparse.ArgumentParser(description="Arma el informe PDF del deber.")
    ap.add_argument("--completo", action="store_true",
                    help="todo dentro del PDF (fichas completas, inventario de pruebas, salidas observadas)")
    args = ap.parse_args()

    pandoc = buscar_pandoc()
    partes = [portada(), *cuerpo(completo=args.completo), *(anexos() if args.completo else [])]
    crudo = escribir("INFORME", partes, pandoc, PDF_INFORME)
    for viejo in ("ANEXOS.md", "ANEXOS.docx"):  # de una versión anterior del armador: ya no se usan
        (SALIDA / viejo).unlink(missing_ok=True)

    todas = crudo + "".join(leer(f"docs/fichas/{c.id}.md") for c in CASOS) if not args.completo else crudo
    marcas = (len(re.findall(r"^\s*(-\s*)?\[POR REDACTAR\]", todas, re.M)) + todas.count("PENDIENTE")
              + todas.count("- [ ]"))
    if marcas:
        print(f"AVISO Todavía hay {marcas} marcas pendientes ([POR REDACTAR] / PENDIENTE / casillas). "
              "Corre scripts/verificar_entrega.py para ver cuáles.")
    if pandoc is None:
        print("INFO No hay pandoc: abre INFORME.md en Google Docs (Archivo → Abrir) o instala `pip install pypandoc_binary`.")


if __name__ == "__main__":
    main()
