"""Autómata finito determinista (AFD) M = (Q, Σ, δ, q0, F).

Decisiones de diseño:
- δ se declara PARCIAL (solo transiciones válidas del proceso). Para que el AFD
  sea formalmente total, toda pareja (q, a) no declarada va a un estado
  sumidero ``ERROR`` que no es final y del que no se sale (δ(ERROR, a) = ERROR).
  JFLAP hace lo mismo implícitamente: si no hay transición, rechaza.
- Un símbolo que no pertenece a Σ NO es un rechazo: es una entrada inválida
  (la cadena no está en Σ*). Se lanza ValueError para distinguir ambos casos.

Complejidad de ejecutar una cadena de longitud n: O(n) tiempo (una búsqueda
en diccionario por símbolo) y O(n) espacio si se guarda la traza (O(1) sin ella).
Siempre termina: consume exactamente un símbolo por paso.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Union

from ..conteo import contador_o_nulo

ESTADO_SUMIDERO = "ERROR"


@dataclass(frozen=True)
class ResultadoAFD:
    """Resultado de procesar una secuencia."""

    aceptada: bool
    estado_final: str
    traza: Tuple[Tuple[str, str, str], ...]  # (origen, símbolo, destino)
    motivo: str

    def como_texto(self) -> str:
        pasos = " ".join(f"{o} --{s}--> {d} |" for o, s, d in self.traza)
        veredicto = "ACEPTADA" if self.aceptada else "RECHAZADA"
        return f"{veredicto}: {pasos} estado final = {self.estado_final}. {self.motivo}"


@dataclass
class AFD:
    nombre: str
    estados: Sequence[str]
    alfabeto: Mapping[str, str]  # símbolo -> nombre del evento
    inicial: str
    finales: Iterable[str]
    delta: Mapping[Tuple[str, str], str]
    posiciones: Mapping[str, Tuple[float, float]] = field(default_factory=dict)
    descripcion: str = ""

    def __post_init__(self) -> None:
        self.estados = list(self.estados)
        self.finales = frozenset(self.finales)
        self.alfabeto = dict(self.alfabeto)
        self.delta = dict(self.delta)
        self._validar()
        self._evento_a_simbolo = {ev: s for s, ev in self.alfabeto.items()}

    # ------------------------------------------------------------------ validación
    def _validar(self) -> None:
        if len(set(self.estados)) != len(self.estados):
            raise ValueError(f"{self.nombre}: hay estados repetidos en Q")
        if ESTADO_SUMIDERO in self.estados:
            raise ValueError(f"{self.nombre}: '{ESTADO_SUMIDERO}' está reservado para el sumidero")
        if self.inicial not in self.estados:
            raise ValueError(f"{self.nombre}: q0='{self.inicial}' no pertenece a Q")
        if not self.finales <= set(self.estados):
            raise ValueError(f"{self.nombre}: F no es subconjunto de Q: {set(self.finales) - set(self.estados)}")
        for s in self.alfabeto:
            if len(s) != 1:
                raise ValueError(f"{self.nombre}: cada símbolo de Σ debe ser 1 carácter (JFLAP), recibido '{s}'")
        if len(set(self.alfabeto.values())) != len(self.alfabeto):
            raise ValueError(f"{self.nombre}: dos símbolos comparten el mismo nombre de evento")
        for (q, a), destino in self.delta.items():
            if q not in self.estados or destino not in self.estados:
                raise ValueError(f"{self.nombre}: δ({q},{a})={destino} usa un estado fuera de Q")
            if a not in self.alfabeto:
                raise ValueError(f"{self.nombre}: δ({q},{a}) usa un símbolo fuera de Σ")

    # ------------------------------------------------------------------ semántica
    def transicion(self, q: str, a: str) -> str:
        """δ total: devuelve el sumidero si (q, a) no está definida."""
        if q == ESTADO_SUMIDERO:
            return ESTADO_SUMIDERO
        return self.delta.get((q, a), ESTADO_SUMIDERO)

    def _normalizar(self, secuencia: Union[str, Sequence[str]]) -> List[str]:
        """Acepta 'criedn', ['c','r'] o ['confirmar','reservar']."""
        if isinstance(secuencia, str):
            simbolos = list(secuencia)
        else:
            simbolos = []
            for item in secuencia:
                if not isinstance(item, str):
                    raise ValueError(f"Elemento no textual en la secuencia: {item!r}")
                simbolos.append(self._evento_a_simbolo.get(item, item))
        for s in simbolos:
            if s not in self.alfabeto:
                raise ValueError(
                    f"{self.nombre}: '{s}' no pertenece a Σ = {sorted(self.alfabeto)}; "
                    "la cadena no está en Σ* (entrada inválida, no un rechazo)"
                )
        return simbolos

    def ejecutar(self, secuencia: Union[str, Sequence[str]], contar=None) -> ResultadoAFD:
        contar = contador_o_nulo(contar)
        simbolos = self._normalizar(secuencia)
        q = self.inicial
        traza: List[Tuple[str, str, str]] = []
        motivo = ""
        for i, a in enumerate(simbolos):
            contar("paso")  # una consulta a δ por símbolo -> O(n)
            destino = self.transicion(q, a)
            traza.append((q, a, destino))
            if destino == ESTADO_SUMIDERO and not motivo:
                motivo = (
                    f"Paso {i + 1}: δ({q}, {a}='{self.alfabeto[a]}') no está definida "
                    f"-> sumidero {ESTADO_SUMIDERO}."
                )
            q = destino
        aceptada = q in self.finales
        if not motivo:
            motivo = (
                f"{q} ∈ F." if aceptada else f"{q} ∉ F: la secuencia termina en un estado no final (proceso incompleto)."
            )
        return ResultadoAFD(aceptada, q, tuple(traza), motivo)

    def acepta(self, secuencia: Union[str, Sequence[str]]) -> bool:
        return self.ejecutar(secuencia).aceptada

    # ------------------------------------------------------------------ utilidades
    def eventos(self, cadena: str) -> List[str]:
        return [self.alfabeto[s] for s in self._normalizar(cadena)]

    def estados_alcanzables(self) -> set:
        vistos, pila = {self.inicial}, [self.inicial]
        while pila:
            q = pila.pop()
            for (o, _a), d in self.delta.items():
                if o == q and d not in vistos:
                    vistos.add(d)
                    pila.append(d)
        return vistos

    def tabla_markdown(self) -> str:
        """Tabla de transiciones completa (incluye columna por cada símbolo)."""
        simbolos = list(self.alfabeto)
        cab = "| Estado | " + " | ".join(f"{s} ({self.alfabeto[s]})" for s in simbolos) + " |"
        sep = "|---|" + "---|" * len(simbolos)
        filas = [cab, sep]
        for q in self.estados:
            marca = ("→ " if q == self.inicial else "") + q + (" *" if q in self.finales else "")
            celdas = [self.delta.get((q, s), "∅") for s in simbolos]
            filas.append(f"| {marca} | " + " | ".join(celdas) + " |")
        filas.append(f"| {ESTADO_SUMIDERO} (sumidero) | " + " | ".join([ESTADO_SUMIDERO] * len(simbolos)) + " |")
        return "\n".join(filas) + "\n\n→ = estado inicial · * = estado final · ∅ = va al sumidero ERROR"

    def definicion_formal(self) -> str:
        sigma = ", ".join(f"{s}={e}" for s, e in self.alfabeto.items())
        return (
            f"M_{self.nombre} = (Q, Σ, δ, q0, F)\n"
            f"Q  = {{{', '.join(self.estados)}}} ∪ {{{ESTADO_SUMIDERO}}}\n"
            f"Σ  = {{{sigma}}}\n"
            f"q0 = {self.inicial}\n"
            f"F  = {{{', '.join(q for q in self.estados if q in self.finales)}}}\n"
            f"|δ declarada| = {len(self.delta)} transiciones (el resto va a {ESTADO_SUMIDERO})"
        )
