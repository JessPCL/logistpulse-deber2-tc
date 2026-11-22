"""Registro (metadatos) de los 10 correos del simulador.

FUENTE ÚNICA de la tabla resumen y del esqueleto de las fichas
(scripts/generar_docs.py). Si el equipo cambia una clasificación o una cota,
la cambia AQUÍ y regenera. Capas: datos en data/casos_simulador.json (lectura:
io_datos.cargar_casos), algoritmos en estos módulos (procesamiento) y textos de
salida en logistpulse/presentacion_casos.py (presentación).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from . import (
    c1_sat, c2_tsp_decision, c3_vertex_cover,
    n1_isomorfismo, n2_factor_rango, n3_log_discreto, n4_automorfismo,
    p1_alcanzabilidad, p2_ruta_minima, p3_flujo_maximo,
)


@dataclass(frozen=True)
class Caso:
    id: str
    grupo: str              # A = P · B = NP (sin afirmar NPC) · C = NP-completo
    clase: str
    asunto: str
    remitente: str
    pregunta: str           # versión de decisión (Sí/No)
    entrada: str
    salida: str
    version: str            # decisión / optimización analizada
    evidencia: str          # algoritmo polinómico | certificado+verificador | reducción
    certificado: str
    reduccion: str
    algoritmo: str
    tipo: str               # exacto / aproximado / heurístico
    tiempo: str
    espacio: str
    variables: str
    decidible: str
    modulo: str
    observaciones: str


CASOS: List[Caso] = [
    Caso(
        "p1", "A", "P", "¿Puede llegar el envío a la zona Norte?", "Daniela Paredes · Planificación",
        "¿Existe un camino dirigido de Durán a Norte usando solo tramos activos?",
        "Grafo dirigido G=(V,E) de tramos activos, origen s, destino t.",
        "Sí/No (+ camino como evidencia).",
        "Decisión (alcanzabilidad).",
        "Algoritmo polinómico conocido: BFS.",
        "Un camino s⇝t (verificable en O(|camino|)), aunque no hace falta: BFS decide en tiempo polinómico.",
        "—",
        "BFS", "Exacto",
        "O(V + E)", "O(V)", "V = sitios, E = tramos activos",
        "Sí: cada vértice entra a la cola una vez; termina al hallar t o vaciar la cola.",
        "logistpulse/casos/p1_alcanzabilidad.py",
        "Con la red del portal: Sí (Durán→Quito→Norte, 2 tramos). Si se cierra Quito→Norte: No.",
    ),
    Caso(
        "p2", "A", "P", "Ruta mínima entre centros de distribución", "Marco Cedeño · Transporte",
        "¿Existe ruta CD Quito ⇝ CD Guayaquil con tiempo total ≤ K?",
        "Grafo dirigido con tiempos w(e) ≥ 0, origen s, destino t (y K en la versión de decisión).",
        "Tiempo mínimo a cada nodo + ruta reconstruida con predecesores.",
        "Optimización (camino mínimo); decisión asociada con cota K.",
        "Algoritmo polinómico conocido: Dijkstra (requiere pesos ≥ 0).",
        "—", "—",
        "Dijkstra (heap binario)", "Exacto",
        "O((V + E) log V)", "O(V + E)", "V = centros, E = conexiones",
        "Sí: cada vértice se finaliza una vez; ≤ E inserciones en el heap.",
        "logistpulse/casos/p2_ruta_minima.py",
        "Costo 8 con EMPATE: Quito→Latacunga→Guayaquil y Quito→Ambato→Guayaquil. Con pesos negativos "
        "Dijkstra falla (contraejemplo incluido); usar Bellman–Ford O(V·E).",
    ),
    Caso(
        "p3", "A", "P", "Máximo de camiones hacia clientes", "Luis Vaca · Distribución",
        "¿Se pueden enviar al menos K camiones/día de Planta a Clientes sin exceder capacidades?",
        "Red dirigida con capacidades enteras c(e) ≥ 0, fuente s, sumidero t.",
        "Valor del flujo máximo, flujo por tramo y corte mínimo.",
        "Optimización (flujo máximo); decisión asociada flujo ≥ K.",
        "Algoritmo polinómico conocido: Edmonds–Karp; el corte mínimo certifica optimalidad.",
        "Flujo factible (capacidad + conservación) verificable en O(V + E).", "—",
        "Edmonds–Karp (Ford–Fulkerson con BFS)", "Exacto",
        "O(V·E²)", "O(V + E)", "V = nodos, E = tramos",
        "Sí: a lo sumo O(V·E) aumentos, cada uno con un BFS O(E).",
        "logistpulse/casos/p3_flujo_maximo.py",
        "Flujo máximo = 10 aunque la salida de Planta suma 12 (cuello en los tramos hacia Clientes).",
    ),
    Caso(
        "n1", "B", "NP", "Comparar topologías equivalentes", "Elena Ruiz · Arquitectura",
        "¿Existe una biyección entre nodos que preserve todas las conexiones (A ≅ B)?",
        "Dos matrices de adyacencia n×n (grafos no dirigidos simples).",
        "Sí/No + permutación π como evidencia.",
        "Decisión.",
        "Certificado π + verificador O(n²) ⇒ ∈ NP.",
        "Permutación π de {0..n−1}; verificar A[i][j] = B[π(i)][π(j)] ∀ i,j.", "—",
        "Búsqueda exhaustiva de permutaciones (+ poda por grados)", "Exacto",
        "O(n!·n²)", "O(n²) entrada + O(n) extra", "n = nodos",
        "Sí: el conjunto de permutaciones es finito.",
        "logistpulse/casos/n1_isomorfismo.py",
        "No se afirma NPC: no se conoce reducción desde un NPC; Babai (2015) cuasi-polinómico.",
    ),
    Caso(
        "n2", "B", "NP", "¿Tiene N un factor en este intervalo?", "Andrés Molina · Seguridad",
        "¿Existe d con 2 ≤ d ≤ B que divida a N?",
        "Enteros N y B en binario (L ≈ log₂N + log₂B bits).",
        "Sí/No + divisor d como evidencia.",
        "Decisión.",
        "Certificado d + verificador O(L²) ⇒ ∈ NP.",
        "d; verificar 2 ≤ d ≤ B y N mod d = 0.", "—",
        "Prueba por división exhaustiva", "Exacto",
        "O(B·L²) — exponencial en L si B ≈ √N", "O(L)", "L = bits de la entrada, B = cota (valor)",
        "Sí: a lo sumo B−1 divisiones.",
        "logistpulse/casos/n2_factor_rango.py",
        "O(B) NO es polinomial: B vale hasta 2^{log B}. Está en NP ∩ coNP ⇒ improbable que sea NPC.",
    ),
    Caso(
        "n3", "B", "NP", "¿Existe exponente x que produzca h?", "Paola León · Seguridad TI",
        "¿Existe x con 0 ≤ x ≤ B y g^x ≡ h (mod p)?",
        "p primo, g, h, B en binario.",
        "Sí/No + exponente x como evidencia.",
        "Decisión.",
        "Certificado x + verificador con exponenciación rápida ⇒ ∈ NP.",
        "x; verificar 0 ≤ x ≤ B y pow(g, x, p) = h en O(log B·M(log p)).", "—",
        "Búsqueda exhaustiva con exponenciación modular (alternativa: baby-step giant-step)", "Exacto",
        "O(B·M(log p)) lineal · O(√B·M(log p)) BSGS", "O(1) lineal · O(√B) BSGS",
        "p = módulo, B = cota del exponente, M(k) = costo de multiplicar k bits",
        "Sí: a lo sumo B+1 candidatos.",
        "logistpulse/casos/n3_log_discreto.py",
        "Ambos métodos son exponenciales en log B; el verificador sí es polinómico.",
    ),
    Caso(
        "n4", "B", "NP", "¿La topología tiene una simetría?", "Santiago Jaramillo · Analítica",
        "¿Existe una permutación π ≠ identidad que preserve las adyacencias?",
        "Matriz de adyacencia n×n.",
        "Sí/No + π como evidencia.",
        "Decisión.",
        "Certificado π + verificador O(n²) ⇒ ∈ NP.",
        "π ≠ id; verificar G[i][j] = G[π(i)][π(j)] ∀ i,j.", "—",
        "Permutaciones + verificación de adyacencia", "Exacto",
        "O(n!·n²)", "O(n) extra", "n = vértices",
        "Sí: se agotan las n! permutaciones.",
        "logistpulse/casos/n4_automorfismo.py",
        "Triángulo: Sí (π = (0,2,1)). Grafo asimétrico de 6 vértices: No tras 720 permutaciones.",
    ),
    Caso(
        "c1", "C", "NP-completo", "¿Hay una asignación que cumpla todas las reglas?", "Mónica Ruiz · Planificación",
        "¿Existe una asignación verdadero/falso que satisfaga todas las cláusulas?",
        "Fórmula CNF: n variables, m cláusulas (≤ k literales c/u).",
        "Sí/No + asignación como evidencia.",
        "Decisión.",
        "Verificador O(m·k) + 3-SAT ≤p DESPACHO-SAT (identidad); Cook–Levin.",
        "Asignación de n bits.", "3-SAT ≤p DESPACHO-SAT (reducción identidad). SAT NPC por Cook–Levin; 3-SAT por Karp.",
        "DPLL (propagación unitaria + literal puro)", "Exacto",
        "DPLL O(2ⁿ·n·m·k) peor caso (fuerza bruta O(2ⁿ·m·k))", "O(n·m·k) (una copia simplificada por nivel de recursión)", "n = variables, m = cláusulas, k = literales por cláusula",
        "Sí: 2ⁿ asignaciones finitas.",
        "logistpulse/casos/c1_sat.py",
        "La instancia del simulador es 2-CNF ⇒ esa instancia cae en 2-SAT ∈ P (resuelta en O(n+m)). "
        "El problema general 3-CNF sigue siendo NPC.",
    ),
    Caso(
        "c2", "C", "NP-completo", "¿Existe una ruta hamiltoniana dentro del presupuesto?", "Jorge Tapia · Ruteo",
        "¿Existe un ciclo que visite cada centro una vez y vuelva al inicio con costo ≤ L?",
        "Matriz de distancias n×n (≥ 0) y presupuesto L.",
        "Sí/No + tour como evidencia (optimización aparte).",
        "Decisión (TSP-DEC); la optimización se trata por separado con Held–Karp.",
        "Verificador O(n) + HAM-CYCLE ≤p TSP-DEC (pesos 1/2, L = n).",
        "Orden de visita (tour).", "HAM-CYCLE ≤p TSP-DEC en O(n²) (Karp 1972).",
        "Enumeración de permutaciones (decisión) · Held–Karp (optimización) · vecino más cercano (heurística)",
        "Exacto (enumeración, Held–Karp) / heurístico (vecino más cercano)",
        "O((n−1)!·n) = O(n!) · Held–Karp O(n²·2ⁿ)", "O(n) · Held–Karp O(n·2ⁿ)", "n = centros",
        "Sí: (n−1)! tours finitos.",
        "logistpulse/casos/c2_tsp_decision.py",
        "Con L = 20: Sí (Planta→Quito→Guayaquil→Planta = 15). Con L = 14: No.",
    ),
    Caso(
        "c3", "C", "NP-completo", "¿Bastan k almacenes para cubrir todas las zonas?", "Carla Núñez · Red logística",
        "¿Existe un conjunto S de a lo sumo k zonas con almacén tal que toda adyacencia entre zonas (arista) tenga un almacén en uno de sus extremos?",
        "Grafo no dirigido G=(V,E) y entero k.",
        "Sí/No + conjunto S como evidencia.",
        "Decisión.",
        "Verificador O(V + E) + INDEPENDENT-SET ≤p VERTEX-COVER.",
        "Conjunto S ⊆ V.", "IS ≤p VC: <G,k> ∈ IS ⇔ <G,|V|−k> ∈ VC (Karp 1972).",
        "Backtracking / ramificación acotada (exacto) · 2-aproximación por emparejamiento (heurística)",
        "Exacto (ramificación) / aproximado (factor 2)",
        "O(2^k·(V + E)) ramificación · O(V + E) aproximación", "O(k·(V + E)) (lista de aristas por nivel)", "V = zonas, E = adyacencias entre zonas, k = almacenes",
        "Sí: árbol de búsqueda de profundidad ≤ k (o 2^V subconjuntos).",
        "logistpulse/casos/c3_vertex_cover.py",
        "El correo mezcla dos definiciones: 'zona cubierta por un almacén propio o vecino' (Dominating Set) y "
        "'Vertex Cover' / '¿Cubre toda arista?'. Se sigue Vertex Cover (etiqueta, datos y código del correo). "
        "Ambos son NP-completos y en esta instancia dan la misma respuesta (S = {B}).",
    ),
]

POR_ID = {c.id: c for c in CASOS}
