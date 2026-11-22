def verificar(p, g, h, B, x):
    """Verifica un exponente propuesto con exponenciación rápida: O(log x) multiplicaciones modulares."""
    return 0 <= x <= B and pow(g, x, p) == h % p


def buscar(p, g, h, B):
    """Prueba x = 0, 1, ..., B con una multiplicación por paso: O(B), exponencial en los bits de B."""
    valor = 1
    for x in range(B + 1):
        if valor == h % p:
            return x
        valor = valor * g % p
    return None


# Entrada: parámetros ficticios de la estación
p, g, h, B = 23, 5, 8, 10
x = buscar(p, g, h, B)
print(f"¿Existe x <= {B} con {g}^x = {h} (mod {p})?", x)

# Pruebas: exponente válido, exponente incorrecto y límite B demasiado bajo
assert x == 6 and verificar(p, g, h, B, x)
assert not verificar(p, g, h, B, 5)
assert buscar(p, g, h, 5) is None
print("Pruebas OK")
