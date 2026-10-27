"""
vista/vista_inicio.py
=====================
Pantalla de inicio: descripción del programa y accesos a las demás pantallas.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .componentes import Tarjeta
from .tema import COLORES, FUENTES

PUNTOS = [
    "Maximiza o minimiza con 1 a 8 variables de decisión y 1 a 8 restricciones de tipo ≤.",
    "Muestra cada tabla Simplex con la variable que entra, la que sale y el elemento pivote.",
    "Avisa y explica los casos especiales: problema no acotado, degeneración y óptimos alternativos.",
    "Incluye el análisis de sensibilidad (precios sombra, costos reducidos y rangos).",
    "Trae precargado el caso real de producción de concreto (Cementos Argos) y otros problemas de prueba.",
]


class VistaInicio(tk.Frame):
    def __init__(self, master, ir_a_simplex=None, cargar_caso_real_simplex=None, ir_a_ayuda=None):
        super().__init__(master, bg=COLORES["fondo"])
        contenedor = tk.Frame(self, bg=COLORES["fondo"])
        contenedor.pack(fill="both", expand=True, padx=24, pady=20)

        tk.Label(contenedor, text="Proyecto final · Investigación de Operaciones I · Grupo 9",
                 font=FUENTES["pequena"], bg=COLORES["fondo"], fg=COLORES["texto_suave"], anchor="w").pack(fill="x")
        tk.Label(contenedor, text="Programación lineal: método Simplex", font=FUENTES["titulo"],
                 bg=COLORES["fondo"], fg=COLORES["texto"], anchor="w").pack(fill="x", pady=(2, 14))

        tarjeta = Tarjeta(contenedor, "Qué hace el programa")
        tarjeta.pack(fill="x")
        for punto in PUNTOS:
            tk.Label(tarjeta.cuerpo, text="•  " + punto, font=FUENTES["base"], bg=COLORES["superficie"],
                     fg=COLORES["texto"], anchor="w", justify="left", wraplength=820).pack(fill="x", pady=2)

        botones = tk.Frame(contenedor, bg=COLORES["fondo"])
        botones.pack(fill="x", pady=(16, 0))
        ttk.Button(botones, text="Abrir el método Simplex", style="Primario.TButton",
                   command=lambda: ir_a_simplex() if ir_a_simplex else None).pack(side="left", padx=(0, 8))
        ttk.Button(botones, text="Cargar y resolver el caso real",
                   command=lambda: cargar_caso_real_simplex() if cargar_caso_real_simplex else None).pack(
            side="left", padx=(0, 8))
        ttk.Button(botones, text="Ver la ayuda",
                   command=lambda: ir_a_ayuda() if ir_a_ayuda else None).pack(side="left")
