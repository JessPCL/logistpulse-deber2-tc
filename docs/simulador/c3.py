def verificar(corredores, k, S):
    """Verificador separado: |S| <= k y cada corredor tiene un equipo en un extremo. O(V + E)."""
    zonas = {z for c in corredores for z in c}
    return len(S) <= k and set(S) <= zonas and all(u in S or v in S for u, v in corredores)


def ramificar(corredores, k):
    """Toma un corredor sin cubrir (u, v): toda solución contiene a u o a v. Tiempo O(2^k·(V + E))."""
    if not corredores:
        return set()
    if k == 0:
        return None
    u, v = corredores[0]
    for z in (u, v):
        resto = [c for c in corredores if z not in c]
        r = ramificar(resto, k - 1)
        if r is not None:
            return r | {z}
    return None


# Entrada: corredores entre zonas y k equipos de inspección
corredores = [("A", "B"), ("B", "C")]
k = 1
S = ramificar(corredores, k)
print(f"¿Bastan {k} equipo(s)?", S is not None, "| selección:", S)

# Pruebas: certificado {B}, k = 0 sin solución, selección que no cubre y un caso que exige k + 1
assert S == {"B"} and verificar(corredores, k, S)
assert ramificar(corredores, 0) is None
assert not verificar(corredores, 1, {"A"})
pares = [(f"a{i}", f"b{i}") for i in range(5)]
assert ramificar(pares, 4) is None and verificar(pares, 5, ramificar(pares, 5))
print("Pruebas OK")
