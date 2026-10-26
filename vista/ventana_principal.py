"""
vista/ventana_principal.py
==========================
Ventana raíz: barra lateral con la navegación y el formato de los números,
zona central donde se apilan las pantallas y barra de estado.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .componentes.widgets import instalar_rueda_global
from .formato import FORMATO, MODO_DECIMAL, MODO_FRACCION
from .tema import COLORES, FUENTES, aplicar_tema, px

OPCIONES_NAVEGACION = (("inicio", "Inicio"), ("simplex", "Método Simplex"), ("ayuda", "Ayuda"))


class VentanaPrincipal(tk.Tk):
    def __init__(self, al_navegar=None):
        super().__init__()
        self._al_navegar = al_navegar
        self._botones_nav = {}
        self.title("IO1 · Grupo 9 — Método Simplex")
        self.geometry(f"{min(1360, self.winfo_screenwidth() - 40)}x{min(840, self.winfo_screenheight() - 100)}")
        self.minsize(1040, 600)
        aplicar_tema(self)
        instalar_rueda_global(self)
        self._construir()

    def _construir(self):
        # Barra de estado (se empaqueta primero para que quede siempre abajo)
        self._mensaje_estado = tk.StringVar(value="Listo.")
        barra = tk.Frame(self, bg=COLORES["lateral"], highlightbackground=COLORES["borde_fuerte"],
                         highlightthickness=1)
        barra.pack(side="bottom", fill="x")
        tk.Label(barra, textvariable=self._mensaje_estado, font=FUENTES["pequena"], bg=COLORES["lateral"],
                 fg=COLORES["lateral_texto"], anchor="w").pack(fill="x", padx=12, pady=3)

        # Barra lateral
        lateral = tk.Frame(self, bg=COLORES["lateral"], width=px(176))
        lateral.pack(side="left", fill="y")
        lateral.pack_propagate(False)
        tk.Label(lateral, text="IO1 · Grupo 9", font=FUENTES["logo"], bg=COLORES["lateral"],
                 fg=COLORES["lateral_titulo"], anchor="w").pack(fill="x", padx=16, pady=(16, 0))
        tk.Label(lateral, text="Investigación de\nOperaciones I", font=FUENTES["mini"], bg=COLORES["lateral"],
                 fg=COLORES["lateral_tenue"], anchor="w", justify="left").pack(fill="x", padx=16, pady=(0, 14))
        for clave, texto in OPCIONES_NAVEGACION:
            boton = tk.Button(lateral, text=texto, font=FUENTES["lateral"], anchor="w", relief="flat", bd=0,
                              padx=16, pady=7, cursor="hand2", bg=COLORES["lateral"], fg=COLORES["lateral_texto"],
                              activebackground=COLORES["lateral_hover"], activeforeground=COLORES["lateral_texto"],
                              command=lambda k=clave: self._navegar(k))
            boton.pack(fill="x")
            self._botones_nav[clave] = boton

        tk.Label(lateral, text="Números", font=FUENTES["pequena_negrita"], bg=COLORES["lateral"],
                 fg=COLORES["lateral_texto"], anchor="w").pack(fill="x", padx=16, pady=(24, 4))
        self._var_modo = tk.StringVar(value=FORMATO.modo)
        for valor, texto in ((MODO_FRACCION, "Fracciones (5/3)"), (MODO_DECIMAL, "Decimales (1.6667)")):
            ttk.Radiobutton(lateral, text=texto, value=valor, variable=self._var_modo,
                            style="Lateral.TRadiobutton",
                            command=lambda: FORMATO.cambiar_modo(self._var_modo.get())).pack(
                fill="x", padx=16, pady=2)

        # Zona central
        self.contenedor_central = tk.Frame(self, bg=COLORES["fondo"])
        self.contenedor_central.pack(side="right", fill="both", expand=True)

    def _navegar(self, clave: str):
        if callable(self._al_navegar):
            self._al_navegar(clave)

    def resaltar_boton_nav(self, clave_activa: str):
        for clave, boton in self._botones_nav.items():
            activo = clave == clave_activa
            boton.configure(bg=COLORES["lateral_activo"] if activo else COLORES["lateral"],
                            font=FUENTES["lateral_negrita"] if activo else FUENTES["lateral"])

    def actualizar_estado(self, mensaje: str):
        self._mensaje_estado.set(mensaje)
