"""n2 · ¿Tiene N un factor en este intervalo?  (Andrés Molina · Seguridad)

Decisión: FACTOR-RANGO = {<N, B> : ∃ d con 2 ≤ d ≤ B y d | N}, con N y B en BINARIO.
Tamaño de la entrada: L ≈ log₂N + log₂B bits (el VALOR de B puede ser ~2^L).
Certificado: d (≤ log₂B bits). Verificador: una división con resto, O(M(L)) = O(L²)
con división escolar  ⇒  FACTOR-RANGO ∈ NP.
Búsqueda por división de prueba: hasta B−1 divisiones ⇒ O(B·L²) = O(2^{log₂B}·L²):
pseudo-polinómica, EXPONENCIAL en el tamaño de la entrada si B ≈ √N.
No se afirma NP-completitud (además está en NP ∩ coNP: un "No" se certifica con
la factorización prima de N y certificados de primalidad; si fuera NPC, NP = coNP).
Nota: si B ≥ N la respuesta es trivialmente Sí (d = N); el caso interesante es B < N.
"""

from __future__ import annotations

from typing import Optional

from ..conteo import contador_o_nulo


def desde_binario(bits: str) -> int:
    if not isinstance(bits, str) or not bits or any(c not in "01" for c in bits):
        raise ValueError(f"Cadena binaria inválida: {bits!r}")
    return int(bits, 2)


def _validar(N: int, B: int) -> None:
    for nombre, x in (("N", N), ("B", B)):
        if isinstance(x, bool) or not isinstance(x, int):
            raise ValueError(f"{nombre} debe ser entero, recibido {x!r}")
    if N < 2:
        raise ValueError("N debe ser ≥ 2")
    if B < 0:
        raise ValueError("B debe ser ≥ 0")


def resolver(N: int, B: int, contar=None) -> Optional[int]:
    """BÚSQUEDA: menor divisor d ∈ [2, B], o None. "division" ≤ B − 1."""
    contar = contador_o_nulo(contar)
    _validar(N, B)
    for d in range(2, B + 1):
        contar("division")
        if N % d == 0:
            return d
    return None


def verificar(N: int, B: int, d: int, contar=None) -> bool:
    """VERIFICACIÓN del certificado d: una sola división. O(L²)."""
    contar = contador_o_nulo(contar)
    _validar(N, B)
    if isinstance(d, bool) or not isinstance(d, int) or not 2 <= d <= B:
        return False
    contar("division")
    return N % d == 0
