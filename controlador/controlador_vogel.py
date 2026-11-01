"""
controlador/controlador_vogel.py
================================
Recibe las acciones de la pantalla de Vogel (resolver, cargar ejemplo,
abrir, guardar, limpiar), llama al modelo y devuelve el resultado a la vista.
"""
from __future__ import annotations

import re

from modelo import ErrorArchivo, ErrorValidacion
from modelo.transporte import OptimizadorMODI, SolverVogel, ValidadorTransporte
from vista.formato import FORMATO

TIPO = "transporte"


class ControladorVogel:
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

    def cargar_primer_ejemplo(self) -> None:
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
        if datos.get("tipo") not in (None, TIPO):
            self.vista.mostrar_mensaje("Archivo equivocado",
                                       "Este archivo es de un problema de Simplex. Ábralo en «Método Simplex».",
                                       "advertencia")
            return
        self.vista.panel_datos.cargar_datos(datos)
        self.vista.cuaderno.select(self.vista.panel_datos)
        self.vista.datos_nuevos()
        self._estado(mensaje + " Pulse «Resolver con Vogel».")

    def guardar_archivo(self) -> None:
        datos = self.vista.panel_datos.obtener_datos()
        nombre = re.sub(r"[^\w\-]+", "_", datos.get("nombre", "")).strip("_") or "transporte"
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
        self.vista.datos_nuevos()
        self._estado("Formulario reiniciado.")

    # -------------------------------------------------------------- resolver
    def resolver(self) -> None:
        panel = self.vista.panel_datos
        panel.limpiar_errores()
        try:
            problema = ValidadorTransporte().validar(panel.obtener_datos())
        except ErrorValidacion as error:
            panel.marcar_errores(error.campos)
            self.vista.cuaderno.select(panel)
            mensajes = error.mensajes
            texto = "\n\n".join("• " + m for m in mensajes[:10])
            if len(mensajes) > 10:
                texto += f"\n\n… y {len(mensajes) - 10} errores más."
            self.vista.mostrar_mensaje("Revise los datos", texto, "error")
            self._estado("Hay datos por corregir antes de resolver.")
            return
        try:
            resultado = SolverVogel(problema).resolver()
            modi = OptimizadorMODI(resultado).resolver()
            self.vista.mostrar_resultado(resultado, modi)
        except Exception as error:  # el programa no debe cerrarse por un fallo inesperado
            self.vista.mostrar_mensaje("Error inesperado", f"No fue posible resolver el problema:\n{error}", "error")
            self._estado("Error al resolver el problema.")
            return
        self._estado(f"Vogel resuelto: costo total {FORMATO.num(resultado.costo_total)} "
                     f"{problema.unidad_costo}, {len(resultado.pasos)} pasos.")

    def _estado(self, mensaje: str) -> None:
        if callable(self._cb_estado):
            self._cb_estado(mensaje)
