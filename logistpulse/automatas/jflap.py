"""Exportar / importar autómatas en formato JFLAP (.jff, JFLAP 7.x, tipo 'fa').

Exportar desde Python garantiza que el .jff que se prueba en JFLAP es EXACTAMENTE
el mismo autómata que prueban los tests. Importar permite comprobarlo al revés:
tests/test_jflap.py lee cada .jff y verifica que acepte/rechace lo mismo.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Tuple, Union

from .afd import AFD


def a_jff(afd: AFD) -> str:
    ids = {q: i for i, q in enumerate(afd.estados)}
    lineas = [
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
        f"<!--Generado por logistpulse.automatas.jflap · {afd.nombre}. Abrir con JFLAP 7.x (Finite Automaton).-->",
        "<structure>",
        "\t<type>fa</type>",
        "\t<automaton>",
        "\t\t<!--Estados-->",
    ]
    for q in afd.estados:
        x, y = afd.posiciones.get(q, (80 + 140 * ids[q], 150))
        lineas.append(f'\t\t<state id="{ids[q]}" name="{_xml(q)}">')
        lineas.append(f"\t\t\t<x>{float(x)}</x>")
        lineas.append(f"\t\t\t<y>{float(y)}</y>")
        lineas.append(f"\t\t\t<label>q{ids[q]}</label>")
        if q == afd.inicial:
            lineas.append("\t\t\t<initial/>")
        if q in afd.finales:
            lineas.append("\t\t\t<final/>")
        lineas.append("\t\t</state>")
    lineas.append("\t\t<!--Transiciones (δ parcial: lo no declarado rechaza)-->")
    for (q, a), d in afd.delta.items():
        lineas += [
            "\t\t<transition>",
            f"\t\t\t<from>{ids[q]}</from>",
            f"\t\t\t<to>{ids[d]}</to>",
            f"\t\t\t<read>{_xml(a)}</read>",
            "\t\t</transition>",
        ]
    lineas += ["\t</automaton>", "</structure>", ""]
    return "\n".join(lineas)


def guardar_jff(afd: AFD, ruta: Union[str, Path]) -> Path:
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(a_jff(afd), encoding="utf-8")
    return ruta


def leer_jff(ruta: Union[str, Path], nombre: str = "", eventos: Dict[str, str] = None) -> AFD:
    """Construye un AFD a partir de un .jff. Valida que sea determinista."""
    raiz = ET.parse(str(ruta)).getroot()
    tipo = raiz.findtext("type")
    if tipo != "fa":
        raise ValueError(f"{ruta}: se esperaba <type>fa</type>, se encontró {tipo!r}")
    auto = raiz.find("automaton")
    if auto is None:
        raise ValueError(f"{ruta}: falta <automaton>")
    nombres: Dict[str, str] = {}
    posiciones: Dict[str, Tuple[float, float]] = {}
    inicial, finales = None, set()
    for st in auto.findall("state"):
        sid, nom = st.get("id"), st.get("name")
        nombres[sid] = nom
        posiciones[nom] = (float(st.findtext("x", "0")), float(st.findtext("y", "0")))
        if st.find("initial") is not None:
            if inicial is not None:
                raise ValueError(f"{ruta}: más de un estado inicial")
            inicial = nom
        if st.find("final") is not None:
            finales.add(nom)
    if inicial is None:
        raise ValueError(f"{ruta}: no hay estado inicial")
    delta: Dict[Tuple[str, str], str] = {}
    simbolos = set()
    for tr in auto.findall("transition"):
        o, d, a = nombres[tr.findtext("from")], nombres[tr.findtext("to")], tr.findtext("read") or ""
        if a == "":
            raise ValueError(f"{ruta}: transición λ desde {o}; un AFD no admite λ")
        if (o, a) in delta and delta[(o, a)] != d:
            raise ValueError(f"{ruta}: no determinista en δ({o},{a})")
        delta[(o, a)] = d
        simbolos.add(a)
    eventos = eventos or {}
    alfabeto = {s: eventos.get(s, s) for s in sorted(simbolos | set(eventos))}
    return AFD(
        nombre=nombre or Path(ruta).stem,
        estados=list(nombres.values()),
        alfabeto=alfabeto,
        inicial=inicial,
        finales=finales,
        delta=delta,
        posiciones=posiciones,
    )


def _xml(texto: str) -> str:
    return texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
