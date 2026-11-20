"""Conteo de operaciones básicas, para comprobar EMPÍRICAMENTE las cotas Big-O.

Cada algoritmo acepta un parámetro opcional `contar`. Si se pasa un Contador,
el algoritmo suma 1 cada vez que ejecuta su operación dominante (extraer de la
cola, examinar una arista, probar una permutación…). tests/test_complejidad.py
compara esos conteos con la cota teórica: así el Big-O escrito en el informe
queda atado al código real y no solo al libro.

Contar operaciones es determinista (no depende de la máquina), a diferencia de
medir segundos; por eso es la prueba principal. Los tiempos reales se prueban
aparte, con tolerancias amplias.
"""

from __future__ import annotations

from typing import Callable, Dict

FuncionConteo = Callable[..., None]


class Contador:
    def __init__(self) -> None:
        self.conteos: Dict[str, int] = {}

    def __call__(self, clave: str, n: int = 1) -> None:
        self.conteos[clave] = self.conteos.get(clave, 0) + n

    def __getitem__(self, clave: str) -> int:
        return self.conteos.get(clave, 0)

    def __repr__(self) -> str:
        return f"Contador({self.conteos})"


def no_contar(clave: str, n: int = 1) -> None:
    """Contador nulo (por defecto): no hace nada y no cambia la complejidad."""


def contador_o_nulo(contar) -> FuncionConteo:
    return no_contar if contar is None else contar
