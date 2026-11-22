"""Revisión automática ANTES de entregar, criterio por criterio de la rúbrica.

Comprueba lo que una máquina sí puede comprobar: pruebas, archivos, coherencia
.jff ⇄ Python, salidas regeneradas, marcas pendientes ([POR REDACTAR] / PENDIENTE /
casillas sin marcar), emojis en los entregables, historial Git (commits, autores,
tag v1.0) y el PDF del informe.
NO califica la calidad de la redacción: eso lo revisa el equipo con la lista de
verificación de docs/PLANTILLA_FICHA.md.

Uso:  python scripts/verificar_entrega.py
"""

import io
import re
import shutil
import subprocess
import unittest
from contextlib import redirect_stdout

import _bootstrap  # noqa: F401
from _bootstrap import RAIZ

OK, PEND, MAL = "[OK]", "[PENDIENTE]", "[ERROR]"


def leer(rel: str) -> str:
    p = RAIZ / rel
    return p.read_text(encoding="utf-8") if p.exists() else ""


def doc_redactado(rel: str, responsable: str):
    texto = leer(rel)
    if not texto:
        return MAL, f"{rel} no existe ({responsable})"
    if "PENDIENTE" in texto or "- [ ]" in texto:
        return PEND, f"{rel}: sin redactar o con casillas sin marcar ({responsable})"
    return OK, f"{rel} redactado"


# ----------------------------------------------------------------------------- comprobaciones
def chk_pruebas():
    import sys
    if str(RAIZ) not in sys.path:
        sys.path.insert(0, str(RAIZ))
    suite = unittest.defaultTestLoader.discover(str(RAIZ / "tests"), top_level_dir=str(RAIZ))
    res = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
    if res.wasSuccessful():
        return OK, f"{res.testsRun} pruebas OK"
    return MAL, f"{len(res.failures)} fallos y {len(res.errors)} errores de {res.testsRun} pruebas"


def chk_jff():
    from logistpulse.automatas import AUTOMATAS
    from logistpulse.automatas.jflap import leer_jff
    malos = []
    for clave, afd in AUTOMATAS.items():
        ruta = RAIZ / "jflap" / f"{clave}.jff"
        if not ruta.exists():
            malos.append(f"falta {clave}.jff")
            continue
        j = leer_jff(ruta)
        if dict(j.delta) != dict(afd.delta) or set(j.finales) != set(afd.finales) or j.inicial != afd.inicial:
            malos.append(f"{clave}.jff no coincide con definiciones.py (corre scripts/generar_jflap.py)")
    return (MAL, "; ".join(malos)) if malos else (OK, "3 .jff idénticos a los autómatas probados")


def chk_capturas():
    caps = list((RAIZ / "jflap" / "capturas").glob("*multiple_run*.png"))
    return (OK, f"{len(caps)} capturas de Multiple Run") if len(caps) >= 3 else \
        (PEND, f"{len(caps)}/3 capturas de Multiple Run en jflap/capturas/ (Camila)")


def chk_archivos(rels, quien):
    faltan = [r for r in rels if not (RAIZ / r).exists()]
    return (OK, f"{len(rels)} archivos presentes") if not faltan else (MAL, f"faltan {faltan} ({quien})")


def chk_ruta():
    from logistpulse.io_datos import cargar_planta
    from logistpulse.rutas import ruta_minima
    g, d = cargar_planta()
    ruta, costo = ruta_minima(g, d["origen"], d["destino"])
    return OK, f"{' → '.join(ruta)} = {costo:g} m"


def chk_reposicion():
    from logistpulse.inventario import EstadoSKU, sugerir
    s = sugerir(EstadoSKU("EJ", 18, 10, 5, 30, 50))
    return (OK, "ejemplo del enunciado = 27") if s.cantidad == 27 else (MAL, f"ejemplo da {s.cantidad} ≠ 27")


def chk_salidas_al_dia():
    from logistpulse import __main__ as demo
    import generar_docs as gd
    actual = leer("docs/generado/salidas_observadas.md")
    for nombre, func in demo.SECCIONES.items():
        buf = io.StringIO()
        with redirect_stdout(buf):
            print(func())
        if buf.getvalue().rstrip() not in actual:
            return PEND, f"salidas_observadas.md desactualizado en '{nombre}' (corre scripts/generar_docs.py)"
    malas = []
    for c in gd.CASOS:
        t = leer(f"docs/fichas/{c.id}.md")
        if gd.INICIO not in t:
            malas.append(f"{c.id} (sin marcas SALIDA)")
        elif gd.bloque_salida(c) not in t:
            malas.append(c.id)
    if malas:
        return PEND, f"salida observada desactualizada en fichas: {', '.join(malas)} (corre scripts/generar_docs.py)"
    return OK, "salidas observadas (generales y de las 10 fichas) = ejecución actual"


def chk_fichas():
    pend = []
    for p in sorted((RAIZ / "docs" / "fichas").glob("*.md")):
        t = p.read_text(encoding="utf-8")
        if re.search(r"^\s*(-\s*)?(\u270d|\[POR REDACTAR\])", t, re.M) or "- [ ]" in t:  # sección por redactar o casilla sin marcar
            pend.append(p.stem)
    if len(list((RAIZ / "docs" / "fichas").glob("*.md"))) != 10:
        return MAL, "no hay exactamente 10 fichas"
    return (OK, "10 fichas completas") if not pend else (PEND, f"fichas pendientes: {', '.join(pend)}")


def chk_grupo_b_sin_npc():
    sospechosas = []
    for p in sorted((RAIZ / "docs" / "fichas").glob("n*.md")):
        for linea in p.read_text(encoding="utf-8").splitlines():
            if re.search(r"\bes NP-complet", linea, re.I) and not re.search(r"\bno\b|sin afirmar|NO se", linea, re.I):
                sospechosas.append(f"{p.stem}: «{linea.strip()[:70]}»")
    return (OK, "ninguna ficha NP afirma NP-completitud") if not sospechosas else \
        (PEND, "revisar: " + " | ".join(sospechosas))


def chk_nota_parada():
    estado, detalle = doc_redactado("docs/fase_F_nota_parada.md", "Jessica")
    if estado != OK:
        return estado, detalle
    palabras = len(leer("docs/fase_F_nota_parada.md").split())
    return (OK, f"nota de {palabras} palabras") if palabras <= 750 else \
        (PEND, f"nota de {palabras} palabras: probablemente pasa de 1 página")


def chk_sprints():
    pend = [f"sprint_{i}" for i in (1, 2, 3) if "(completar" in leer(f"docs/sprints/sprint_{i}.md")]
    pend += [f"sprint_{i} sin roles rotativos" for i in (1, 2, 3) if "Roles de este sprint" not in leer(f"docs/sprints/sprint_{i}.md")]
    backlog = leer("docs/sprints/backlog.md")
    if backlog.count("C-") < 10:
        pend.append("backlog sin una unidad de trabajo por correo")
    if backlog.count("Por hacer") >= 15:
        pend.append("backlog sin actualizar (casi todo 'Por hacer')")
    return (OK, "backlog y 3 sprints documentados") if not pend else (PEND, f"pendiente: {', '.join(pend)} (Jessica)")


ETAPAS_EVIDENCIA = ("s1", "s2", "s3", "final")
NOMBRE_EVIDENCIA = re.compile(r"(s[123]|final)_[A-Za-z0-9_\-]+\.(png|jpe?g)", re.I)


def chk_evidencias():
    """Capturas de gestión en docs/evidencias/: una o más por etapa, con nombres sin espacios."""
    carpeta = RAIZ / "docs" / "evidencias"
    imgs = sorted(p.name for p in carpeta.iterdir()
                  if p.suffix.lower() in (".png", ".jpg", ".jpeg")) if carpeta.exists() else []
    malos = [n for n in imgs if not NOMBRE_EVIDENCIA.fullmatch(n)]
    if malos:
        return PEND, ("renombrar con prefijo s1_/s2_/s3_/final_ y sin espacios ni tildes: " + ", ".join(malos))
    faltan = [e for e in ETAPAS_EVIDENCIA if not any(n.lower().startswith(e + "_") for n in imgs)]
    if faltan:
        return PEND, (f"{len(imgs)} capturas en docs/evidencias; faltan las de: {', '.join(faltan)} "
                      "(lista y momento de cada una: docs/EMPIEZA_AQUI.md, sección 8)")
    return OK, f"{len(imgs)} capturas de gestión (s1, s2, s3 y final)"


def chk_git():
    if not (RAIZ / ".git").exists() or shutil.which("git") is None:
        return PEND, "todavía no es un repositorio Git (Jessica: ver equipo/GUIA_CODESPACES.md, paso 1)"

    def git(*args):
        return subprocess.run(["git", "-C", str(RAIZ), *args], capture_output=True, text=True).stdout.strip()
    commits = len(git("log", "--oneline").splitlines())
    autores = set(git("log", "--format=%an").splitlines())
    tags = git("tag").splitlines()
    falta = []
    if commits < 6:
        falta.append(f"solo {commits} commits")
    if len(autores) < 3:
        falta.append(f"{len(autores)} autor(es) en el historial (deben aparecer los 3)")
    if "v1.0" not in tags:
        falta.append("falta el tag v1.0")
    if shutil.which("gh"):  # visibilidad en GitHub (si el repo ya tiene remoto)
        vis = subprocess.run(["gh", "repo", "view", "--json", "visibility", "-q", ".visibility"],
                             cwd=RAIZ, capture_output=True, text=True).stdout.strip()
        if vis == "PRIVATE":
            falta.append("el repo es PRIVADO: antes de entregar, hazlo público o invita al profesor")
    detalle = f"{commits} commits · autores: {', '.join(sorted(autores)) or '—'} · tags: {', '.join(tags) or '—'}"
    return (OK, detalle) if not falta else (PEND, detalle + " → " + "; ".join(falta))


EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50\u25B6\u2139]")
ENTREGABLES = ["README.md", "docs/MATRIZ_TRAZABILIDAD.md", "docs/DECISIONES_Y_HALLAZGOS.md", "docs/conclusiones.md",
               "docs/presentacion_guion.md", "docs/fase_A_automatas.md", "docs/fase_B_rutas.md",
               "docs/fase_C_fefo_reposicion.md", "docs/fase_E_implementacion.md", "docs/fase_F_nota_parada.md",
               "docs/EMPIEZA_AQUI.md", "docs/evidencias/LEEME.md", "docs/QUE_PIDE_CADA_CORREO.md"]


def chk_sin_emojis():
    """Los documentos que se entregan no llevan emojis."""
    rutas = ENTREGABLES + [str(p.relative_to(RAIZ)) for p in sorted((RAIZ / "docs" / "fichas").glob("*.md"))] \
        + [str(p.relative_to(RAIZ)) for p in sorted((RAIZ / "docs" / "sprints").glob("*.md"))]
    con = []
    for rel in rutas:
        encontrados = set(EMOJI.findall(leer(rel)))
        if encontrados:
            con.append(f"{rel} ({' '.join(sorted(encontrados))})")
    return (OK, "documentos entregables sin emojis") if not con else (PEND, "quitar emojis en: " + "; ".join(con))


def pdf_en_release(tag: str = "v1.0") -> str:
    """Nombre del PDF adjunto al release (gh en el Codespace); "" si no hay gh, red o release."""
    if shutil.which("gh") is None:
        return ""
    try:
        r = subprocess.run(["gh", "release", "view", tag, "--json", "assets", "-q", ".assets[].name"],
                           cwd=RAIZ, capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return next((n for n in r.stdout.split() if n.lower().endswith(".pdf")), "") if r.returncode == 0 else ""


def chk_informe():
    """El PDF no se versiona (*.pdf está en .gitignore): vale el archivo local o el adjunto del release."""
    pdfs = sorted(p for p in RAIZ.rglob("*.pdf") if ".git" not in p.parts)
    if pdfs:
        return OK, "informe: " + ", ".join(str(p.relative_to(RAIZ)) for p in pdfs) + " (fuera de git: va en el release y en el aula)"
    adjunto = pdf_en_release()
    if adjunto:
        return OK, f"informe: {adjunto} adjunto al release v1.0"
    if (RAIZ / "docs" / "generado" / "INFORME.md").exists():
        return PEND, "hay borrador (docs/generado/INFORME.docx); falta exportarlo a PDF con Word como docs/INFORME_Deber2_LOGISTPULSE.pdf y adjuntarlo al release v1.0"
    return PEND, "no hay informe: corre scripts/armar_informe.py y exporta a PDF (Jessica)"


def chk_declaracion_ia():
    return (PEND, "README: falta completar la declaración de uso de IA") if "(Completar" in leer("README.md") else \
        (OK, "declaración de uso de IA completa")


def chk_presentacion():
    t = leer("docs/presentacion_guion.md")
    return (PEND, "guion de la presentación sin los aportes de cada integrante") if "Cada integrante pega aquí" in t else \
        (OK, "guion de la presentación completo")


CRITERIOS = [
    ("Autómatas y secuencias", "2,0", [
        ("Suite completa de pruebas", chk_pruebas),
        (".jff coherentes", chk_jff),
        ("Diagramas de estados", lambda: chk_archivos([f"docs/diagramas/afd_{k}.png" for k in ("pedido", "reserva", "orden_compra")], "generar_diagramas")),
        ("Capturas JFLAP", chk_capturas),
        ("Redacción Fase A", lambda: doc_redactado("docs/fase_A_automatas.md", "Camila")),
    ]),
    ("Grafo y búsqueda de rutas", "1,5", [
        ("Ruta calculada", chk_ruta),
        ("Diagrama de la planta", lambda: chk_archivos(["docs/diagramas/planta_ruta.png", "data/planta.json"], "Luis")),
        ("Redacción Fase B", lambda: doc_redactado("docs/fase_B_rutas.md", "Luis")),
    ]),
    ("FEFO y reposición", "1,5", [
        ("Regla de reposición", chk_reposicion),
        ("Redacción Fase C", lambda: doc_redactado("docs/fase_C_fefo_reposicion.md", "Luis")),
    ]),
    ("Decidibilidad y complejidad", "1,5", [
        ("Tabla resumen", lambda: chk_archivos(["docs/generado/tabla_resumen.md"], "generar_docs")),
        ("10 fichas", chk_fichas),
        ("Grupo B no afirma NPC", chk_grupo_b_sin_npc),
        ("Nota de la parada (1 pág.)", chk_nota_parada),
    ]),
    ("Implementación y pruebas", "1,5", [
        ("Salidas observadas al día", chk_salidas_al_dia),
        ("Pruebas de complejidad", lambda: chk_archivos(["tests/test_complejidad.py"], "—")),
        ("Redacción Fase E", lambda: doc_redactado("docs/fase_E_implementacion.md", "—")),
    ]),
    ("Gestión del proyecto y versiones", "1,0", [
        ("Backlog y sprints", chk_sprints),
        ("Historial Git y release", chk_git),
        ("Capturas de gestión", chk_evidencias),
    ]),
    ("Comunicación y reflexión", "1,0", [
        ("Informe PDF", chk_informe),
        ("Supuestos, límites y conclusiones", lambda: doc_redactado("docs/conclusiones.md", "Jessica")),
        ("Declaración de uso de IA", chk_declaracion_ia),
        ("Guion de la presentación", chk_presentacion),
        ("Documentos sin emojis", chk_sin_emojis),
    ]),
]


def main() -> int:
    print("REVISIÓN DE ENTREGA · Deber 2 LOGISTPULSE\n")
    completos, hay_errores = 0, False
    for criterio, puntos, checks in CRITERIOS:
        resultados = []
        for nombre, f in checks:
            try:
                estado, detalle = f()
            except Exception as e:  # una comprobación rota no debe ocultar las demás
                estado, detalle = MAL, f"error al comprobar: {e}"
            resultados.append((nombre, estado, detalle))
        peor = MAL if any(r[1] == MAL for r in resultados) else PEND if any(r[1] == PEND for r in resultados) else OK
        completos += peor == OK
        hay_errores |= peor == MAL
        print(f"{peor} {criterio} ({puntos} pts)")
        for nombre, estado, detalle in resultados:
            print(f"     {estado} {nombre}: {detalle}")
    print(f"\nCriterios con toda la evidencia verificable lista: {completos}/{len(CRITERIOS)}")
    print("Recuerda: esto no evalúa la calidad de la redacción; usen la lista de docs/PLANTILLA_FICHA.md.")
    return 1 if hay_errores else 0


if __name__ == "__main__":
    raise SystemExit(main())
