"""
modelo/transporte/optimizador_modi.py
=====================================
Método MODI: revisa si la solución de Vogel se puede mejorar y, si se
puede, la mejora hasta llegar a la mejor. Así se compara el costo de Vogel
con el mejor costo posible.

  1. Se calculan unos valores u (por fila) y v (por columna) con las
     celdas que tienen envío: u_i + v_j = costo.
  2. Para cada celda sin envío se calcula d_ij = costo − u_i − v_j.
  3. Si todos los d_ij son 0 o más, ya es la mejor solución
     (si alguno es 0, hay otra solución con el mismo costo).
  4. Si no, entra la celda con el d_ij más negativo y se arma un camino
     cerrado (+ − + − ...) con celdas que tienen envío.
  5. Se mueve la cantidad θ (la menor de las celdas −): se suma en las (+)
     y se resta en las (−). Se vuelve al paso 1.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from fractions import Fraction

from ..caso_especial import (DEGENERACION, INFACTIBLE, INFORMATIVO, NIVEL_ADVERTENCIA, NIVEL_ERROR,
                             NIVEL_EXITO, NIVEL_INFO, OPTIMOS_ALTERNATIVOS, CasoEspecial)
from ..numeros import ValorM, texto_numero
from .solver_vogel import ResultadoVogel

ESTADO_OPTIMO = "optimo"
ESTADO_LIMITE = "limite_iteraciones"


@dataclass
class IteracionMODI:
    numero: int
    asignaciones: dict                 # envíos ANTES del cambio {(i, j): cantidad}
    u: list[ValorM]
    v: list[ValorM]
    fila_referencia: int               # fila donde u = 0
    costos_reducidos: dict             # {(i, j): d_ij} de las celdas sin envío
    es_optima: bool
    costo: ValorM
    entra: tuple | None = None
    empate_entrada: list = field(default_factory=list)
    ciclo: list = field(default_factory=list)   # celdas del camino; posición par = (+), impar = (−)
    theta: Fraction | None = None
    sale: tuple | None = None
    empate_salida: list = field(default_factory=list)


@dataclass
class ResultadoMODI:
    iteraciones: list[IteracionMODI]
    asignaciones: dict                 # mejor solución {(i, j): cantidad}
    costo_inicial: ValorM
    costo_optimo: ValorM
    estado: str
    celdas_alternativas: list          # celdas sin envío con d_ij = 0 en la mejor solución
    rutas_prohibidas_usadas: list
    casos: list[CasoEspecial] = field(default_factory=list)

    @property
    def vogel_es_optimo(self) -> bool:
        return self.estado == ESTADO_OPTIMO and self.costo_inicial == self.costo_optimo

    @property
    def ahorro(self) -> ValorM:
        return self.costo_inicial - self.costo_optimo


class OptimizadorMODI:
    """Aplica MODI a la solución inicial de Vogel."""

    MAX_ITERACIONES = 200

    def __init__(self, resultado_vogel: ResultadoVogel):
        self.vogel = resultado_vogel
        self.costos = resultado_vogel.costos
        self.m = resultado_vogel.m
        self.n = resultado_vogel.n

    # ---------------------------------------- PASO 1: u_i + v_j = c_ij
    def _potenciales(self, basicas):
        conteo = [0] * self.m
        for i, _ in basicas:
            conteo[i] += 1
        referencia = max(range(self.m), key=lambda i: (conteo[i], -i))
        u: list = [None] * self.m
        v: list = [None] * self.n
        u[referencia] = ValorM(0)
        pendientes = list(basicas)
        hubo_cambio = True
        while pendientes and hubo_cambio:
            hubo_cambio = False
            for celda in list(pendientes):
                i, j = celda
                if u[i] is not None and v[j] is None:
                    v[j] = self.costos[i][j] - u[i]
                elif v[j] is not None and u[i] is None:
                    u[i] = self.costos[i][j] - v[j]
                elif u[i] is None and v[j] is None:
                    continue
                pendientes.remove(celda)
                hubo_cambio = True
        if any(x is None for x in u) or any(x is None for x in v):
            raise ValueError("Las celdas básicas no forman una base válida (árbol).")
        return u, v, referencia

    # --------------------------------- PASO 4: ciclo cerrado con celdas básicas
    @staticmethod
    def _ciclo(basicas, entra):
        vecinos: dict = {}
        for i, j in basicas:
            vecinos.setdefault(("f", i), []).append((("c", j), (i, j)))
            vecinos.setdefault(("c", j), []).append((("f", i), (i, j)))
        inicio, objetivo = ("c", entra[1]), ("f", entra[0])
        padre = {inicio: None}
        cola = deque([inicio])
        while cola:
            nodo = cola.popleft()
            if nodo == objetivo:
                break
            for vecino, celda in vecinos.get(nodo, []):
                if vecino not in padre:
                    padre[vecino] = (nodo, celda)
                    cola.append(vecino)
        if objetivo not in padre:
            raise ValueError("No se encontró un ciclo para la celda que entra.")
        camino = []
        nodo = objetivo
        while padre[nodo] is not None:
            anterior, celda = padre[nodo]
            camino.append(celda)
            nodo = anterior
        camino.reverse()
        return [entra] + camino

    def _costo(self, asignaciones) -> ValorM:
        return sum((self.costos[i][j] * x for (i, j), x in asignaciones.items()), ValorM(0))

    # ------------------------------------------------------------- resolver
    def resolver(self) -> ResultadoMODI:
        asignaciones = dict(self.vogel.asignaciones)
        iteraciones: list[IteracionMODI] = []
        bases_vistas = set()
        anti_ciclaje = False
        estado = ESTADO_LIMITE
        numero = 0
        while True:
            basicas = list(asignaciones.keys())
            clave = frozenset(basicas)
            if clave in bases_vistas:
                anti_ciclaje = True
            bases_vistas.add(clave)

            # PASO 1 y 2: valores u, v y d_ij
            u, v, referencia = self._potenciales(basicas)
            reducidos = {(i, j): self.costos[i][j] - u[i] - v[j]
                         for i in range(self.m) for j in range(self.n) if (i, j) not in asignaciones}
            costo = self._costo(asignaciones)
            negativos = [c for c, d in reducidos.items() if d < 0]

            # PASO 3: ¿ya es la mejor?
            if not negativos:
                iteraciones.append(IteracionMODI(numero, dict(asignaciones), u, v, referencia,
                                                 reducidos, True, costo))
                estado = ESTADO_OPTIMO
                break
            if numero >= self.MAX_ITERACIONES:
                iteraciones.append(IteracionMODI(numero, dict(asignaciones), u, v, referencia,
                                                 reducidos, False, costo))
                break

            # PASO 4: celda que entra y camino
            if anti_ciclaje:
                entra, empate = negativos[0], []
            else:
                peor = min(reducidos[c] for c in negativos)
                empatadas = [c for c in negativos if reducidos[c] == peor]
                entra, empate = empatadas[0], (empatadas if len(empatadas) > 1 else [])
            ciclo = self._ciclo(basicas, entra)

            # PASO 5: cantidad θ, celda que sale y actualización
            menos = ciclo[1::2]
            theta = min(asignaciones[c] for c in menos)
            empate_salida = [c for c in menos if asignaciones[c] == theta]
            sale = empate_salida[0]
            iteraciones.append(IteracionMODI(
                numero, dict(asignaciones), u, v, referencia, reducidos, False, costo, entra, empate,
                ciclo, theta, sale, empate_salida if len(empate_salida) > 1 else []))
            nuevas = dict(asignaciones)
            for posicion, celda in enumerate(ciclo):
                if posicion == 0:
                    nuevas[celda] = theta
                elif posicion % 2 == 0:
                    nuevas[celda] = nuevas[celda] + theta
                else:
                    nuevas[celda] = nuevas[celda] - theta
            del nuevas[sale]
            asignaciones = nuevas
            numero += 1

        final = iteraciones[-1]
        alternativas = [c for c, d in final.costos_reducidos.items() if d == 0]
        prohibidas = [c for c, x in asignaciones.items() if x > 0 and self.costos[c[0]][c[1]].tiene_m]
        resultado = ResultadoMODI(iteraciones, asignaciones, self.vogel.costo_total, final.costo, estado,
                                  alternativas, prohibidas)
        self._casos_especiales(resultado)
        return resultado

    # ------------------------------------------------------- casos especiales
    def _casos_especiales(self, r: ResultadoMODI) -> None:
        nombres_o, nombres_d = self.vogel.origenes, self.vogel.destinos
        if r.estado != ESTADO_OPTIMO:
            r.casos.append(CasoEspecial(INFORMATIVO, "Límite de revisiones",
                                        f"MODI se detuvo tras {self.MAX_ITERACIONES} revisiones.",
                                        NIVEL_ERROR))
            return
        if r.rutas_prohibidas_usadas:
            celdas = ", ".join(f"{nombres_o[i]} → {nombres_d[j]}" for i, j in r.rutas_prohibidas_usadas)
            r.casos.append(CasoEspecial(
                INFACTIBLE, "Sin solución con las rutas permitidas",
                f"Hasta la mejor solución necesita usar rutas prohibidas (costo M): {celdas}. Con las rutas "
                f"permitidas no se puede atender la demanda. Revise las rutas, la oferta o la demanda.", NIVEL_ERROR))
        elif r.vogel_es_optimo:
            r.casos.append(CasoEspecial(
                INFORMATIVO, "La solución de Vogel ya es la mejor",
                "Todos los d_ij de las celdas sin envío son 0 o más, así que ningún cambio baja el costo total.", NIVEL_EXITO))
        else:
            r.casos.append(CasoEspecial(
                INFORMATIVO, "Vogel se pudo mejorar con MODI",
                f"Costo con Vogel = {texto_numero(r.costo_inicial)}; mejor costo = "
                f"{texto_numero(r.costo_optimo)}; ahorro = {texto_numero(r.ahorro)} en "
                f"{len(r.iteraciones) - 1} mejora(s).", NIVEL_INFO))
        if r.celdas_alternativas:
            celdas = ", ".join(f"({nombres_o[i]}, {nombres_d[j]})" for i, j in r.celdas_alternativas)
            r.casos.append(CasoEspecial(
                OPTIMOS_ALTERNATIVOS, "Hay otra solución igual de buena",
                f"Las celdas sin envío {celdas} tienen d_ij = 0: se puede cambiar la distribución sin "
                f"cambiar el costo total.", NIVEL_ADVERTENCIA))
        if any(it.theta == 0 for it in r.iteraciones if it.theta is not None):
            r.casos.append(CasoEspecial(
                DEGENERACION, "Mejora sin cambio de costo",
                "En alguna mejora θ = 0: cambió la distribución pero no el costo (efecto de la degeneración).",
                NIVEL_INFO))
