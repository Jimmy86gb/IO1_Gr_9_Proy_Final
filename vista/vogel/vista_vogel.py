"""
vista/vogel/vista_vogel.py
==========================
Pantalla del método de Vogel. Junta las pestañas: datos, modelo, paso a
paso, tablas, solución, MODI y reporte. Es igual de simple que la del Simplex.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..componentes.dialogos import DialogosMixin
from ..componentes.panel_reporte import PanelReporte
from ..formato import FORMATO
from ..reportes.reporte_vogel import texto_vogel
from ..tema import COLORES, FUENTES
from .panel_datos_vogel import PanelDatosVogel
from .panel_pasos_vogel import PanelPasosVogel, PanelTodosPasosVogel
from .panel_resultados_vogel import PanelModi, PanelPlanteamientoVogel, PanelSolucionVogel

AYUDA_INICIAL = "Escriba la tabla de transporte o cargue un ejemplo y pulse «Resolver con Vogel»."


class VistaVogel(DialogosMixin, tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=COLORES["fondo"])
        self.controlador = None
        self.resultado = None
        self.modi = None

        self.franja = tk.Label(self, text=AYUDA_INICIAL, font=FUENTES["pequena"], bg=COLORES["fondo"],
                               fg=COLORES["texto_suave"], anchor="w", justify="left")
        self.franja.pack(fill="x", padx=16, pady=(8, 0))

        self.cuaderno = ttk.Notebook(self)
        self.cuaderno.pack(fill="both", expand=True, padx=10, pady=(4, 8))
        self.panel_datos = PanelDatosVogel(self.cuaderno)
        self.panel_planteamiento = PanelPlanteamientoVogel(self.cuaderno)
        self.panel_pasos = PanelPasosVogel(self.cuaderno)
        self.panel_todos = PanelTodosPasosVogel(self.cuaderno)
        self.panel_solucion = PanelSolucionVogel(self.cuaderno)
        self.panel_modi = PanelModi(self.cuaderno)
        self.panel_reporte = PanelReporte(self.cuaderno)
        for panel, titulo in ((self.panel_datos, "1 · Datos"), (self.panel_planteamiento, "2 · Modelo"),
                              (self.panel_pasos, "3 · Paso a paso"), (self.panel_todos, "4 · Tablas"),
                              (self.panel_solucion, "5 · Solución"), (self.panel_modi, "6 · MODI"),
                              (self.panel_reporte, "7 · Reporte")):
            self.cuaderno.add(panel, text=f"  {titulo}  ")
        FORMATO.suscribir(self.refrescar)

    def establecer_controlador(self, controlador) -> None:
        self.controlador = controlador
        self.panel_datos.controlador = controlador

    # ------------------------------------------------------------ resultados
    def mostrar_resultado(self, resultado, modi) -> None:
        self.resultado, self.modi = resultado, modi
        self.panel_planteamiento.mostrar(resultado)
        self.panel_pasos.mostrar(resultado)
        self.panel_todos.mostrar(resultado)
        self.panel_solucion.mostrar(resultado, modi)
        if modi is not None:
            self.panel_modi.mostrar(resultado, modi)
        self._actualizar_reporte()
        self._actualizar_franja()
        self.cuaderno.select(self.panel_pasos)

    def refrescar(self) -> None:
        """Se llama al cambiar entre fracciones y decimales."""
        if self.resultado is None:
            return
        for panel in (self.panel_planteamiento, self.panel_pasos, self.panel_todos, self.panel_solucion,
                      self.panel_modi):
            panel.refrescar()
        self._actualizar_reporte()
        self._actualizar_franja()

    def _actualizar_reporte(self) -> None:
        self.panel_reporte.mostrar(texto_vogel(self.resultado, self.modi, FORMATO))

    def _actualizar_franja(self) -> None:
        """Resume el resultado en una línea. Rojo = infactible, amarillo = caso especial, verde = normal."""
        r, modi = self.resultado, self.modi
        p = r.problema
        texto = f"Costo total con Vogel: {FORMATO.num(r.costo_total)} {p.unidad_costo} · {len(r.pasos)} pasos"
        infactible = modi is not None and modi.rutas_prohibidas_usadas
        if infactible:
            texto += " · NO tiene solución usando solo las rutas permitidas"
        elif modi is not None:
            texto += (" · Vogel ya es la mejor solución" if modi.vogel_es_optimo
                      else f" · mejor solución (MODI): {FORMATO.num(modi.costo_optimo)} {p.unidad_costo}")
        especiales = [c.titulo for c in r.casos if c.nivel in ("advertencia", "error")]
        if especiales:
            texto += "  ·  " + "; ".join(especiales)
        color = COLORES["error"] if infactible else (COLORES["advertencia"] if especiales else COLORES["exito"])
        self.franja.configure(text=texto, fg=color)

    def datos_nuevos(self) -> None:
        """Se llama al cargar o limpiar datos: los resultados mostrados ya no son de este problema."""
        texto = "Datos listos. Pulse «Resolver con Vogel»."
        if self.resultado is not None:
            texto += " Las otras pestañas todavía muestran el problema anterior."
        self.franja.configure(text=texto, fg=COLORES["texto_suave"])
