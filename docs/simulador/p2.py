import heapq


def dijkstra(tramos, origen):
    """Tiempos mínimos desde origen con tiempos >= 0. Tiempo O((V + E) log V), espacio O(V + E)."""
    ady = {}
    for u, v, w in tramos:
        if w < 0:
            raise ValueError("Dijkstra exige tiempos no negativos")
        ady.setdefault(u, []).append((v, w))
        ady.setdefault(v, [])
    dist = {x: float("inf") for x in ady}
    pred = {x: None for x in ady}  # lo que el sistema debe conservar para reconstruir la ruta
    dist[origen] = 0
    heap = [(0, origen)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue  # entrada vieja del heap
        for v, w in ady[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                pred[v] = u
                heapq.heappush(heap, (dist[v], v))
    return dist, pred


def ruta(pred, destino):
    camino = []
    while destino is not None:
        camino.append(destino)
        destino = pred[destino]
    return camino[::-1]


# Entrada: tiempos nuevos del expediente (tramos con sentido)
tramos = [("Quito", "Latacunga", 2), ("Quito", "Ambato", 5), ("Latacunga", "Guayaquil", 6), ("Ambato", "Guayaquil", 3)]
dist, pred = dijkstra(tramos, "Quito")
print("Tiempo mínimo Quito -> Guayaquil:", dist["Guayaquil"], "| ruta:", " -> ".join(ruta(pred, "Guayaquil")))

# Pruebas: tiempos a cada nodo, empate en 8 y rechazo de pesos negativos
assert dist == {"Quito": 0, "Latacunga": 2, "Ambato": 5, "Guayaquil": 8}
assert ruta(pred, "Guayaquil") == ["Quito", "Latacunga", "Guayaquil"]  # Quito -> Ambato -> Guayaquil también suma 8
try:
    dijkstra([("S", "A", 2), ("S", "B", 3), ("B", "A", -2)], "S")
    raise AssertionError("debía rechazar el peso negativo")
except ValueError:
    pass  # con pesos negativos Dijkstra no garantiza el mínimo (se usaría Bellman-Ford)
print("Pruebas OK")
