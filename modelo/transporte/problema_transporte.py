"""
modelo/transporte/problema_transporte.py
========================================
Guarda los datos de un problema de transporte: qué origen envía a qué
destino, cuánto cuesta cada envío por unidad, cuánto ofrece cada origen
y cuánto necesita cada destino. Se busca el menor costo total.

    x_ij = unidades que se envían del origen i al destino j
    c_ij = costo de enviar 1 unidad (puede ser M = ruta prohibida)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction

from ..numeros import ValorM


@dataclass
class ProblemaTransporte:
    nombre: str
    unidad_producto: str          # p. ej. "cajas"
    unidad_costo: str             # p. ej. "COP" (el costo unitario es COP por caja)
    origenes: list[str]
    destinos: list[str]
    oferta: list[Fraction]
    demanda: list[Fraction]
    costos: list[list[ValorM]]
    descripcion: str = ""
    datos_originales: dict = field(default_factory=dict, repr=False)

    @property
    def m(self) -> int:
        """Número de orígenes."""
        return len(self.origenes)

    @property
    def n(self) -> int:
        """Número de destinos."""
        return len(self.destinos)

    @property
    def total_oferta(self) -> Fraction:
        return sum(self.oferta, Fraction(0))

    @property
    def total_demanda(self) -> Fraction:
        return sum(self.demanda, Fraction(0))

    @property
    def esta_balanceado(self) -> bool:
        return self.total_oferta == self.total_demanda

    def rutas_prohibidas(self) -> list[tuple[int, int]]:
        return [(i, j) for i in range(self.m) for j in range(self.n) if self.costos[i][j].tiene_m]
