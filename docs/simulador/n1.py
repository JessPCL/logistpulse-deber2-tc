from itertools import permutations


def verificar(A, B, p):
    """¿La correspondencia p conserva todas las conexiones? O(n²)."""
    n = len(A)
    return sorted(p) == list(range(n)) and all(A[i][j] == B[p[i]][p[j]] for i in range(n) for j in range(n))


def buscar(A, B):
    """Prueba las n! correspondencias. Tiempo O(n!·n²), espacio O(n)."""
    if len(A) != len(B):
        return None
    for p in permutations(range(len(A))):
        if verificar(A, B, p):
            return p
    return None


# Entrada: matrices de adyacencia de las dos redes (código del expediente)
A = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
B = [[0, 1, 1], [1, 0, 0], [1, 0, 0]]
p = buscar(A, B)
print("¿Misma estructura?", p is not None, "| correspondencia nodo i de A -> nodo p[i] de B:", p)

# Pruebas: certificado válido, identidad inválida y un par no isomorfo con los mismos grados
assert p == (1, 0, 2) and verificar(A, B, p)
assert not verificar(A, B, (0, 1, 2))
C6 = [[1 if abs(i - j) in (1, 5) else 0 for j in range(6)] for i in range(6)]
dos_triangulos = [[1 if i != j and i // 3 == j // 3 else 0 for j in range(6)] for i in range(6)]
assert buscar(C6, dos_triangulos) is None
print("Pruebas OK")
