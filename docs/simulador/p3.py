from collections import deque


def edmonds_karp(tramos, s, t, registro):
    """Flujo máximo con caminos aumentantes por BFS (Edmonds-Karp). Tiempo O(V·E²), espacio O(V + E)."""
    cap, ady = {}, {}
    for u, v, c in tramos:
        for a, b in ((u, v), (v, u)):
            if (a, b) not in cap:
                cap[(a, b)] = 0
                ady.setdefault(a, []).append(b)
        cap[(u, v)] += c
    original = dict(cap)
    flujo = 0
    while True:
        padre = {s: None}
        cola = deque([s])
        while cola and t not in padre:
            u = cola.popleft()
            for v in ady[u]:
                if v not in padre and cap[(u, v)] > 0:
                    padre[v] = u
                    cola.append(v)
        if t not in padre:
            return flujo
        camino, v = [], t
        while padre[v] is not None:
            camino.append((padre[v], v))
            v = padre[v]
        camino.reverse()
        cuello = min(cap[e] for e in camino)
        for u, v in camino:
            cap[(u, v)] -= cuello
            cap[(v, u)] += cuello
        flujo += cuello
        estado = [f"{u}->{v} usado {original[(u, v)] - cap[(u, v)]}/{original[(u, v)]}" for u, v in camino]
        registro.append(f"cuello {cuello}, total {flujo}: " + "; ".join(estado))


# Entrada: capacidades del expediente (camiones/día por tramo)
tramos = [("Planta", "Quito", 7), ("Planta", "Guayaquil", 5), ("Quito", "Clientes", 4),
          ("Guayaquil", "Clientes", 6), ("Quito", "Guayaquil", 2)]
registro = []
maximo = edmonds_karp(tramos, "Planta", "Clientes", registro)
print("Máximo de camiones/día:", maximo)
for i, linea in enumerate(registro, 1):
    print(f"  Aumento {i}: {linea}")

# Pruebas: máximo 10 (no 12 = 7 + 5) y un caso con cuello de botella simple
assert maximo == 10
assert sum(c for u, v, c in tramos if u == "Planta") == 12
assert edmonds_karp([("s", "a", 3), ("a", "t", 2)], "s", "t", []) == 2
print("Pruebas OK")
