"""
modelo/transporte/solver_vogel.py
=================================
Método de aproximación de Vogel, programado desde cero.

  0. Si la oferta total y la demanda total no son iguales, se agrega un
     destino ficticio (sobra oferta) o un origen ficticio (falta oferta)
     con costo 0.
  1. Cada fila y cada columna recibe una penalización:
     segundo costo más bajo − costo más bajo.
  2. Se elige la fila o columna con la MAYOR penalización. Si hay empate:
     la de menor costo, luego la que permita enviar más, luego la primera.
  3. En esa fila o columna se usa la celda de MENOR costo y se envía lo
     máximo posible: x = mín(oferta, demanda).
  4. Se tacha la fila o columna que quedó completa. Si se completan las
     dos a la vez (degeneración), solo se tacha una.
  5. Si solo queda una fila o columna, se llena por costo mínimo.
  6. Se repite hasta terminar. Costo total = suma de costo × cantidad.

Vogel da una buena solución inicial, pero no siempre es la mejor.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from fractions import Fraction

from ..caso_especial import (DEGENERACION, DESBALANCE, EMPATE, INFORMATIVO, NIVEL_ADVERTENCIA,
                             NIVEL_INFO, RUTA_PROHIBIDA, CasoEspecial)
from ..numeros import ValorM, texto_numero
from .problema_transporte import ProblemaTransporte

FILA = "fila"
COLUMNA = "columna"

MODO_PENALIZACION = "penalizacion"     # pasos normales
MODO_UNICA_FILA = "unica_fila"         # queda una sola fila
MODO_UNICA_COLUMNA = "unica_columna"   # queda una sola columna
MODO_CEROS = "ceros"                   # ya no queda nada por enviar

CRITERIO_MENOR_COSTO = "menor_costo"
CRITERIO_MAYOR_ASIGNACION = "mayor_asignacion"
CRITERIO_ORDEN = "orden"


@dataclass
class PenalizacionLinea:
    tipo: str                    # FILA o COLUMNA
    indice: int
    menor: ValorM                # costo más bajo
    segundo: ValorM | None       # segundo costo más bajo
    penalizacion: ValorM | None  # segundo − más bajo
    costos_activos: list = field(default_factory=list)


@dataclass
class PasoVogel:
    numero: int
    modo: str
    filas_activas: list[int]
    columnas_activas: list[int]
    oferta_antes: list[Fraction]
    demanda_antes: list[Fraction]
    penalizaciones_filas: dict
    penalizaciones_columnas: dict
    linea: tuple | None                  # (FILA o COLUMNA, número) elegida
    empate_lineas: list                  # filas/columnas empatadas en la mayor penalización
    criterio_desempate: str | None
    celda: tuple[int, int]
    costo: ValorM
    cantidad: Fraction
    empate_celdas: list
    criterio_celda: str | None
    tachada: tuple                       # fila o columna tachada en este paso
    simultaneo: bool                     # fila y columna completas a la vez
    asignaciones: dict                   # envíos DESPUÉS del paso {(i, j): cantidad}
    oferta_despues: list[Fraction]
    demanda_despues: list[Fraction]


@dataclass
class ResultadoVogel:
    problema: ProblemaTransporte
    origenes: list[str]                  # incluye el ficticio si se agregó
    destinos: list[str]
    oferta: list[Fraction]
    demanda: list[Fraction]
    costos: list[list[ValorM]]
    ficticio: str | None                 # "origen", "destino" o None
    cantidad_ficticia: Fraction
    pasos: list[PasoVogel]
    asignaciones: dict                   # envíos {(i, j): cantidad} (incluye ceros)
    costo_total: ValorM
    casos: list[CasoEspecial]
    celdas_cero: list
    rutas_prohibidas_usadas: list
    tiempo_ms: float = 0.0

    @property
    def m(self) -> int:
        return len(self.origenes)

    @property
    def n(self) -> int:
        return len(self.destinos)

    @property
    def es_degenerada(self) -> bool:
        return bool(self.celdas_cero)

    def es_fila_ficticia(self, i: int) -> bool:
        return self.ficticio == "origen" and i == self.m - 1

    def es_columna_ficticia(self, j: int) -> bool:
        return self.ficticio == "destino" and j == self.n - 1

    def envios(self) -> list[tuple[int, int, Fraction, ValorM]]:
        """(i, j, cantidad, costo de la ruta) de las asignaciones positivas, en orden de filas."""
        return [(i, j, x, self.costos[i][j] * x) for (i, j), x in sorted(self.asignaciones.items()) if x > 0]


class SolverVogel:
    """Aplica el método de Vogel a un ``ProblemaTransporte``."""

    def __init__(self, problema: ProblemaTransporte):
        self.problema = problema

    # ------------------------------------------------------- PASO 0: balanceo
    def _balancear(self):
        p = self.problema
        origenes, destinos = list(p.origenes), list(p.destinos)
        oferta, demanda = list(p.oferta), list(p.demanda)
        costos = [list(fila) for fila in p.costos]
        diferencia = p.total_oferta - p.total_demanda
        ficticio = None
        if diferencia > 0:                                    # sobra oferta
            destinos.append(self._nombre_libre("Destino ficticio", destinos))
            demanda.append(diferencia)
            for fila in costos:
                fila.append(ValorM(0))
            ficticio = "destino"
        elif diferencia < 0:                                  # falta oferta
            origenes.append(self._nombre_libre("Origen ficticio", origenes))
            oferta.append(-diferencia)
            costos.append([ValorM(0) for _ in destinos])
            ficticio = "origen"
        return origenes, destinos, oferta, demanda, costos, ficticio, abs(diferencia)

    @staticmethod
    def _nombre_libre(base: str, existentes: list[str]) -> str:
        nombre, k = base, 2
        while nombre.lower() in (e.lower() for e in existentes):
            nombre = f"{base} {k}"
            k += 1
        return nombre

    # ------------------------------------------------- PASO 1: penalizaciones
    @staticmethod
    def _penalizacion(tipo, indice, costos_activos) -> PenalizacionLinea:
        ordenados = sorted(costos_activos)
        menor = ordenados[0]
        segundo = ordenados[1] if len(ordenados) > 1 else None
        penalizacion = (segundo - menor) if segundo is not None else None
        return PenalizacionLinea(tipo, indice, menor, segundo, penalizacion, list(costos_activos))

    # ----------------------------------------- PASO 3: celda de menor costo
    @staticmethod
    def _elegir_celda(candidatas, costos, oferta, demanda):
        menor = min(costos[i][j] for i, j in candidatas)
        empatadas = [(i, j) for i, j in candidatas if costos[i][j] == menor]
        if len(empatadas) == 1:
            return empatadas[0], [], None
        mayor = max(min(oferta[i], demanda[j]) for i, j in empatadas)
        empatadas2 = [(i, j) for i, j in empatadas if min(oferta[i], demanda[j]) == mayor]
        criterio = CRITERIO_MAYOR_ASIGNACION if len(empatadas2) == 1 else CRITERIO_ORDEN
        return empatadas2[0], empatadas, criterio

    @staticmethod
    def _celdas_de_linea(linea, filas, columnas):
        tipo, k = linea
        return [(k, j) for j in columnas] if tipo == FILA else [(i, k) for i in filas]

    # ------------------------------------- PASO 2: línea de mayor penalización
    def _elegir_linea(self, penal_filas, penal_columnas, costos, oferta, demanda, filas, columnas):
        lineas = [(FILA, i) for i in filas] + [(COLUMNA, j) for j in columnas]

        def info(linea):
            return penal_filas[linea[1]] if linea[0] == FILA else penal_columnas[linea[1]]

        maxima = max(info(l).penalizacion for l in lineas)
        empatadas = [l for l in lineas if info(l).penalizacion == maxima]
        if len(empatadas) == 1:
            return empatadas[0], [], None
        # a) desempata el menor costo
        menor = min(info(l).menor for l in empatadas)
        empatadas2 = [l for l in empatadas if info(l).menor == menor]
        if len(empatadas2) == 1:
            return empatadas2[0], empatadas, CRITERIO_MENOR_COSTO

        # b) desempata la mayor cantidad que se puede enviar
        def asignable(linea):
            celda, _, _ = self._elegir_celda(self._celdas_de_linea(linea, filas, columnas),
                                             costos, oferta, demanda)
            return min(oferta[celda[0]], demanda[celda[1]])

        mayor = max(asignable(l) for l in empatadas2)
        empatadas3 = [l for l in empatadas2 if asignable(l) == mayor]
        if len(empatadas3) == 1:
            return empatadas3[0], empatadas, CRITERIO_MAYOR_ASIGNACION
        # c) la primera (filas antes que columnas)
        return empatadas3[0], empatadas, CRITERIO_ORDEN

    # --------------------------------------------------------------- resolver
    def resolver(self) -> ResultadoVogel:
        inicio = time.perf_counter()
        origenes, destinos, oferta, demanda, costos, ficticio, cantidad_ficticia = self._balancear()
        m, n = len(origenes), len(destinos)
        filas, columnas = list(range(m)), list(range(n))    # filas y columnas sin tachar
        s, d = list(oferta), list(demanda)                   # oferta y demanda que quedan
        asignaciones: dict = {}
        pasos: list[PasoVogel] = []
        numero = 1

        # PASO 6: repetir mientras quede más de una fila o columna
        while len(filas) + len(columnas) > 1:
            filas_antes, columnas_antes = list(filas), list(columnas)
            oferta_antes, demanda_antes = list(s), list(d)
            penal_filas, penal_columnas = {}, {}
            linea, empate_lineas, criterio = None, [], None

            if len(filas) == 1:                               # PASO 5: una sola fila
                modo = MODO_UNICA_FILA
                linea = (FILA, filas[0])
                candidatas = self._celdas_de_linea(linea, filas, columnas)
            elif len(columnas) == 1:                          # PASO 5: una sola columna
                modo = MODO_UNICA_COLUMNA
                linea = (COLUMNA, columnas[0])
                candidatas = self._celdas_de_linea(linea, filas, columnas)
            elif all(s[i] == 0 for i in filas) and all(d[j] == 0 for j in columnas):
                modo = MODO_CEROS                             # PASO 5: solo quedan ceros
                candidatas = [(i, j) for i in filas for j in columnas]
            else:
                modo = MODO_PENALIZACION
                # PASO 1: penalización de cada fila y columna
                for i in filas:
                    penal_filas[i] = self._penalizacion(FILA, i, [costos[i][j] for j in columnas])
                for j in columnas:
                    penal_columnas[j] = self._penalizacion(COLUMNA, j, [costos[i][j] for i in filas])
                # PASO 2: elegir la mayor penalización
                linea, empate_lineas, criterio = self._elegir_linea(
                    penal_filas, penal_columnas, costos, s, d, filas, columnas)
                candidatas = self._celdas_de_linea(linea, filas, columnas)

            # PASO 3: celda más barata y asignación máxima posible
            celda, empate_celdas, criterio_celda = self._elegir_celda(candidatas, costos, s, d)
            i, j = celda
            cantidad = min(s[i], d[j])
            asignaciones[(i, j)] = cantidad
            s[i] -= cantidad
            d[j] -= cantidad

            # PASO 4: tachar SOLO UNA
            simultaneo = s[i] == 0 and d[j] == 0
            if simultaneo:
                if len(filas) == 1:
                    tachada = (COLUMNA, j)
                elif len(columnas) == 1:
                    tachada = (FILA, i)
                elif linea is not None:
                    tachada = linea
                else:
                    tachada = (FILA, i)
            elif s[i] == 0:
                tachada = (FILA, i)
            else:
                tachada = (COLUMNA, j)
            if tachada[0] == FILA:
                filas.remove(tachada[1])
            else:
                columnas.remove(tachada[1])

            pasos.append(PasoVogel(
                numero, modo, filas_antes, columnas_antes, oferta_antes, demanda_antes,
                penal_filas, penal_columnas, linea, empate_lineas, criterio, celda, costos[i][j],
                cantidad, empate_celdas, criterio_celda, tachada, simultaneo, dict(asignaciones),
                list(s), list(d)))
            numero += 1

        costo_total = sum((costos[i][j] * x for (i, j), x in asignaciones.items()), ValorM(0))
        celdas_cero = [c for c, x in asignaciones.items() if x == 0]
        prohibidas = [c for c, x in asignaciones.items() if x > 0 and costos[c[0]][c[1]].tiene_m]
        resultado = ResultadoVogel(self.problema, origenes, destinos, oferta, demanda, costos, ficticio,
                                   cantidad_ficticia, pasos, asignaciones, costo_total, [], celdas_cero,
                                   prohibidas)
        self._casos_especiales(resultado)
        resultado.tiempo_ms = (time.perf_counter() - inicio) * 1000
        return resultado

    # ------------------------------------------------------- casos especiales
    def _casos_especiales(self, r: ResultadoVogel) -> None:
        p = self.problema
        u = p.unidad_producto

        # a) Problema no balanceado
        if r.ficticio == "destino":
            recibe = [f"{r.origenes[i]} ({texto_numero(x)} {u})" for (i, j), x in sorted(r.asignaciones.items())
                      if j == r.n - 1 and x > 0]
            r.casos.append(CasoEspecial(
                DESBALANCE, "Problema NO balanceado: sobra oferta",
                f"Oferta total = {texto_numero(p.total_oferta)} {u} y demanda total = "
                f"{texto_numero(p.total_demanda)} {u}. Se agregó «{r.destinos[-1]}» con demanda "
                f"{texto_numero(r.cantidad_ficticia)} {u} y costo 0. Lo asignado a ese destino NO se envía "
                f"(se queda en el origen)"
                + (": " + ", ".join(recibe) + "." if recibe else "."), NIVEL_ADVERTENCIA))
        elif r.ficticio == "origen":
            envia = [f"{r.destinos[j]} ({texto_numero(x)} {u})" for (i, j), x in sorted(r.asignaciones.items())
                     if i == r.m - 1 and x > 0]
            r.casos.append(CasoEspecial(
                DESBALANCE, "Problema NO balanceado: falta oferta",
                f"Demanda total = {texto_numero(p.total_demanda)} {u} y oferta total = "
                f"{texto_numero(p.total_oferta)} {u}. Se agregó «{r.origenes[-1]}» con oferta "
                f"{texto_numero(r.cantidad_ficticia)} {u} y costo 0. Lo que «envía» ese origen es "
                f"DEMANDA SIN ATENDER"
                + (": " + ", ".join(envia) + "." if envia else "."), NIVEL_ADVERTENCIA))

        # b) Empates
        empates = []
        for paso in r.pasos:
            if paso.empate_lineas:
                lineas = ", ".join(self._nombre_linea(r, l) for l in paso.empate_lineas)
                empates.append(f"paso {paso.numero}: penalización {texto_numero(self._valor_pen(paso))} "
                               f"en {lineas} → se eligió {self._nombre_linea(r, paso.linea)} "
                               f"({self._texto_criterio(paso.criterio_desempate)})")
            if paso.empate_celdas:
                celdas = ", ".join(f"({r.origenes[i]}, {r.destinos[j]})" for i, j in paso.empate_celdas)
                empates.append(f"paso {paso.numero}: costo mínimo empatado en {celdas} → se eligió "
                               f"({r.origenes[paso.celda[0]]}, {r.destinos[paso.celda[1]]}) "
                               f"({self._texto_criterio(paso.criterio_celda)})")
        if empates:
            r.casos.append(CasoEspecial(
                EMPATE, "Empates",
                "Hubo empates y se desempataron con una regla fija (menor costo, más unidades y orden): " + "; ".join(empates) + ".", NIVEL_INFO))

        # c) Degeneración
        base_esperada = r.m + r.n - 1
        positivas = sum(1 for x in r.asignaciones.values() if x > 0)
        if r.celdas_cero:
            celdas = ", ".join(f"({r.origenes[i]}, {r.destinos[j]})" for i, j in r.celdas_cero)
            simultaneos = [str(paso.numero) for paso in r.pasos if paso.simultaneo and paso.cantidad > 0]
            r.casos.append(CasoEspecial(
                DEGENERACION, "Solución degenerada",
                f"Hay {positivas} envíos con cantidad y se necesitan {base_esperada} (filas + columnas − 1). "
                f"Se completó con envíos de 0 en: {celdas}"
                + (f" (en el/los paso(s) {', '.join(simultaneos)} una fila y una columna se completaron a la "
                   f"vez)" if simultaneos else "") + ".", NIVEL_ADVERTENCIA))

        # d) Rutas prohibidas (costo M)
        prohibidas = p.rutas_prohibidas()
        if r.rutas_prohibidas_usadas:
            celdas = ", ".join(f"{r.origenes[i]} → {r.destinos[j]} ({texto_numero(r.asignaciones[(i, j)])} {u})"
                               for i, j in r.rutas_prohibidas_usadas)
            r.casos.append(CasoEspecial(
                RUTA_PROHIBIDA, "La solución usa rutas PROHIBIDAS (M)",
                f"Vogel envió unidades por rutas con costo M: {celdas}. Mire la pestaña «6 · MODI»: si la "
                f"mejor solución también las usa, el problema no tiene solución con las rutas permitidas.", NIVEL_ADVERTENCIA))
        elif prohibidas:
            r.casos.append(CasoEspecial(
                RUTA_PROHIBIDA, "Rutas prohibidas respetadas",
                f"Hay {len(prohibidas)} ruta(s) con costo M y la solución no envía nada por ellas.",
                NIVEL_INFO))

        r.casos.append(CasoEspecial(
            INFORMATIVO, "Vogel da una solución inicial",
            "Vogel da una solución muy buena, pero no siempre la mejor. Compárela con la mejor posible "
            "en la pestaña «6 · MODI».",
            NIVEL_INFO))

    # ------------------------------------------------------------ auxiliares
    @staticmethod
    def _nombre_linea(r: ResultadoVogel, linea) -> str:
        tipo, k = linea
        return f"fila {r.origenes[k]}" if tipo == FILA else f"columna {r.destinos[k]}"

    @staticmethod
    def _valor_pen(paso: PasoVogel):
        tipo, k = paso.linea
        info = paso.penalizaciones_filas[k] if tipo == FILA else paso.penalizaciones_columnas[k]
        return info.penalizacion

    @staticmethod
    def _texto_criterio(criterio) -> str:
        return {CRITERIO_MENOR_COSTO: "criterio: menor costo",
                CRITERIO_MAYOR_ASIGNACION: "criterio: mayor asignación",
                CRITERIO_ORDEN: "criterio: primera en orden"}.get(criterio, "")
