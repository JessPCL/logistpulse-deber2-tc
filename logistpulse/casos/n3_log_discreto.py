"""n3 · ¿Existe exponente x que produzca h?  (Paola León · Seguridad TI)

Decisión: DLOG-ACOTADO = {<p, g, h, B> : p primo y ∃ x, 0 ≤ x ≤ B, g^x ≡ h (mod p)}.
Tamaño: L ≈ log p + log B bits.
Certificado: x (≤ log₂B bits). Verificador: exponenciación rápida (cuadrado y
multiplicación), ≤ 2·⌈log₂(x+1)⌉ multiplicaciones modulares = O(log B · M(log p))
⇒ DLOG-ACOTADO ∈ NP.
Búsqueda lineal: ≤ B+1 multiplicaciones -> O(B · M(log p)): exponencial en log B.
Alternativa: baby-step giant-step, O(√B · M(log p)) tiempo y O(√B) espacio
(sigue siendo exponencial en el tamaño de B). No se afirma NP-completitud.
"""

from __future__ import annotations

import math
from typing import Optional

from ..conteo import contador_o_nulo


def es_primo(n: int) -> bool:
    """Miller–Rabin determinista para n < 3.3·10^24 (bases primas hasta 41)."""
    if n < 2:
        return False
    pequenos = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
    for q in pequenos:
        if n % q == 0:
            return n == q
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in pequenos:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def _validar(p: int, g: int, h: int, B: int) -> None:
    for nombre, x in (("p", p), ("g", g), ("h", h), ("B", B)):
        if isinstance(x, bool) or not isinstance(x, int):
            raise ValueError(f"{nombre} debe ser entero, recibido {x!r}")
    if not es_primo(p):
        raise ValueError(f"p = {p} no es primo")
    if not (1 <= g < p) or not (0 <= h < p):
        raise ValueError("Se requiere 1 ≤ g < p y 0 ≤ h < p")
    if B < 0:
        raise ValueError("B debe ser ≥ 0")


def potencia_modular(g: int, x: int, p: int, contar=None) -> int:
    """g^x mod p por cuadrado y multiplicación: ≤ 2·⌈log₂(x+1)⌉ multiplicaciones."""
    contar = contador_o_nulo(contar)
    resultado, base = 1 % p, g % p
    while x > 0:
        if x & 1:
            resultado = (resultado * base) % p
            contar("multiplicacion")
        base = (base * base) % p
        contar("multiplicacion")
        x >>= 1
    return resultado


def resolver(p: int, g: int, h: int, B: int, contar=None) -> Optional[int]:
    """BÚSQUEDA lineal: menor x ∈ [0, B] con g^x ≡ h. "multiplicacion" ≤ B + 1."""
    contar = contador_o_nulo(contar)
    _validar(p, g, h, B)
    valor = 1 % p
    for x in range(B + 1):
        if valor == h:
            return x
        valor = (valor * g) % p
        contar("multiplicacion")
    return None


def baby_step_giant_step(p: int, g: int, h: int, B: int, contar=None) -> Optional[int]:
    """BÚSQUEDA en O(√B): menor x ∈ [0, B] con g^x ≡ h (mod p)."""
    contar = contador_o_nulo(contar)
    _validar(p, g, h, B)
    m = math.isqrt(B) + 1
    bebe = {}
    v = 1 % p
    for j in range(m):  # pasos de bebé: g^j
        bebe.setdefault(v, j)
        v = (v * g) % p
        contar("multiplicacion")
    factor = pow(g, -m, p)  # g^{-m} (existe porque p es primo y g ≠ 0)
    gamma = h
    for i in range(m + 1):  # pasos de gigante: h·g^{-im}
        if gamma in bebe:
            x = i * m + bebe[gamma]
            return x if x <= B else None  # los siguientes candidatos son aún mayores
        gamma = (gamma * factor) % p
        contar("multiplicacion")
    return None


def verificar(p: int, g: int, h: int, B: int, x: int, contar=None) -> bool:
    """VERIFICACIÓN del certificado x: polinómica en log B y log p."""
    _validar(p, g, h, B)
    if isinstance(x, bool) or not isinstance(x, int) or not 0 <= x <= B:
        return False
    return potencia_modular(g, x, p, contar) == h
