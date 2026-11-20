"""Capa de LECTURA: carga y valida los JSON de data/. No contiene algoritmos."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

from .inventario import EstadoSKU, Lote
from .rutas import GrafoPonderado

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"


def _leer_json(ruta: Union[str, Path]) -> Dict[str, Any]:
    ruta = Path(ruta)
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo de datos: {ruta}")
    try:
        return json.loads(ruta.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"{ruta.name}: JSON mal formado ({e})") from e


def _requerir(d: Dict[str, Any], claves: Tuple[str, ...], contexto: str) -> None:
    faltan = [c for c in claves if c not in d]
    if faltan:
        raise ValueError(f"{contexto}: faltan campos {faltan}")


def cargar_planta(ruta: Union[str, Path] = DATA / "planta.json") -> Tuple[GrafoPonderado, Dict[str, Any]]:
    d = _leer_json(ruta)
    _requerir(d, ("dirigido", "vertices", "aristas", "origen", "destino"), "planta")
    g = GrafoPonderado(dirigido=bool(d["dirigido"]))
    for v, nombre in d["vertices"].items():
        g.agregar_vertice(v, nombre)
    for i, arista in enumerate(d["aristas"]):
        if not (isinstance(arista, list) and len(arista) == 3):
            raise ValueError(f"planta: arista #{i} debe ser [u, v, peso], recibido {arista!r}")
        u, v, w = arista
        for x in (u, v):
            if x not in d["vertices"]:
                raise ValueError(f"planta: la arista #{i} usa el vértice no declarado '{x}'")
        g.agregar_arista(u, v, w)
    return g, d


def _fecha(texto: str, contexto: str) -> date:
    try:
        return date.fromisoformat(texto)
    except (TypeError, ValueError) as e:
        raise ValueError(f"{contexto}: fecha inválida {texto!r} (use AAAA-MM-DD)") from e


def cargar_lotes(ruta: Union[str, Path] = DATA / "lotes_fefo.json") -> Tuple[List[Lote], date, List[Dict[str, Any]]]:
    d = _leer_json(ruta)
    _requerir(d, ("fecha_referencia", "lotes"), "lotes")
    ref = _fecha(d["fecha_referencia"], "fecha_referencia")
    lotes = []
    for i, l in enumerate(d["lotes"]):
        _requerir(l, ("codigo", "sku", "vencimiento", "disponible"), f"lote #{i}")
        lotes.append(Lote(l["codigo"], l["sku"], _fecha(l["vencimiento"], f"lote {l['codigo']}"), l["disponible"]))
    return lotes, ref, d.get("pedidos", [])


def cargar_skus(ruta: Union[str, Path] = DATA / "skus_reposicion.json") -> List[EstadoSKU]:
    d = _leer_json(ruta)
    _requerir(d, ("skus",), "reposición")
    out, vistos = [], set()
    for i, s in enumerate(d["skus"]):
        _requerir(s, ("sku", "disponible", "en_orden", "reservado", "minimo", "objetivo"), f"sku #{i}")
        if s["sku"] in vistos:
            raise ValueError(f"reposición: SKU repetido '{s['sku']}'")
        vistos.add(s["sku"])
        out.append(EstadoSKU(s["sku"], s["disponible"], s["en_orden"], s["reservado"], s["minimo"], s["objetivo"]))
    return out


# ----------------------------------------------------------------------------- 10 casos del simulador
def _matriz_desde_aristas(n: int, aristas) -> List[List[int]]:
    M = [[0] * n for _ in range(n)]
    for a, b in aristas:
        M[a][b] = M[b][a] = 1
    return M


def cargar_casos(ruta: Union[str, Path] = DATA / "casos_simulador.json") -> Dict[str, Dict[str, Any]]:
    """Lee data/casos_simulador.json y devuelve cada instancia ya validada y en la
    estructura que usa su algoritmo. Toda la LECTURA de datos de los casos pasa por aquí."""
    from .casos import (c1_sat, c2_tsp_decision, c3_vertex_cover, n1_isomorfismo, n2_factor_rango,
                        p1_alcanzabilidad, p2_ruta_minima, p3_flujo_maximo)

    d = _leer_json(ruta)
    faltan = [c for c in ("p1", "p2", "p3", "n1", "n2", "n3", "n4", "c1", "c2", "c3") if c not in d]
    if faltan:
        raise ValueError(f"casos: faltan los expedientes {faltan}")
    x = {k: v.get("extras", {}) for k, v in d.items() if isinstance(v, dict)}

    p1 = d["p1"]
    p2 = d["p2"]
    neg = {u: [tuple(e) for e in vs] for u, vs in x["p2"]["contraejemplo_peso_negativo"].items()}
    p3 = d["p3"]
    n1 = d["n1"]
    for nombre in ("A", "B"):
        n1_isomorfismo.validar_matriz(n1[nombre], nombre)
    asim = x["n4"]["asimetrico_6"]
    n4 = {"G": d["n4"]["G"], "asimetrico_6": _matriz_desde_aristas(asim["n"], asim["aristas"])}
    n1_isomorfismo.validar_matriz(n4["G"], "G")
    c1 = d["c1"]
    c1_sat.validar(c1["clausulas"], c1["n"])
    c2 = d["c2"]
    c2_tsp_decision.validar(c2["distancias"])
    if len(c2["centros"]) != len(c2["distancias"]):
        raise ValueError("c2: hay distinto número de centros que de filas en la matriz")

    return {
        "p1": {"red": p1_alcanzabilidad.red_desde_conexiones(p1["conexiones"]),
               "red_con_cierre": p1_alcanzabilidad.red_desde_conexiones(p1["conexiones"], x["p1"]["cierre_de_vias"]),
               "cierre": [tuple(c) for c in x["p1"]["cierre_de_vias"]],
               "conexiones": [tuple(c) for c in p1["conexiones"]],
               "origen": p1["origen"], "destino": p1["destino"]},
        "p2": {"grafo": p2_ruta_minima.grafo_desde_tramos(p2["tramos"]), "tramos": p2["tramos"],
               "origen": p2["origen"], "destino": p2["destino"], "contraejemplo_negativo": neg},
        "p3": {"capacidades": p3_flujo_maximo.capacidades_desde_tramos(p3["tramos"]),
               "s": p3["fuente"], "t": p3["sumidero"]},
        "n1": {"A": n1["A"], "B": n1["B"]},
        "n2": {"N": n2_factor_rango.desde_binario(d["n2"]["N_binario"]),
               "B": n2_factor_rango.desde_binario(d["n2"]["B_binario"]),
               "N_binario": d["n2"]["N_binario"], "B_binario": d["n2"]["B_binario"]},
        "n3": {k: d["n3"][k] for k in ("p", "g", "h", "B")},
        "n4": n4,
        "c1": {"n": c1["n"], "clausulas": c1["clausulas"],
               "tres_cnf_satisfacible": x["c1"]["tres_cnf_satisfacible"],
               "tres_cnf_insatisfacible": x["c1"]["tres_cnf_insatisfacible"]},
        "c2": {"centros": c2["centros"], "D": c2["distancias"], "L": c2["L"],
               "trampa_heuristica": x["c2"]["trampa_heuristica"]},
        "c3": {"ady": c3_vertex_cover.ady_desde_aristas(d["c3"]["aristas"]), "k": d["c3"]["k"],
               "aristas": [tuple(a) for a in d["c3"]["aristas"]]},
    }
