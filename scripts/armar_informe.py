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
import zipfile
from pathlib import Path
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
VERSION = "v1.1"
FECHA = "24 de noviembre de 2026"


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


CHECKLIST = re.compile(r"^(#{1,6}) (Checklist|Lista de verificación|Preguntas)\b")


def sin_checklists(texto: str) -> str:
    """Quita las secciones "Checklist", "Lista de verificación" y "Preguntas …" (de práctica para la
    defensa oral): son control interno del equipo, no contenido del informe. Siguen en los .md."""
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


PIES = {
    "s1_01_ruleset_main": "Sprint 1 · Regla que protege main: PR, una aprobación y pruebas en verde",
    "s1_02_colaboradores": "Sprint 1 · Colaboradores del repositorio",
    "s1_03_issues_backlog": "Sprint 1 · Issues del backlog con responsables",
    "s1_04_pr_sin_emojis": "Sprint 1 · PR aprobado por un compañero con las pruebas en verde",
    "s1_05_actions_verde": "Sprint 1 · Pruebas automáticas en GitHub Actions",
    "s1_06_codespace_pruebas": "Sprint 1 · Pruebas ejecutadas en Codespaces",
    "s2_01_revision_fase_a": "Sprint 2 · Revisión y fusión del PR de la Fase A",
    "s2_02_revision_de_pares": "Sprint 2 · Revisión de pares",
    "s2_03_issues_cerrados": "Sprint 2 · Issues cerrados desde sus PR",
    "s3_01_prs_cerrados": "Sprint 3 · Pull requests cerrados",
    "final_01_contribuidores": "Entrega · Contribuciones de los tres integrantes",
    "final_02_release_v1": "Entrega · Release v1.0 con el informe adjunto",
}


def pie_de_foto(nombre: str) -> str:
    """Pie de cada captura: el de PIES o, si no está, uno armado con el nombre del archivo."""
    if nombre in PIES:
        return PIES[nombre]
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
    return ("## Evidencias de gestión\n\nCapturas de GitHub que respaldan la gestión: protección de `main`, Issues, PR revisados, "
            "pruebas automáticas y release.\n\n") + "\n".join(
        f"![{pie_de_foto(p.stem)}](../evidencias/{quote(p.name)})\n" for p in imgs)


def sin_titulo(texto: str) -> str:
    """Quita el título "# ..." de la primera línea: el informe ya pone su propio encabezado numerado."""
    lineas = texto.splitlines()
    return "\n".join(lineas[1:] if lineas and lineas[0].startswith("# ") else lineas) + "\n"


def seccion_readme(titulo: str) -> str:
    t = leer("README.md")
    m = re.search(rf"## [^\n]*{titulo}[^\n]*\n(.*?)(?=\n## |\Z)", t, re.S)
    return m.group(1).strip() + "\n" if m else "_(sección no encontrada en el README)_\n"




# ---------------------------------------------------------------- fórmulas, numeración y estilo
SIMBOLOS = {
    "Sigma": "Σ", "delta": "δ", "pi": "π", "Theta": "Θ", "varepsilon": "ε", "epsilon": "ε", "alpha": "α",
    "lambda": "λ", "sigma": "σ", "in": "∈", "notin": "∉", "cdot": "·", "times": "×", "le": "≤", "leq": "≤",
    "ge": "≥", "geq": "≥", "neq": "≠", "ne": "≠", "approx": "≈", "cong": "≅", "equiv": "≡", "to": "→",
    "rightarrow": "→", "Rightarrow": "⇒", "Leftrightarrow": "⇔", "iff": "⇔", "subseteq": "⊆", "dots": "…",
    "ldots": "…", "cdots": "⋯", "lfloor": "⌊", "rfloor": "⌋", "lceil": "⌈", "rceil": "⌉", "infty": "∞",
    "forall": "∀", "exists": "∃", "neg": "¬", "lor": "∨", "land": "∧", "cup": "∪", "cap": "∩", "emptyset": "∅",
    "mid": "∣", "log": "log", "ln": "ln", "min": "min", "max": "max", "bmod": "mod", "mod": "mod",
}


def _grupo(s, i):
    """Devuelve (contenido, fin) del argumento que empieza en s[i]: {…} o un solo carácter."""
    while i < len(s) and s[i] == " ":
        i += 1
    if i < len(s) and s[i] == "{":
        nivel, j = 0, i
        while j < len(s):
            nivel += {"{": 1, "}": -1}.get(s[j], 0)
            if nivel == 0:
                return s[i + 1:j], j + 1
            j += 1
        return s[i + 1:], len(s)
    if i < len(s) and s[i] == "\\":
        m = re.match(r"\\[A-Za-z]+", s[i:])
        if m:
            return m.group(0), i + len(m.group(0))
    return s[i:i + 1], i + 1


def tex_a_texto(tex: str) -> str:
    """TeX sencillo → texto Markdown con Unicode, subíndices ~x~ y superíndices ^x^ (sin OMML)."""
    s, out, i = tex.strip(), [], 0
    while i < len(s):
        c = s[i]
        if c == "\\":
            m = re.match(r"\\([A-Za-z]+)|\\(.)", s[i:])
            nombre = m.group(1) or m.group(2)
            i += len(m.group(0))
            if nombre in ("text", "mathrm", "textit", "mathit", "mathbf", "textbf", "operatorname", "mathsf", "texttt"):
                arg, i = _grupo(s, i)
                out.append(tex_a_texto(arg) if "\\" in arg else arg)
            elif nombre == "sqrt":
                arg, i = _grupo(s, i)
                t = tex_a_texto(arg)
                out.append("√" + (t if len(t) == 1 else f"({t})"))
            elif nombre == "xrightarrow":
                arg, i = _grupo(s, i)
                out.append(f"—{tex_a_texto(arg)}→")
            elif nombre == "pmod":
                arg, i = _grupo(s, i)
                out.append(f" (mod {tex_a_texto(arg)})")
            elif nombre in ("left", "right", "big", "Big", "displaystyle"):
                pass
            elif nombre in (",", ";", " ", "quad", "qquad", ":"):
                out.append(" ")
            elif nombre == "!":
                pass
            elif nombre in ("{", "}", "%", "$", "#", "&", "_"):
                out.append(nombre)
            elif nombre == "\\":
                out.append(" ")
            else:
                out.append(SIMBOLOS.get(nombre, nombre))
                # \log p, \bmod 7: TeX pone espacio después de los operadores con nombre
                if nombre in ("log", "ln", "min", "max", "bmod", "mod") and i < len(s) and s[i] not in " ({_^":
                    out.append(" ")
        elif c in "_^":
            arg, i = _grupo(s, i + 1)
            t = tex_a_texto(arg).replace(" ", "\\ ")
            if t == "*":
                t = "\\*"
            out.append(f"~{t}~" if c == "_" else f"^{t}^")
        elif c in "{}":
            i += 1
        elif c == "&":
            i += 1
        else:
            out.append(c)
            i += 1
    texto = "".join(out)
    texto = re.sub(r" {2,}", " ", texto).replace("⌊ ", "⌊").replace(" ⌋", "⌋").replace("-", "−")
    return texto.replace("|", "\\|").replace("*", "\\*").replace("\\\\*", "\\*")


DISPLAY = re.compile(r"\$\$(.+?)\$\$", re.S)
INLINE = re.compile(r"(?<![\\$])\$(?=\S)([^$\n]+?)(?<=\S)\$(?![\d$])")


def formulas_a_texto(texto: str) -> str:
    """Cambia las fórmulas $…$ por texto (Times New Roman), fuera de los bloques y del código en línea."""
    partes = re.split(r"(```.*?```|`[^`\n]*`)", texto, flags=re.S)
    for k in range(0, len(partes), 2):
        p = DISPLAY.sub(lambda m: tex_a_texto(m.group(1)), partes[k])
        partes[k] = INLINE.sub(lambda m: tex_a_texto(m.group(1)), p)
    return "".join(partes)


def numerar(texto: str) -> str:
    """Numeración única: # → "N.", ## → "N.k"; los niveles ### y más bajos van sin número.
    Quita la numeración propia de cada documento (1., 2.1, 0.) para que no haya dos sistemas."""
    out, h1, h2, en_codigo, anexo = [], 0, 0, False, False
    for linea in texto.splitlines():
        if linea.startswith("```"):
            en_codigo = not en_codigo
        m = None if en_codigo else re.match(r"^(#{1,6}) (.*)$", linea)
        if m:
            nivel, titulo = len(m.group(1)), re.sub(r"^\d+(\.\d+)*\.?\s+", "", m.group(2)).strip()
            if nivel == 1:
                anexo = titulo.startswith("Anexo")
                h1, h2 = (h1, 0) if anexo else (h1 + 1, 0)
                linea = f"# {titulo}" if anexo else f"# {h1}. {titulo}"
            elif nivel == 2 and anexo:
                linea = f"## {titulo}"
            elif nivel == 2:
                h2 += 1
                linea = f"## {h1}.{h2} {titulo}"
            else:
                linea = f"{m.group(1)} {titulo}"
        out.append(linea)
    return "\n".join(out) + "\n"


NOMBRES = {"Camila": "Camila Granda", "Luis": "Luis Borja", "Jessica": "Jessica Pijal"}


def responsables(texto: str) -> str:
    """Una sola forma para las líneas de autoría: "**Responsable:** Nombre Apellido" (sin notas de rúbrica)."""
    def fila(m):
        nombre = next((v for k, v in NOMBRES.items() if k in m.group(0)), None)
        return f"**Responsable:** {nombre}" if nombre else m.group(0)
    return re.sub(r"^\*\*Responsable[^\n]*$", fila, texto, flags=re.M)


def rutas_desde_docs(texto: str) -> str:
    """Las imágenes de docs/*.md apuntan a diagramas/…; el informe se arma en docs/generado/."""
    return re.sub(r"\]\((?!https?:|\.\./|/)diagramas/", "](../diagramas/", texto)


def afd_en_su_seccion(texto: str) -> str:
    """Pone cada diagrama de estados junto a su tabla de transiciones (no al final de la fase)."""
    return re.sub(r"^\*Diagrama:\* `docs/diagramas/(afd_\w+)\.png` · \*Archivo JFLAP:\* `([^`]+)`\.",
                  lambda m: f"![Diagrama de estados ({m.group(1)[4:].replace('orden_compra', 'orden de compra')})](../diagramas/{m.group(1)}.png)"
                            f"\n\nArchivo JFLAP: `{m.group(2)}`.", texto, flags=re.M)


def fase(rel: str) -> str:
    """Documento de una fase como cuerpo de su sección: sin su título, con sus ## como subsecciones."""
    return afd_en_su_seccion(rutas_desde_docs(sin_titulo(leer(rel))))


TNR = 'w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="Times New Roman" w:cs="Times New Roman"'
ORDEN_RPR = ["rStyle", "rFonts", "b", "bCs", "i", "iCs", "caps", "smallCaps", "strike", "dstrike", "outline",
             "shadow", "emboss", "imprint", "noProof", "snapToGrid", "vanish", "webHidden", "color", "spacing",
             "w", "kern", "position", "sz", "szCs", "highlight", "u", "effect", "bdr", "shd", "fitText",
             "vertAlign", "rtl", "cs", "em", "lang", "eastAsianLayout", "specVanish", "oMath"]
HIJO = re.compile(r"<w:(\w+)\b(?:[^>]*?/>|[^>]*>.*?</w:\1>)", re.S)


def _rpr_times(interior: str, negro: bool) -> str:
    hijos = [(m.group(1), m.group(0)) for m in HIJO.finditer(interior)]
    hijos = [(n, x) for n, x in hijos if n not in ("rFonts", "sz", "szCs") and not (negro and n == "color")]
    hijos += [("rFonts", f"<w:rFonts {TNR}/>"), ("sz", '<w:sz w:val="24"/>'), ("szCs", '<w:szCs w:val="24"/>')]
    if negro:
        hijos.append(("color", '<w:color w:val="000000"/>'))
    hijos.sort(key=lambda h: ORDEN_RPR.index(h[0]) if h[0] in ORDEN_RPR else len(ORDEN_RPR))
    return "<w:rPr>" + "".join(x for _, x in hijos) + "</w:rPr>"


def _estilo(m) -> str:
    bloque = m.group(0)
    sid = re.search(r'w:styleId="([^"]+)"', bloque)
    negro = bool(sid) and re.match(r"(Heading|Title|Subtitle|Author|Date|TOCHeading)", sid.group(1)) is not None
    if "<w:rPr" not in bloque:  # hereda Times New Roman 12 de los valores por defecto (docDefaults)
        return bloque
    return re.sub(r"<w:rPr>(.*?)</w:rPr>|<w:rPr/>", lambda r: _rpr_times(r.group(1) or "", negro), bloque, flags=re.S)


def formato_times(docx: Path) -> None:
    """Times New Roman 12 en todo el documento: estilos, valores por defecto y tema del .docx (solo stdlib)."""
    tmp = docx.with_suffix(".tmp.docx")
    with zipfile.ZipFile(docx) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            datos = zin.read(item.filename)
            if item.filename == "word/styles.xml":
                x = datos.decode("utf-8")
                x = re.sub(r"<w:style\b.*?</w:style>", _estilo, x, flags=re.S)
                x = re.sub(r"<w:rPrDefault>(.*?)</w:rPrDefault>",
                           lambda r: "<w:rPrDefault>" + re.sub(r"<w:rPr>(.*?)</w:rPr>|<w:rPr/>",
                                                               lambda q: _rpr_times(q.group(1) or "", False), r.group(1), flags=re.S)
                           + "</w:rPrDefault>", x, flags=re.S)
                datos = x.encode("utf-8")
            elif item.filename == "word/settings.xml" and b"updateFields" not in datos:
                # Word pregunta al abrir si actualiza los campos: así el índice sale con sus páginas
                marca = b'<w:updateFields w:val="true"/>'
                datos = (datos.replace(b"<w:footnotePr", marca + b"<w:footnotePr", 1) if b"<w:footnotePr" in datos
                         else re.sub(rb"(<w:settings\b[^>]*>)", lambda m: m.group(1) + marca, datos, count=1))
            elif item.filename.startswith("word/theme/") and item.filename.endswith(".xml"):
                datos = re.sub(rb'<a:latin typeface="[^"]*"', b'<a:latin typeface="Times New Roman"', datos)
            elif item.filename == "word/document.xml":
                x = datos.decode("utf-8")
                x = re.sub(r"<w:rFonts\b[^>]*/>", f"<w:rFonts {TNR}/>", x)
                x = re.sub(r'<w:sz w:val="\d+"/>', '<w:sz w:val="24"/>', x)
                x = re.sub(r'<w:szCs w:val="\d+"/>', '<w:szCs w:val="24"/>', x)
                salto = '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'  # portada | índice | cuerpo
                i = x.find("<w:sdt><w:sdtPr><w:docPartObj><w:docPartGallery")
                j = x.find("</w:sdt>", i)
                if i >= 0 and j >= 0:
                    j += len("</w:sdt>")
                    x = x[:i] + salto + x[i:j] + salto + x[j:]
                datos = x.encode("utf-8")
            zout.writestr(item, datos)
    tmp.replace(docx)


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
    """Ficha de un correo. Resumida: respuesta, clasificación y evidencia, y la conclusión
    (decidibilidad, computabilidad y complejidad), con el enlace a la ficha completa del repositorio."""
    rel = f"docs/fichas/{cid}.md"
    texto = leer(rel)
    if resumida:
        corto = solo_secciones(texto, RESUMEN_FICHA).replace("## ¿Qué concluimos?", "## Conclusión")
        return bajar_titulos(sin_mermaid(corto)) + f"\nFicha completa: {enlace(rel)}\n"
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
    return ("## Material de respaldo en el repositorio\n\n"
            f"Este informe resume el análisis. El material completo y ejecutable está en el repositorio público "
            f"{REPO}; la versión entregada es la etiqueta `{VERSION}`.\n\n"
            "| Material | En el repositorio |\n|---|---|\n" + filas + "\n")


def evidencia_jflap() -> str:
    """Las tres capturas de Multiple Run de JFLAP (las demás capturas quedan en jflap/capturas/)."""
    imgs = [(k, f"jflap/capturas/{k}_multiple_run.png") for k in ("pedido", "reserva", "orden_compra")]
    imgs = [(k, rel) for k, rel in imgs if (RAIZ / rel).exists()]
    if not imgs:
        return ""
    return ("## Evidencia JFLAP (Multiple Run)\n\n" +
            "".join(f"![JFLAP · {k.replace('orden_compra', 'orden de compra')} · Multiple Run](../../{rel})\n\n" for k, rel in imgs) +
            f"Determinismo y trazas válidas/inválidas de cada autómata: {enlace('jflap/capturas')}.\n")


def portada(titulo: str = TITULO) -> str:
    autores = ", ".join(f'"{a}"' for a in AUTORES)
    return (f'---\ntitle: "{titulo}"\n'
            'subtitle: "Universidad San Francisco de Quito · Colegio Politécnico"\n'
            f"author: [{autores}]\ndate: \"{FECHA}\"\nlang: es\n---\n")


INTRODUCCION = """LOGISTPULSE es la empresa de logística del enunciado. Este trabajo modela sus procesos con tres autómatas finitos deterministas (Fase A), busca rutas en la planta con Dijkstra y BFS (Fase B), define la selección de lotes FEFO y la regla de reposición (Fase C), clasifica diez problemas recibidos por correo como P, NP o NP-completos (Fase D), los implementa y prueba en Python (Fase E) y distingue decidibilidad de eficiencia con el problema de la parada (Fase F).

**Regla de clasificación.** P ⊆ NP y NP-completo ⊆ NP; la separación P ≠ NP no está demostrada. Cada correo se clasifica según la evidencia disponible: (A) un algoritmo polinómico conocido; (B) un certificado con verificador polinómico, sin afirmar NP-completitud porque no se conoce una reducción ni un algoritmo polinómico; (C) NP-completitud, demostrada con la pertenencia a NP y una reducción polinómica desde un problema NP-completo conocido.

**Organización.** Las secciones 2 a 7 corresponden a las fases A a F. La sección 8 resume la gestión del proyecto (backlog, sprints y evidencias), la sección 9 reúne los supuestos, los límites de la inferencia y las conclusiones, y la sección 10 declara el uso de IA.
"""

HALLAZGOS_LEAD = ("Durante el análisis aparecieron catorce resultados que precisan o corrigen una lectura rápida del enunciado. "
                  "Cada uno está respaldado por una prueba automática del repositorio.\n")

MODELO_COMPUTO = """## Modelo de cómputo y convenciones

- **Modelo de cómputo:** máquina de Turing determinista (o, de forma equivalente, el modelo RAM) con enteros codificados en binario. Un número B ocupa unos log₂B bits, y M(k) es el costo de multiplicar números de k bits (O(k²) con el método escolar).
- **Big-O:** siempre con las variables definidas (V, E, n, m, k, L, P, B) y para tiempo y espacio.
- **Reducciones (grupo C):** cada una va del problema conocido al nuestro (CONOCIDO ≤p NUESTRO) e incluye la construcción, la correctitud (⇔) y el costo polinómico de la transformación.
- **Referencias:** Sipser, 3.ª ed. (PATH ∈ P, Teo. 7.14; Cook–Levin, §7.4; VERTEX-COVER y HAMPATH, §7.5; A_TM indecidible, Teo. 4.11; HALT_TM indecidible, Teo. 5.1) y CLRS (caminos mínimos, flujo máximo y NP-completitud).
"""

INTRO_FICHAS = ("Cada ficha resumida presenta la respuesta al remitente, la clasificación con su evidencia y la conclusión "
                "sobre decidibilidad, computabilidad y complejidad. La ficha completa del repositorio añade la entrada y la salida, "
                "el algoritmo, el análisis Big-O, el código, las pruebas y la salida observada.\n")


def hallazgos() -> str:
    t = leer("docs/DECISIONES_Y_HALLAZGOS.md")
    cuerpo_h = t.split("## 2. Hallazgos", 1)[1].split("\n", 1)[1].split("\n## 3.")[0]
    return "## Hallazgos del análisis\n\n" + HALLAZGOS_LEAD + "\n" + cuerpo_h.strip().rstrip("-").strip() + "\n"


def cuerpo(completo: bool) -> list:
    """Secciones 1-10. Sin --completo: fichas resumidas y enlaces al repositorio en vez de copias."""
    return [
        "# Introducción\n", INTRODUCCION, donde_esta(), hallazgos(), MODELO_COMPUTO,
        "# Fase A · Autómatas\n", fase("docs/fase_A_automatas.md"), evidencia_jflap(),
        bajar_titulos(leer("docs/generado/tablas_transiciones.md")) if completo else "",
        "# Fase B · Planta y rutas\n", fase("docs/fase_B_rutas.md"),
        "# Fase C · FEFO y reposición\n", fase("docs/fase_C_fefo_reposicion.md"),
        "# Fase D · Clasificación de los diez correos\n",
        bajar_titulos(leer("docs/generado/tabla_resumen.md")), "" if completo else INTRO_FICHAS,
        *(ficha(c.id, resumida=not completo) for c in CASOS),
        "# Fase E · Implementación y validación\n", fase("docs/fase_E_implementacion.md"),
        bajar_titulos(leer("docs/generado/crecimiento.md")),
        "# Fase F · Decidibilidad y el problema de la parada\n", fase("docs/fase_F_nota_parada.md"),
        "# Gestión del proyecto\n",
        bajar_titulos(leer("docs/sprints/backlog.md")),
        *(bajar_titulos(leer(f"docs/sprints/sprint_{i}.md")) for i in (1, 2, 3)),
        evidencias_gestion(),
        "# Supuestos, límites y conclusiones\n", fase("docs/conclusiones.md"),
        "# Declaración de uso de IA\n",
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
    ("Tabla resumen de los 10 correos", "Tabla resumen de los diez correos"),
    ("Backlog del producto · lo mantiene quien tenga el rol de Coordinación en cada sprint", "Backlog del producto"),
]


def escribir(nombre: str, partes: list, pandoc, pdf: str) -> str:
    """Escribe docs/generado/<nombre>.md (y .docx en Times New Roman 12 si hay pandoc).
    Devuelve el texto antes de quitar checklists (para contar marcas pendientes)."""
    completo = sin_emojis(sin_notas_internas("\n".join(partes)))
    for viejo, nuevo in LIMPIEZA:
        completo = completo.replace(viejo, nuevo)
    texto = numerar(formulas_a_texto(responsables(sin_checklists(completo))))
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
        formato_times(docx)
        print(f"OK {docx.relative_to(RAIZ)} (Times New Roman 12) → ábrelo en Word o Google Docs y expórtalo a PDF como {pdf}")
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
