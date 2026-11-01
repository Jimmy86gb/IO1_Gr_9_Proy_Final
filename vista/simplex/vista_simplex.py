"""
vista/simplex/vista_simplex.py
==============================
Pantalla completa del método Simplex: une todas las pestañas (datos, modelo,
paso a paso, tablas, solución, sensibilidad y reporte). Ofrece al controlador
métodos simples para mostrar resultados y errores.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..componentes.dialogos import DialogosMixin
from ..componentes.panel_reporte import PanelReporte
from ..formato import FORMATO
from ..reportes.reporte_simplex import texto_simplex
from ..tema import COLORES, FUENTES
from .panel_datos_simplex import PanelDatosSimplex
from .panel_iteraciones_simplex import PanelIteracionesSimplex, PanelTodasTablasSimplex
from .panel_resultados_simplex import PanelModeloSimplex, PanelSensibilidad, PanelSolucionSimplex


class VistaSimplex(DialogosMixin, tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=COLORES["fondo"])
        self.controlador = None
        self.resultado = None
        self.sensibilidad = None

        tk.Label(self, text="Escriba los datos o cargue un ejemplo y pulse «Resolver con Simplex».",
                 font=FUENTES["pequena"], bg=COLORES["fondo"], fg=COLORES["texto_suave"], anchor="w").pack(
            fill="x", padx=16, pady=(8, 0))

        self.cuaderno = ttk.Notebook(self)
        self.cuaderno.pack(fill="both", expand=True, padx=10, pady=(4, 8))
        self.panel_datos = PanelDatosSimplex(self.cuaderno)
        self.panel_modelo = PanelModeloSimplex(self.cuaderno)
        self.panel_pasos = PanelIteracionesSimplex(self.cuaderno)
        self.panel_tablas = PanelTodasTablasSimplex(self.cuaderno)
        self.panel_solucion = PanelSolucionSimplex(self.cuaderno)
        self.panel_sensibilidad = PanelSensibilidad(self.cuaderno)
        self.panel_reporte = PanelReporte(self.cuaderno)
        for panel, titulo in ((self.panel_datos, "1 · Datos"), (self.panel_modelo, "2 · Modelo"),
                              (self.panel_pasos, "3 · Paso a paso"), (self.panel_tablas, "4 · Tablas"),
                              (self.panel_solucion, "5 · Solución"), (self.panel_sensibilidad, "6 · Sensibilidad"),
                              (self.panel_reporte, "7 · Reporte")):
            self.cuaderno.add(panel, text=f"  {titulo}  ")

        # Al cambiar entre fracciones y decimales se vuelven a dibujar las pantallas de resultados
        for panel in (self.panel_modelo, self.panel_pasos, self.panel_tablas, self.panel_solucion,
                      self.panel_sensibilidad):
            FORMATO.suscribir(panel.refrescar)
        FORMATO.suscribir(self._refrescar_reporte)

    def establecer_controlador(self, controlador) -> None:
        self.controlador = controlador
        self.panel_datos.controlador = controlador

    # ------------------------------------------------------------ resultados
    def mostrar_resultado(self, resultado, sensibilidad) -> None:
        self.resultado = resultado
        self.sensibilidad = sensibilidad
        self.panel_modelo.mostrar(resultado.problema)
        self.panel_pasos.mostrar(resultado)
        self.panel_tablas.mostrar(resultado)
        self.panel_solucion.mostrar(resultado)
        if sensibilidad is not None:
            self.panel_sensibilidad.mostrar(sensibilidad)
        elif resultado.estado == "no_acotado":
            self.panel_sensibilidad.mostrar_mensaje(
                "No hay análisis de sensibilidad porque el problema no tiene una solución óptima finita "
                "(es no acotado).", "advertencia")
        else:
            self.panel_sensibilidad.mostrar_mensaje(
                "No hay análisis de sensibilidad porque el método se detuvo sin encontrar una solución óptima.",
                "advertencia")
        self._refrescar_reporte()
        self.cuaderno.select(self.panel_pasos)

    def _refrescar_reporte(self) -> None:
        if self.resultado is not None:
            self.panel_reporte.mostrar(texto_simplex(self.resultado, self.sensibilidad, FORMATO))
