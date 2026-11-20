"""Capa de PRESENTACIÓN: arma texto para consola / Markdown. No calcula nada nuevo."""

from __future__ import annotations

from typing import Dict, List

from .automatas import AUTOMATAS, SECUENCIAS
from .inventario import ResultadoFEFO, Sugerencia
from .rutas import GrafoPonderado


def titulo(texto: str) -> str:
    return f"\n{'=' * 78}\n{texto}\n{'=' * 78}"


def reporte_automatas() -> str:
    out = []
    for clave, afd in AUTOMATAS.items():
        out.append(titulo(f"FASE A · Autómata {afd.nombre}"))
        out.append(afd.definicion_formal())
        out.append("")
        for cadena, esperado, explicacion in SECUENCIAS[clave]:
            r = afd.ejecutar(cadena)
            ok = "[OK]" if r.aceptada == esperado else "[NO COINCIDE]"
            eventos = " → ".join(afd.eventos(cadena)) if cadena else "ε"
            out.append(f"{ok} '{cadena or 'ε'}' [{eventos}] -> {'ACEPTA' if r.aceptada else 'RECHAZA'} · {r.motivo}")
            out.append(f"     {explicacion}")
    return "\n".join(out)


def reporte_ruta(g: GrafoPonderado, nombre_escenario: str, bloqueados: List[str], ruta, costo,
                 empates: List[List[str]], unidad: str = "m") -> str:
    bloq = ", ".join(bloqueados) if bloqueados else "ninguno"
    if ruta is None:
        return f"[{nombre_escenario}] bloqueados: {bloq} -> NO existe ruta (dist = ∞)"
    lineas = [f"[{nombre_escenario}] bloqueados: {bloq} -> {' → '.join(ruta)} = {costo:g} {unidad}"]
    if len(empates) > 1:
        lineas.append(f"     Empate: {len(empates)} rutas de costo {costo:g}: " + " | ".join(" → ".join(r) for r in empates))
    return "\n".join(lineas)


def reporte_fefo(r: ResultadoFEFO) -> str:
    plan = ", ".join(f"{c}:{q}" for c, q in r.plan) or "—"
    desc = "; ".join(f"{c} ({m})" for c, m in r.descartados) or "—"
    return (f"{r.sku} x{r.solicitado} -> {r.estado} · plan [{plan}] · reservado {r.reservado} · "
            f"pendiente {r.pendiente}\n     orden FEFO: {r.orden_considerado} · descartados: {desc}")


def tabla_reposicion(sugs: List[Sugerencia]) -> str:
    filas = ["| SKU | posición | mínimo | objetivo | ¿posición ≤ mínimo? | sugerencia |", "|---|---|---|---|---|---|"]
    for s in sugs:
        filas.append(f"| {s.sku} | {s.posicion} | {s.minimo} | {s.objetivo} | {'Sí' if s.posicion <= s.minimo else 'No'} | {s.cantidad} |")
    return "\n".join(filas)
