def verificar(N, B, d):
    """Verifica un divisor propuesto con una sola división: polinomial en log N."""
    return 2 <= d <= B and N % d == 0


def buscar(N, B):
    """Prueba d = 2, 3, ..., min(B, N): O(B) divisiones, exponencial en los bits de B."""
    for d in range(2, min(B, N) + 1):
        if N % d == 0:
            return d
    return None


# Entrada: datos de la consola (los números se reciben en binario)
N, B = 91, 10
d = buscar(N, B)
print(f"N = {N} ({bin(N)[2:]}, {N.bit_length()} bits), B = {B} ({bin(B)[2:]}) -> divisor:", d)

# Pruebas: divisor en el rango, rango sin divisor, certificado fuera de rango y un primo
assert d == 7 and verificar(N, B, d)
assert buscar(91, 6) is None
assert not verificar(91, 10, 13)
assert buscar(97, 96) is None
print("Pruebas OK")
