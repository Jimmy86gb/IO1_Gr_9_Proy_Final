"""
vista/componentes/panel_reporte.py
==================================
Muestra en pantalla el informe completo del problema resuelto (solo lectura).
El texto se puede seleccionar y copiar con Ctrl + C.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..tema import COLORES, FUENTES

MENSAJE_VACIO = ("Todavía no hay informe.\n\n"
                 "Escriba los datos (o cargue un ejemplo) y pulse «Resolver con Simplex»; "
                 "el informe completo aparecerá aquí.")


class PanelReporte(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=COLORES["fondo"])
        marco = tk.Frame(self, bg=COLORES["superficie"], highlightbackground=COLORES["borde"], highlightthickness=1)
        marco.pack(fill="both", expand=True, padx=14, pady=12)
        self.texto = tk.Text(marco, wrap="none", font=FUENTES["mono"], bg=COLORES["superficie"],
                             fg=COLORES["texto"], relief="flat", bd=0, padx=12, pady=10, highlightthickness=0,
                             selectbackground=COLORES["primario_suave"], selectforeground=COLORES["texto"],
                             state="disabled")
        barra_v = ttk.Scrollbar(marco, orient="vertical", command=self.texto.yview)
        barra_h = ttk.Scrollbar(marco, orient="horizontal", command=self.texto.xview)
        self.texto.configure(yscrollcommand=barra_v.set, xscrollcommand=barra_h.set)
        self.texto.grid(row=0, column=0, sticky="nsew")
        barra_v.grid(row=0, column=1, sticky="ns")
        barra_h.grid(row=1, column=0, sticky="ew")
        marco.grid_rowconfigure(0, weight=1)
        marco.grid_columnconfigure(0, weight=1)
        self.limpiar()

    def mostrar(self, contenido: str) -> None:
        self.texto.configure(state="normal")
        self.texto.delete("1.0", "end")
        self.texto.insert("1.0", contenido)
        self.texto.configure(state="disabled")
        self.texto.yview_moveto(0)
        self.texto.xview_moveto(0)

    def limpiar(self) -> None:
        self.mostrar(MENSAJE_VACIO)
