"""Selección FEFO (First Expired, First Out) para reservar inventario.

Reglas (Fase C):
- Elegible  ⇔  mismo SKU  ∧  disponible > 0  ∧  vencimiento > fecha_referencia.
  Un lote que vence HOY ya no se reserva (decisión documentada; ver DECISIONES).
- Orden: (vencimiento ascendente, código de lote ascendente)  -> desempate reproducible.
- Política si el stock elegible no alcanza (las tres que menciona el enunciado):
    "parcial"  : reserva lo que hay y reporta el pendiente           (estado PARCIAL).
    "rechazar" : no reserva nada y el pedido se rechaza              (estado RECHAZADO).
    "esperar"  : no reserva nada; el pedido queda en espera de la
                 reposición y se marca requiere_reposicion           (estado EN_ESPERA).

Terminación: un filtro, un ordenamiento y un recorrido sobre una lista finita;
el recorrido se detiene antes si la cantidad pendiente llega a 0.
Complejidad con L lotes: O(L log L) tiempo (ordenar) + O(L) recorrido; O(L) espacio.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Iterable, List, Tuple

from ..conteo import contador_o_nulo

POLITICAS = ("parcial", "rechazar", "esperar")


@dataclass(frozen=True)
class Lote:
    codigo: str
    sku: str
    vencimiento: date
    disponible: int

    def __post_init__(self) -> None:
        if not isinstance(self.codigo, str) or not self.codigo.strip():
            raise ValueError(f"Código de lote inválido: {self.codigo!r}")
        if not isinstance(self.sku, str) or not self.sku.strip():
            raise ValueError(f"SKU inválido en lote {self.codigo}")
        if not isinstance(self.vencimiento, date):
            raise ValueError(f"Fecha de vencimiento inválida en lote {self.codigo}")
        if isinstance(self.disponible, bool) or not isinstance(self.disponible, int) or self.disponible < 0:
            raise ValueError(f"Disponible debe ser entero ≥ 0 en lote {self.codigo}: {self.disponible!r}")


@dataclass
class ResultadoFEFO:
    sku: str
    solicitado: int
    plan: List[Tuple[str, int]]  # (código de lote, cantidad a tomar)
    pendiente: int
    estado: str  # COMPLETO | PARCIAL | RECHAZADO | EN_ESPERA
    descartados: List[Tuple[str, str]] = field(default_factory=list)  # (código, motivo)
    orden_considerado: List[str] = field(default_factory=list)

    @property
    def reservado(self) -> int:
        return sum(c for _, c in self.plan)

    @property
    def requiere_reposicion(self) -> bool:
        return self.pendiente > 0


class _ClaveContada:
    """Envuelve la clave de orden para contar comparaciones (Timsort usa solo <)."""

    __slots__ = ("clave", "contar")

    def __init__(self, clave, contar) -> None:
        self.clave, self.contar = clave, contar

    def __lt__(self, otra: "_ClaveContada") -> bool:
        self.contar("comparacion")
        return self.clave < otra.clave


def seleccionar_fefo(lotes: Iterable[Lote], sku: str, cantidad: int, fecha_referencia: date,
                     politica: str = "parcial", contar=None) -> ResultadoFEFO:
    """contar: "lote" ≤ 2L (filtro + recorrido), "comparacion" ≤ L·⌈log₂L⌉ + L (ordenamiento)."""
    contar = contador_o_nulo(contar)
    lotes = list(lotes)
    if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
        raise ValueError(f"La cantidad pedida debe ser entero > 0: {cantidad!r}")
    if politica not in POLITICAS:
        raise ValueError(f"Política desconocida '{politica}'. Use una de {POLITICAS}")
    if not isinstance(fecha_referencia, date):
        raise ValueError("fecha_referencia debe ser datetime.date")
    codigos = [l.codigo for l in lotes]
    if len(set(codigos)) != len(codigos):
        raise ValueError("Hay códigos de lote repetidos")

    # 1) Filtrar candidatos (O(L)) y registrar por qué se descarta cada lote.
    candidatos, descartados = [], []
    for l in lotes:
        contar("lote")
        if l.sku != sku:
            continue
        if l.vencimiento <= fecha_referencia:
            descartados.append((l.codigo, f"vencido o vence hoy ({l.vencimiento.isoformat()})"))
        elif l.disponible == 0:
            descartados.append((l.codigo, "sin cantidad disponible"))
        else:
            candidatos.append(l)

    # 2) Ordenar por (vencimiento, código)  -> O(L log L)
    candidatos.sort(key=lambda l: _ClaveContada((l.vencimiento, l.codigo), contar))

    # 3) Recorrer tomando lo necesario  -> O(L)
    pendiente, plan = cantidad, []
    for l in candidatos:
        if pendiente == 0:
            break
        contar("lote")
        tomar = min(pendiente, l.disponible)
        plan.append((l.codigo, tomar))
        pendiente -= tomar

    if pendiente == 0:
        estado = "COMPLETO"
    elif politica == "rechazar":
        plan, pendiente, estado = [], cantidad, "RECHAZADO"
    elif politica == "esperar":
        plan, pendiente, estado = [], cantidad, "EN_ESPERA"
    else:
        estado = "PARCIAL"
    return ResultadoFEFO(sku, cantidad, plan, pendiente, estado, sorted(descartados),
                         [l.codigo for l in candidatos])
