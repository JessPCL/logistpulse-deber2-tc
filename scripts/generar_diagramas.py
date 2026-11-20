"""Genera los diagramas (DOT -> PNG/SVG) de los autómatas y de la planta con la ruta.

Requiere Graphviz (comando `dot`). En Colab ya viene instalado; en Windows/Mac:
https://graphviz.org/download/. Si no está, se escriben solo los .dot.

Uso:  python scripts/generar_diagramas.py
"""

import shutil
import subprocess

import _bootstrap  # noqa: F401
from _bootstrap import RAIZ

from logistpulse.automatas import AUTOMATAS
from logistpulse.io_datos import cargar_casos, cargar_planta
from logistpulse.rutas import ruta_minima, todas_las_rutas_minimas

SALIDA = RAIZ / "docs" / "diagramas"
AZUL, VERDE, ROJO = "#1f6eb5", "#2e8b57", "#c0392b"
EXITO = {"Entregado", "Consumida", "Recibida"}
CIERRE_NEGATIVO = {"Cancelado", "Rechazada", "Liberada", "Expirada"}


def dot_automata(afd) -> str:
    l = [f'digraph "{afd.nombre}" {{', "  rankdir=LR; fontname=Helvetica; labelloc=t;",
         f'  label="AFD · {afd.nombre}  (F = doble círculo; transiciones no dibujadas → sumidero ERROR)";',
         '  node [fontname=Helvetica, style=filled, fillcolor="#eef4fc", color="#7f9cc4"];',
         '  edge [fontname=Helvetica, fontsize=11, color="#4b5d78"];',
         "  __inicio [shape=point, width=0.12, label=\"\"];"]
    for q in afd.estados:
        forma = "doublecircle" if q in afd.finales else "circle"
        relleno = "#e3f4ea" if q in EXITO else ("#fbeaea" if q in CIERRE_NEGATIVO else "#eef4fc")
        l.append(f'  "{q}" [shape={forma}, fillcolor="{relleno}"];')
    l.append(f'  __inicio -> "{afd.inicial}";')
    agrupadas = {}
    for (q, a), d in afd.delta.items():
        agrupadas.setdefault((q, d), []).append(f"{a}: {afd.alfabeto[a]}")
    for (q, d), etiquetas in agrupadas.items():
        l.append(f'  "{q}" -> "{d}" [label="{chr(10).join(etiquetas)}"];'.replace("\n", "\\n"))
    l.append("}")
    return "\n".join(l)


def dot_planta() -> str:
    g, d = cargar_planta()
    ruta, costo = ruta_minima(g, d["origen"], d["destino"])
    empates = todas_las_rutas_minimas(g, d["origen"], d["destino"])
    en_ruta = {frozenset(p) for p in zip(ruta, ruta[1:])}
    en_empate = {frozenset(p) for r in empates for p in zip(r, r[1:])} - en_ruta
    pos = {"R": (0, 1), "A": (1.8, 2), "B": (1.8, 0), "P": (3.6, 1), "C": (3.6, -1), "E": (5.4, 1), "D": (7.6, 1)}
    l = ["graph planta {", "  layout=neato; overlap=false; splines=true; fontname=Helvetica; labelloc=t;",
         f'  label="Planta LOGISTPULSE · Dijkstra {d["origen"]}→{d["destino"]}: {" → ".join(ruta)} = {costo:g} m '
         f'(azul) · ruta empatada de la Figura 5 (naranja punteado)";',
         '  node [shape=box, style="rounded,filled", fillcolor="#eef4fc", color="#7f9cc4", fontname=Helvetica];',
         '  edge [fontname=Helvetica, color="#9aa7b8", penwidth=1.5];']
    for v in g.vertices:
        x, y = pos.get(v, (0, 0))
        color = "#e3f4ea" if v == d["origen"] else ("#fdebd7" if v == d["destino"] else "#eef4fc")
        l.append(f'  "{v}" [label="{v}\\n{g.nombres.get(v, "")}", pos="{x},{y}!", fillcolor="{color}"];')
    for u, v, w in g.aristas():
        par = frozenset((u, v))
        estilo = ""
        if par in en_ruta:
            estilo = f', color="{AZUL}", penwidth=4'
        elif par in en_empate:
            estilo = ', color="#e67e22", penwidth=3, style=dashed'
        l.append(f'  "{u}" -- "{v}" [label="{w:g}"{estilo}];')
    l.append("}")
    return "\n".join(l)


def dot_casos():
    """Grafos de los expedientes con red explícita (p1, p2, p3, c3), para el informe."""
    d = cargar_casos()
    base = ['  rankdir=LR; fontname=Helvetica;',
            '  node [shape=ellipse, style=filled, fillcolor="#eef4fc", color="#7f9cc4", fontname=Helvetica];',
            '  edge [fontname=Helvetica, color="#4b5d78"];']
    p1 = ["digraph p1 {", *base, '  label="p1 · tramos activos (dirigido)"; labelloc=t;']
    p1 += [f'  "{u}" -> "{v}"{" [color=\"%s\", penwidth=3]" % AZUL if (u, v) in {("Durán", "Quito"), ("Quito", "Norte")} else ""};'
           for u, v in d["p1"]["conexiones"]]
    p2 = ["digraph p2 {", *base, '  label="p2 · tiempos de viaje (dirigido)"; labelloc=t;']
    p2 += [f'  "{u}" -> "{v}" [label="{w}"];' for u, v, w in d["p2"]["tramos"]]
    p3 = ["digraph p3 {", *base, '  label="p3 · capacidades (camiones/día)"; labelloc=t;']
    p3 += [f'  "{u}" -> "{v}" [label="{c}"];' for u, vs in d["p3"]["capacidades"].items() for v, c in vs.items()]
    c3 = ["graph c3 {", *[b.replace("rankdir=LR; ", "rankdir=LR; ") for b in base], '  label="c3 · corredores entre zonas"; labelloc=t;']
    c3 += [f'  "{u}" -- "{v}";' for u, v in d["c3"]["aristas"]]
    return {"caso_p1": "\n".join(p1 + ["}"]), "caso_p2": "\n".join(p2 + ["}"]),
            "caso_p3": "\n".join(p3 + ["}"]), "caso_c3": "\n".join(c3 + ["}"])}


def renderizar(nombre: str, fuente: str, motor: str = "dot") -> None:
    SALIDA.mkdir(parents=True, exist_ok=True)
    ruta_dot = SALIDA / f"{nombre}.dot"
    ruta_dot.write_text(fuente, encoding="utf-8")
    if shutil.which(motor) is None:
        print(f"AVISO Graphviz no instalado: solo se escribió {ruta_dot.relative_to(RAIZ)}")
        return
    for fmt in ("png", "svg"):
        subprocess.run([motor, f"-T{fmt}", "-Gdpi=150" if fmt == "png" else "-Gdpi=72",
                        str(ruta_dot), "-o", str(SALIDA / f"{nombre}.{fmt}")], check=True)
    print(f"OK docs/diagramas/{nombre}.png / .svg")


def main() -> None:
    for clave, afd in AUTOMATAS.items():
        renderizar(f"afd_{clave}", dot_automata(afd))
    renderizar("planta_ruta", dot_planta(), motor="neato")
    for nombre, fuente in dot_casos().items():
        renderizar(nombre, fuente)


if __name__ == "__main__":
    main()
