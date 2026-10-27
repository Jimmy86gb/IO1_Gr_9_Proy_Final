"""
controlador/controlador_simplex.py
==================================
Controlador del método Simplex: recibe las acciones de la pantalla (resolver,
cargar ejemplo, abrir, guardar, limpiar), usa el modelo y devuelve los
resultados a la vista.
"""
from __future__ import annotations

import re

from modelo import ErrorArchivo, ErrorValidacion
from modelo.simplex import AnalizadorSensibilidad, SolverSimplex, ValidadorPL
from vista.formato import FORMATO

TIPO = "simplex"
ESTADOS = {"optimo": "solución óptima", "no_acotado": "problema no acotado",
           "limite_iteraciones": "se alcanzó el límite de iteraciones"}


class ControladorSimplex:
    def __init__(self, vista, repositorio, cb_estado=None):
        self.vista = vista
        self.repositorio = repositorio
        self._cb_estado = cb_estado
        self.ejemplos = []
        self.vista.establecer_controlador(self)
        self._actualizar_ejemplos()

    # ------------------------------------------------------------- ejemplos
    def _actualizar_ejemplos(self) -> None:
        self.ejemplos = self.repositorio.listar_ejemplos(TIPO)
        self.vista.panel_datos.establecer_ejemplos([titulo for titulo, _ in self.ejemplos])

    def cargar_caso_real_por_defecto(self) -> None:
        if self.ejemplos:
            self.cargar_ejemplo(0)

    def cargar_ejemplo(self, indice) -> None:
        if indice is None or not 0 <= indice < len(self.ejemplos):
            self.vista.mostrar_mensaje("Ejemplos", "Elija primero un ejemplo de la lista.", "advertencia")
            return
        titulo, ruta = self.ejemplos[indice]
        self._cargar_archivo(ruta, f"Ejemplo cargado: {titulo}")

    def abrir_archivo(self) -> None:
        ruta = self.vista.pedir_archivo_abrir(self.repositorio.carpeta(TIPO))
        if ruta:
            self._cargar_archivo(ruta, "Problema abierto desde archivo.")

    def _cargar_archivo(self, ruta, mensaje: str) -> None:
        try:
            datos = self.repositorio.cargar(ruta)
        except ErrorArchivo as error:
            self.vista.mostrar_mensaje("No se pudo abrir el archivo", str(error), "error")
            return
        self.vista.panel_datos.cargar_datos(datos)
        self.vista.cuaderno.select(self.vista.panel_datos)
        self._estado(mensaje + " Pulse «Resolver con Simplex».")

    def guardar_archivo(self) -> None:
        datos = self.vista.panel_datos.obtener_datos()
        nombre = re.sub(r"[^\w\-]+", "_", datos.get("nombre", "")).strip("_") or "problema"
        ruta = self.vista.pedir_archivo_guardar(self.repositorio.carpeta(TIPO), nombre + ".json")
        if not ruta:
            return
        try:
            self.repositorio.guardar(ruta, datos)
        except ErrorArchivo as error:
            self.vista.mostrar_mensaje("No se pudo guardar el archivo", str(error), "error")
            return
        self._actualizar_ejemplos()
        self._estado(f"Problema guardado en {ruta}")

    def limpiar(self) -> None:
        self.vista.panel_datos.limpiar_formulario()
        self._estado("Formulario reiniciado.")

    # -------------------------------------------------------------- resolver
    def resolver(self) -> None:
        panel = self.vista.panel_datos
        panel.limpiar_errores()
        try:
            problema = ValidadorPL().validar(panel.obtener_datos())
        except ErrorValidacion as error:
            panel.marcar_errores(error.campos)
            self.vista.mostrar_mensaje("Revise los datos", "\n\n".join("• " + m for m in error.mensajes), "error")
            self._estado("Hay datos por corregir antes de resolver.")
            return
        try:
            resultado = SolverSimplex(problema).resolver()
            sensibilidad = AnalizadorSensibilidad(resultado).analizar() if resultado.es_optimo else None
            self.vista.mostrar_resultado(resultado, sensibilidad)
        except Exception as error:  # el programa no debe cerrarse por un fallo inesperado
            self.vista.mostrar_mensaje("Error inesperado", f"No fue posible resolver el problema:\n{error}", "error")
            self._estado("Error al resolver el problema.")
            return
        self._estado(f"Simplex resuelto: {ESTADOS.get(resultado.estado, resultado.estado)}, "
                     f"{resultado.numero_pivoteos} pivoteos.")

    def _estado(self, mensaje: str) -> None:
        if callable(self._cb_estado):
            self._cb_estado(mensaje)
