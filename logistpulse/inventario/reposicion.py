"""Regla de reposición por punto de pedido.

    posición   = disponible + en_orden − reservado
    sugerencia = max(0, objetivo − posición)   si posición ≤ mínimo
                 0                              en otro caso

Evitar duplicados: como `en_orden` (órdenes de compra ABIERTAS) suma en la
posición, una orden ya emitida eleva la posición y la siguiente corrida sugiere
0 o solo la diferencia que falta. Ejecutar la regla dos veces seguidas, después
de emitir la orden sugerida, no genera una segunda orden (ver test de idempotencia).

Terminación: un recorrido sobre P productos, operaciones aritméticas O(1) por SKU.
Complejidad: O(P) tiempo; O(1) espacio extra si se procesa uno a uno (generador);
O(P) si se guardan todas las sugerencias.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator, List

from ..conteo import contador_o_nulo


def _entero_no_negativo(nombre: str, valor: object, sku: str) -> None:
    if isinstance(valor, bool) or not isinstance(valor, int) or valor < 0:
        raise ValueError(f"{sku}: '{nombre}' debe ser entero ≥ 0, recibido {valor!r}")


@dataclass(frozen=True)
class EstadoSKU:
    sku: str
    disponible: int
    en_orden: int
    reservado: int
    minimo: int
    objetivo: int

    def __post_init__(self) -> None:
        if not isinstance(self.sku, str) or not self.sku.strip():
            raise ValueError(f"SKU inválido: {self.sku!r}")
        for campo in ("disponible", "en_orden", "reservado", "minimo", "objetivo"):
            _entero_no_negativo(campo, getattr(self, campo), self.sku)
        if self.objetivo < self.minimo:
            raise ValueError(f"{self.sku}: objetivo ({self.objetivo}) < mínimo ({self.minimo})")

    @property
    def posicion(self) -> int:
        return self.disponible + self.en_orden - self.reservado


@dataclass(frozen=True)
class Sugerencia:
    sku: str
    posicion: int
    minimo: int
    objetivo: int
    cantidad: int

    @property
    def reponer(self) -> bool:
        return self.cantidad > 0


def sugerir(s: EstadoSKU) -> Sugerencia:
    pos = s.posicion
    cantidad = max(0, s.objetivo - pos) if pos <= s.minimo else 0
    return Sugerencia(s.sku, pos, s.minimo, s.objetivo, cantidad)


def sugerencias(skus: Iterable[EstadoSKU], contar=None) -> Iterator[Sugerencia]:
    """Generador: procesa un SKU a la vez con O(1) espacio extra. contar: "sku" = P.

    Los SKU repetidos se rechazan en la capa de LECTURA (io_datos.cargar_skus),
    para no guardar aquí un conjunto O(P) y respetar la cota O(1) del enunciado.
    """
    contar = contador_o_nulo(contar)
    for s in skus:
        contar("sku")
        yield sugerir(s)


def emitir_orden(s: EstadoSKU, cantidad: int) -> EstadoSKU:
    """Simula emitir una orden de compra: la cantidad pasa a en_orden."""
    _entero_no_negativo("cantidad", cantidad, s.sku)
    return EstadoSKU(s.sku, s.disponible, s.en_orden + cantidad, s.reservado, s.minimo, s.objetivo)
