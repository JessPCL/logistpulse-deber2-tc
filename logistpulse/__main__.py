"""Demo completa:  python -m logistpulse   (o  python -m logistpulse casos)

Secciones: automatas | rutas | inventario | casos | todo (por defecto)
Correo p1 con tu propia lista de conexiones:  python -m logistpulse p1 ARCHIVO ORIGEN DESTINO
"""

from __future__ import annotations

import sys

from . import presentacion as pr
from .casos import CASOS
from .io_datos import cargar_casos, cargar_conexiones
from .presentacion_casos import DEMOS, respuesta_p1
from .inventario import emitir_orden, seleccionar_fefo, sugerencias, sugerir
from .io_datos import cargar_lotes, cargar_planta, cargar_skus
from .rutas import bfs_ruta, dijkstra, ruta_minima, todas_las_rutas_minimas


def seccion_automatas() -> str:
    return pr.reporte_automatas()


def seccion_rutas() -> str:
    g, d = cargar_planta()
    out = [pr.titulo("FASE B · Planta como grafo ponderado (Dijkstra)")]
    out.append(f"V = {g.num_vertices}, E = {g.num_aristas}, dirigido = {g.dirigido}, origen = {d['origen']}, destino = {d['destino']}")
    res = dijkstra(g, d["origen"], con_traza=True)
    out.append("Traza de Dijkstra (escenario base):")
    out += [f"   {t}" for t in res.traza]
    for esc in d["escenarios"]:
        ruta, costo = ruta_minima(g, d["origen"], d["destino"], esc["bloqueados"])
        empates = todas_las_rutas_minimas(g, d["origen"], d["destino"], esc["bloqueados"])
        out.append(pr.reporte_ruta(g, esc["nombre"], esc["bloqueados"], ruta, costo, empates, d.get("unidad", "m")))
    rb = bfs_ruta(g.como_lista_adyacencia(), d["origen"], d["destino"])
    out.append(f"BFS (ignora pesos): {' → '.join(rb)} = {len(rb) - 1} tramos, pero cuesta {g.costo_ruta(rb):g} m > 11 ⇒ "
               "con pesos hay que usar Dijkstra")
    return "\n".join(out)


def seccion_inventario() -> str:
    lotes, ref, pedidos = cargar_lotes()
    out = [pr.titulo(f"FASE C · FEFO (fecha de referencia {ref.isoformat()})")]
    for p in pedidos:
        out.append(pr.reporte_fefo(seleccionar_fefo(lotes, p["sku"], p["cantidad"], ref, p["politica"])))
    skus = cargar_skus()
    out.append(pr.titulo("FASE C · Reposición por punto de pedido"))
    out.append(pr.tabla_reposicion(list(sugerencias(skus))))
    ej = skus[0]
    s1 = sugerir(ej)
    s2 = sugerir(emitir_orden(ej, s1.cantidad))
    out.append(f"\nAnti-duplicado: {ej.sku} sugiere {s1.cantidad}; tras emitir esa orden (en_orden += {s1.cantidad}) "
               f"la posición pasa a {s2.posicion} > mínimo ⇒ nueva sugerencia = {s2.cantidad}")
    return "\n".join(out)


def seccion_casos() -> str:
    datos = cargar_casos()  # lectura
    out = []
    for c in CASOS:
        out.append(pr.titulo(f"FASE D · {c.id.upper()} · {c.clase} · {c.asunto}"))
        out.append(DEMOS[c.id](datos[c.id]))  # procesamiento + presentación
    return "\n".join(out)


SECCIONES = {
    "automatas": seccion_automatas,
    "rutas": seccion_rutas,
    "inventario": seccion_inventario,
    "casos": seccion_casos,
}


def main_p1(argv) -> int:
    """python -m logistpulse p1 ARCHIVO ORIGEN DESTINO   (correo p1: ejecutar con una lista de conexiones)"""
    if len(argv) != 3:
        print("Uso: python -m logistpulse p1 ARCHIVO_DE_CONEXIONES ORIGEN DESTINO\n"
              "     ejemplo: python -m logistpulse p1 data/ejemplos/p1_con_ruta.txt Durán Norte")
        return 2
    archivo, origen, destino = argv
    try:
        print(respuesta_p1(cargar_conexiones(archivo), origen, destino))
    except (OSError, ValueError) as e:
        print(f"Error: {e}")
        return 2
    return 0


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["p1"]:
        return main_p1(argv[1:])
    elegidas = argv or list(SECCIONES)
    for nombre in elegidas:
        if nombre not in SECCIONES:
            print(f"Sección desconocida '{nombre}'. Opciones: {', '.join(SECCIONES)}")
            return 2
        print(SECCIONES[nombre]())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
