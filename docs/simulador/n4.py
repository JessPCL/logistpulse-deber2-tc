from itertools import permutations


def verificar(G, p):
    """¿p es una simetría real (no la identidad) que conserva todas las adyacencias? O(n²)."""
    n = len(G)
    return (sorted(p) == list(range(n)) and list(p) != list(range(n))
            and all(G[i][j] == G[p[i]][p[j]] for i in range(n) for j in range(n)))


def buscar(G):
    """Prueba las n! permutaciones; si ninguna sirve, responde No tras agotarlas. O(n!·n²)."""
    for p in permutations(range(len(G))):
        if verificar(G, p):
            return p
    return None


def matriz(n, aristas):
    G = [[0] * n for _ in range(n)]
    for u, v in aristas:
        G[u][v] = G[v][u] = 1
    return G


# Entrada: el plano del portal (triángulo de 3 zonas)
triangulo = matriz(3, [(0, 1), (1, 2), (0, 2)])
p = buscar(triangulo)
print("Simetría del plano (zona i -> zona p[i]):", p)

# Pruebas: certificado válido, la identidad no cuenta y un grafo asimétrico agota las 6! = 720 opciones
assert p == (0, 2, 1) and verificar(triangulo, p)
assert not verificar(triangulo, (0, 1, 2))
asimetrico = matriz(6, [(0, 1), (1, 2), (2, 3), (3, 4), (5, 1), (5, 2)])
assert buscar(asimetrico) is None
print("Pruebas OK")
