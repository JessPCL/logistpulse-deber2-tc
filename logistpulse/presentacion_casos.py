"""Capa de PRESENTACIÓN de los 10 casos: recibe los datos ya leídos
(io_datos.cargar_casos) y los resultados de los algoritmos, y arma el texto.
Cada salida empieza con la RESPUESTA AL CORREO (lo que pide el remitente) y
sigue con la evidencia técnica (certificado, verificador, conteos, etc.).
"""

from __future__ import annotations

import math
from typing import Any, Callable, Dict, List

from .casos import (c1_sat, c2_tsp_decision, c3_vertex_cover, n1_isomorfismo, n2_factor_rango,
                    n3_log_discreto, n4_automorfismo, p1_alcanzabilidad, p2_ruta_minima, p3_flujo_maximo)
from .conteo import Contador

Inst = Dict[str, Any]


def tabla_bfs(traza: List[dict], inicio: str) -> str:
    filas = ["| Paso | Sale de la cola | Entran (se registra padre) | Cola después |", "|---|---|---|---|",
             f"| INICIO | — | {inicio} | {inicio} |"]
    for i, t in enumerate(traza, 1):
        entran = "**¡destino!**" if t["destino"] else (", ".join(t["entran"]) or "—")
        filas.append(f"| {i} | {t['sale']} | {entran} | {', '.join(t['cola']) or '∅'} |")
    return "\n".join(filas)


def demo_p1(inst: Inst) -> str:
    red, o, d = inst["red"], inst["origen"], inst["destino"]
    traza: List[dict] = []
    ruta = p1_alcanzabilidad.resolver(red, o, d, traza=traza)
    sin = p1_alcanzabilidad.resolver(inst["red_con_cierre"], o, d)
    cierre = ", ".join(f"{u}→{v}" for u, v in inst["cierre"])
    return (
        f"RESPUESTA AL CORREO: Sí, hoy existe ruta {o} → {d}: {' → '.join(ruta)} ({len(ruta) - 1} tramos).\n"
        f"Si se cierra {cierre}: {'Sí' if sin else 'No'} existe ruta (BFS agotó la cola).\n"
        f"Verificar camino: {p1_alcanzabilidad.verificar_camino(red, ruta, o, d)}\n"
        f"BFS por niveles:\n{tabla_bfs(traza, o)}"
    )


def demo_p2(inst: Inst) -> str:
    g, o, d = inst["grafo"], inst["origen"], inst["destino"]
    dist, ruta, empates = p2_ruta_minima.resolver(g, o, d)
    neg = inst["contraejemplo_negativo"]
    d_mal = p2_ruta_minima.dijkstra_sin_precondicion(neg, "S")
    d_bien = p2_ruta_minima.bellman_ford(neg, "S")
    return (
        f"RESPUESTA AL CORREO: recorrido sugerido {' → '.join(ruta)}, tiempo total {dist[d]:g}. "
        f"El sistema debe conservar pred[v] (predecesor) de cada nodo para reconstruir la ruta.\n"
        f"dist desde {o}: {dist}\n"
        f"Rutas de costo mínimo (empate): {[' → '.join(r) for r in empates]}\n"
        f"Versión de decisión: ¿ruta con costo ≤ 8? {p2_ruta_minima.decidir(g, o, d, 8)} · "
        f"≤ 7? {p2_ruta_minima.decidir(g, o, d, 7)}\n"
        f"Peso negativo (S→A 2, S→B 3, B→A −2, A→C 1): Dijkstra da C={d_mal['C']:g}, "
        f"Bellman–Ford da C={d_bien['C']:g}  ⇒ Dijkstra falla"
    )


def demo_p3(inst: Inst) -> str:
    cap, s, t = inst["capacidades"], inst["s"], inst["t"]
    cont = Contador()
    valor, flujo, lado_s, registro = p3_flujo_maximo.edmonds_karp(cap, s, t, contar=cont)
    V = len({*cap, *[v for vs in cap.values() for v in vs]})
    E = sum(len(vs) for vs in cap.values())
    lineas = [f"RESPUESTA AL CORREO: pueden llegar como máximo {valor} camiones/día de {s} a {t} "
              f"(la salida de {s} suma {sum(cap[s].values())}, pero el cuello de botella deja pasar {valor}).",
              "Registro de actualización de tramos (usado / disponible):"]
    for r in registro:
        lineas.append(f"  Aumento {r['iteracion']}: {' → '.join(r['camino'])} · cuello {r['cuello']} · total {r['total']}")
        for tr in r["tramos"]:
            lineas.append(f"      {tr['accion']:8} {tr['tramo']:22} usado {tr['usado']}/{tr['capacidad']} · disponible {tr['disponible']}")
    lineas += [
        f"Flujo final por tramo: {flujo}",
        f"Verificador (capacidad + conservación) -> valor {p3_flujo_maximo.verificar_flujo(cap, flujo, s, t)}",
        f"Corte mínimo S = {sorted(lado_s)} · capacidad = {p3_flujo_maximo.capacidad_corte(cap, lado_s)} = flujo ⇒ óptimo",
        f"Versión de decisión: ¿≥ {valor}? {p3_flujo_maximo.decidir(cap, s, t, valor)} · "
        f"¿≥ {valor + 1}? {p3_flujo_maximo.decidir(cap, s, t, valor + 1)}",
        f"Trabajo realizado: {cont['aumento']} aumentos (cota V·E = {V * E}) y {cont['arista']} aristas residuales "
        f"examinadas (cota (aumentos+1)·2E = {(cont['aumento'] + 1) * 2 * E}); V = {V}, E = {E}",
    ]
    return "\n".join(lineas)


def demo_n1(inst: Inst) -> str:
    A, B = inst["A"], inst["B"]
    cont = Contador()
    pi = n1_isomorfismo.resolver(A, B, contar=cont)
    return (
        f"RESPUESTA AL CORREO: {'Sí' if pi else 'No'}, las dos redes tienen la misma estructura; "
        f"correspondencia (certificado) π = {pi}  (nodo i de A ↦ nodo π(i) de B).\n"
        f"Verificador(π) = {n1_isomorfismo.verificar(A, B, pi)} · Verificador(identidad) = {n1_isomorfismo.verificar(A, B, (0, 1, 2))}\n"
        f"Búsqueda: {cont['permutacion']} permutaciones probadas (de {len(A)}! = {math.factorial(len(A))} posibles)\n"
        f"C6 vs dos triángulos (mismos grados, no isomorfos): "
        f"{n1_isomorfismo.resolver(n1_isomorfismo.ciclo(6), n1_isomorfismo.union_de_ciclos(3, 3))}"
    )


def demo_n2(inst: Inst) -> str:
    N, B = inst["N"], inst["B"]
    cb, cv = Contador(), Contador()
    d = n2_factor_rango.resolver(N, B, contar=cb)
    ok = n2_factor_rango.verificar(N, B, d, contar=cv)
    return (
        (f"RESPUESTA AL CORREO: Sí, N tiene un divisor en el rango: d = {d} (2 ≤ {d} ≤ {B} y {N} mod {d} = 0).\n"
         if d else f"RESPUESTA AL CORREO: No, N no tiene divisores entre 2 y {B}.\n") +
        f"Entrada en binario: N = {inst['N_binario']}₂ ({N.bit_length()} bits), B = {inst['B_binario']}₂ ({B.bit_length()} bits)\n"
        f"BUSCAR: {cb['division']} divisiones (crece con el VALOR de B, hasta B−1) · "
        f"VERIFICAR: {cv['division']} división · verificar(d) = {ok}\n"
        f"Con B = 6 -> {n2_factor_rango.resolver(N, 6)} (7 queda fuera del rango) · "
        f"verificar({N}, {B}, 13) = {n2_factor_rango.verificar(N, B, 13)}"
    )


def demo_n3(inst: Inst) -> str:
    p, g, h, B = inst["p"], inst["g"], inst["h"], inst["B"]
    cl, cb, cv = Contador(), Contador(), Contador()
    x = n3_log_discreto.resolver(p, g, h, B, contar=cl)
    xb = n3_log_discreto.baby_step_giant_step(p, g, h, B, contar=cb)
    ok = n3_log_discreto.verificar(p, g, h, B, x, contar=cv)
    return (
        (f"RESPUESTA AL CORREO: Sí, existe un exponente permitido: x = {x} ({g}^{x} ≡ {h} mod {p}, 0 ≤ {x} ≤ {B}).\n"
         if x is not None else f"RESPUESTA AL CORREO: No existe x en [0, {B}] con {g}^x ≡ {h} (mod {p}).\n") +
        f"BUSCAR lineal: {cl['multiplicacion']} multiplicaciones · BSGS: x = {xb}, {cb['multiplicacion']} multiplicaciones\n"
        f"VERIFICAR (cuadrado y multiplicación): {cv['multiplicacion']} multiplicaciones · verificar(x) = {ok} · "
        f"verificar(x=5) = {n3_log_discreto.verificar(p, g, h, B, 5)}\n"
        f"Con B = 5 -> {n3_log_discreto.resolver(p, g, h, 5)} (el único x ≤ 21 con {g}^x ≡ {h} es 6)"
    )


def demo_n4(inst: Inst) -> str:
    G, asim = inst["G"], inst["asimetrico_6"]
    pi, k = n4_automorfismo.resolver(G)
    pi2, k2 = n4_automorfismo.resolver(asim)
    return (
        (f"RESPUESTA AL CORREO: Sí, el plano tiene una simetría real: π = {pi} "
         f"(reasignación distinta de la identidad que mantiene todas las adyacencias).\n"
         if pi else "RESPUESTA AL CORREO: No hay simetría: se agotaron todas las permutaciones.\n") +
        f"Verificar(π) = {n4_automorfismo.verificar(G, pi)} · verificar(identidad) = {n4_automorfismo.verificar(G, (0, 1, 2))} "
        f"· hallado tras {k} permutaciones\n"
        f"Grafo asimétrico de 6 vértices: {pi2} -> 'No' tras AGOTAR {k2} = 6! permutaciones"
    )


def respuesta_p1(conexiones, origen: str, destino: str) -> str:
    """Respuesta de p1 para CUALQUIER lista de conexiones (la pide el correo)."""
    red = p1_alcanzabilidad.red_desde_conexiones(conexiones)
    if origen not in red or destino not in red:
        faltan = [x for x in (origen, destino) if x not in red]
        return f"No: {', '.join(faltan)} no aparece en ninguna conexión."
    camino = p1_alcanzabilidad.resolver(red, origen, destino)
    if camino is None:
        return f"No: no existe ruta {origen} → {destino} (BFS visitó todo lo alcanzable y no llegó)."
    return (f"Sí: existe ruta {origen} → {destino}: {' → '.join(camino)} ({len(camino) - 1} tramos) · "
            f"verificar camino = {p1_alcanzabilidad.verificar_camino(red, camino, origen, destino)}")


def demo_c1(inst: Inst) -> str:
    cl, n = inst["clausulas"], inst["n"]
    c_dpll, c_fb = Contador(), Contador()
    a = c1_sat.dpll(cl, n, contar=c_dpll)  # algoritmo seleccionado
    a_fb = c1_sat.fuerza_bruta(cl, n, contar=c_fb)  # referencia independiente
    a2 = c1_sat.dos_sat(cl, n)
    t, u = inst["tres_cnf_satisfacible"], inst["tres_cnf_insatisfacible"]
    a3 = c1_sat.dpll(t["clausulas"], t["n"])
    texto = ", ".join(f"x{i} = {'verdadero' if v else 'falso'}" for i, v in sorted(a.items())) if a else ""

    def lit(l):
        return f"x{abs(l)}" if l > 0 else f"¬x{abs(l)}"

    def regla(c):
        return "(" + " ∨ ".join(lit(l) for l in c) + ")"

    detalle = "".join(
        f"\n  Regla {i} {regla(c)}: " + (f"se cumple porque {lit(l)} es verdadero" if l is not None else "NO se cumple")
        for i, (c, l) in enumerate(zip(cl, c1_sat.verificar_detalle(cl, a)), 1)) if a else ""
    return (
        (f"RESPUESTA AL CORREO: Sí, hay un horario candidato que cumple todas las reglas: {texto} "
         f"(DPLL; comprobación independiente: verificar = {c1_sat.verificar(cl, a)}).\n"
         f"Comprobación cláusula por cláusula:{detalle}\n"
         if a else "RESPUESTA AL CORREO: No existe una asignación que cumpla todas las reglas; "
         "el equipo deberá renegociar la ventana de despacho.\n") +
        f"DPLL: {c_dpll['nodo']} nodo(s) del árbol · fuerza bruta (referencia): {a_fb}, probó {c_fb['asignacion']} "
        f"de 2^{n} = {2 ** n} asignaciones (crece como 2ⁿ)\n"
        f"La instancia es 2-CNF = {c1_sat.es_2cnf(cl)} ⇒ 2-SAT lineal -> {a2} · verificar = {c1_sat.verificar(cl, a2)}\n"
        f"3-CNF satisfacible (extra): DPLL -> {a3} · verificar = {c1_sat.verificar(t['clausulas'], a3)}\n"
        f"3-CNF con las 8 cláusulas (extra): DPLL -> {c1_sat.dpll(u['clausulas'], u['n'])} · "
        f"fuerza bruta -> {c1_sat.fuerza_bruta(u['clausulas'], u['n'])}"
    )


def demo_c2(inst: Inst) -> str:
    D, L, centros = inst["D"], inst["L"], inst["centros"]
    r = c2_tsp_decision.decidir(D, L)
    if r is None:
        return f"RESPUESTA AL CORREO: No existe recorrido que visite todos los centros y regrese con ≤ {L} km."
    tour = r[0]
    hk_t, hk_c = c2_tsp_decision.held_karp(D)
    D4, L4 = c2_tsp_decision.reducir_ham_a_tsp(4, [(0, 1), (1, 2), (2, 3), (3, 0)])
    Dst, Lst = c2_tsp_decision.reducir_ham_a_tsp(4, [(0, 1), (0, 2), (0, 3)])
    trampa = inst["trampa_heuristica"]
    nn_t, nn_c = c2_tsp_decision.vecino_mas_cercano(trampa)
    op_t, op_c = c2_tsp_decision.held_karp(trampa)
    return (
        f"RESPUESTA AL CORREO: Sí, existe un recorrido dentro de L = {L} km: "
        f"{' → '.join(centros[i] for i in tour)} = {r[1]:g} km (verificar = {c2_tsp_decision.verificar(D, L, tour)}).\n"
        f"Decisión con L = 14: {'Sí' if c2_tsp_decision.decidir(D, 14) else 'No'} (el único tour, salvo sentido, cuesta 15)\n"
        f"Optimización (pregunta distinta, Held–Karp): {hk_t} = {hk_c:g}\n"
        f"Reducción HAM→TSP: C4 -> {c2_tsp_decision.decidir(D4, L4) is not None} · "
        f"estrella K1,3 -> {c2_tsp_decision.decidir(Dst, Lst) is not None}\n"
        f"Heurística vs exacto (4 centros): vecino más cercano {nn_t} = {nn_c:g} · Held–Karp {op_t} = {op_c:g}"
    )


def demo_c3(inst: Inst) -> str:
    ady, k = inst["ady"], inst["k"]
    S = c3_vertex_cover.ramificacion(ady, k)
    if S is None:
        return f"RESPUESTA AL CORREO: No, con k = {k} equipos de inspección no se pueden cubrir todos los corredores."
    est = c3_vertex_cover.estrella(5)
    G2, kvc = c3_vertex_cover.reducir_is_a_vc(ady, 2)
    return (
        f"RESPUESTA AL CORREO: Sí, basta con {len(S)} equipo(s) de inspección (k = {k}): selección {sorted(S)}; "
        f"cubre todos los corredores (verificar = {c3_vertex_cover.verificar(ady, k, S)}).\n"
        f"verificar({{'A'}}) = {c3_vertex_cover.verificar(ady, k, {'A'})} · con k = 0: {c3_vertex_cover.ramificacion(ady, 0)} (No)\n"
        f"Estrella de 5 hojas: óptimo = {c3_vertex_cover.minimo_por_subconjuntos(est)} · "
        f"2-aproximación = {sorted(c3_vertex_cover.aproximacion_2(est))} (tamaño 2 ≤ 2·1)\n"
        f"Reducción IS→VC: ¿IS de tamaño 2 en A-B-C? ⇔ ¿VC de tamaño {kvc}? -> "
        f"{c3_vertex_cover.ramificacion(G2, kvc) is not None}"
    )


DEMOS: Dict[str, Callable[[Inst], str]] = {
    "p1": demo_p1, "p2": demo_p2, "p3": demo_p3,
    "n1": demo_n1, "n2": demo_n2, "n3": demo_n3, "n4": demo_n4,
    "c1": demo_c1, "c2": demo_c2, "c3": demo_c3,
}
