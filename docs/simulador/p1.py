from collections import deque


def hay_ruta(conexiones, origen, destino):
    """BFS sobre tramos con sentido. Devuelve el camino o None. Tiempo O(V + E), espacio O(V)."""
    ady = {}
    for u, v in conexiones:
        ady.setdefault(u, []).append(v)
        ady.setdefault(v, [])
    if origen not in ady or destino not in ady:
        return None
    padre = {origen: None}
    cola = deque([origen])
    while cola:
        u = cola.popleft()
        if u == destino:
            camino = []
            while u is not None:
                camino.append(u)
                u = padre[u]
            return camino[::-1]
        for v in ady[u]:
            if v not in padre:  # cada zona entra a la cola una sola vez
                padre[v] = u
                cola.append(v)
    return None


# Entrada: tramos habilitados del expediente (las flechas del mapa tienen sentido)
tramos = [("Durán", "Quito"), ("Durán", "Guayaquil"), ("Quito", "Norte"), ("Guayaquil", "Sur")]
print("¿Hay ruta Durán -> Norte?", hay_ruta(tramos, "Durán", "Norte"))

# Pruebas: con ruta, sin ruta (cierre de Quito -> Norte) y respeto del sentido
assert hay_ruta(tramos, "Durán", "Norte") == ["Durán", "Quito", "Norte"]
sin_quito_norte = [t for t in tramos if t != ("Quito", "Norte")]
assert hay_ruta(sin_quito_norte, "Durán", "Norte") is None
assert hay_ruta(tramos, "Norte", "Durán") is None
print("Pruebas OK")
