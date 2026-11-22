from itertools import permutations


def costo(dist, ruta):
    return sum(dist[ruta[i]][ruta[i + 1]] for i in range(len(ruta) - 1))


def verificar(dist, L, ruta):
    """Visita cada centro una vez, vuelve a la salida y cuesta <= L. O(n)."""
    n = len(dist)
    return (len(ruta) == n + 1 and ruta[0] == ruta[-1] == 0
            and sorted(ruta[:-1]) == list(range(n)) and costo(dist, ruta) <= L)


def buscar(dist, L):
    """Pregunta de DECISIÓN: ¿existe un recorrido con costo <= L? Prueba los (n-1)! órdenes: O(n!·n)."""
    n = len(dist)
    for orden in permutations(range(1, n)):
        ruta = (0,) + orden + (0,)
        if costo(dist, ruta) <= L:
            return ruta
    return None


# Entrada: matriz de distancias (km) y presupuesto L del expediente
centros = ["Planta", "Quito", "Guayaquil"]
dist = [[0, 4, 8], [4, 0, 3], [8, 3, 0]]
L = 20
ruta = buscar(dist, L)
print("Recorrido:", " -> ".join(centros[i] for i in ruta), "| costo:", costo(dist, ruta), "km <=", L)

# Pruebas: recorrido verificado, presupuesto insuficiente y diferencia con la pregunta de optimización
assert ruta == (0, 1, 2, 0) and costo(dist, ruta) == 15 and verificar(dist, L, ruta)
assert buscar(dist, 14) is None
assert not verificar(dist, L, (0, 1, 0))  # no visita Guayaquil
mas_barato = min(costo(dist, (0,) + o + (0,)) for o in permutations(range(1, 3)))
assert mas_barato == 15  # el óptimo responde otra pregunta: ¿cuál es el recorrido más corto?
print("Pruebas OK")
