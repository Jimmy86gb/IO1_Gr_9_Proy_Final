"""
vista/vista_inicio.py
=====================
Pantalla de inicio: qué hace el programa y botones para ir a cada método.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .componentes import Tarjeta
from .tema import COLORES, FUENTES

SIMPLEX = [
    "Maximiza o minimiza con 1 a 8 variables y 1 a 8 restricciones de tipo ≤.",
    "Muestra cada tabla con la variable que entra, la que sale y el pivote.",
    "Avisa los casos especiales: sin límite, degeneración y óptimos alternativos.",
    "Incluye el análisis de sensibilidad (precios sombra y rangos).",
    "Trae el caso real de concreto (Cementos Argos) y otros ejemplos.",
]
VOGEL = [
    "Minimiza el costo de transporte con hasta 8 orígenes y 8 destinos.",
    "Funciona con problemas balanceados o no (agrega un origen o destino ficticio).",
    "Muestra las penalizaciones de cada paso y la celda escogida.",
    "Compara con la mejor solución posible (MODI) y avisa si hay rutas prohibidas.",
    "Trae el caso real de despacho de concreto (Cementos Argos) y otros ejemplos.",
]


class VistaInicio(tk.Frame):
    def __init__(self, master, ir_a_simplex=None, cargar_caso_real_simplex=None, ir_a_vogel=None,
                 cargar_caso_real_vogel=None, ir_a_ayuda=None):
        super().__init__(master, bg=COLORES["fondo"])
        contenedor = tk.Frame(self, bg=COLORES["fondo"])
        contenedor.pack(fill="both", expand=True, padx=24, pady=20)

        tk.Label(contenedor, text="Proyecto final · Investigación de Operaciones I · Grupo 9",
                 font=FUENTES["pequena"], bg=COLORES["fondo"], fg=COLORES["texto_suave"], anchor="w").pack(fill="x")
        tk.Label(contenedor, text="Método Simplex y método de Vogel", font=FUENTES["titulo"],
                 bg=COLORES["fondo"], fg=COLORES["texto"], anchor="w").pack(fill="x", pady=(2, 14))

        for titulo, puntos, abrir, caso, texto_caso in (
                ("Método Simplex (programación lineal)", SIMPLEX, ir_a_simplex, cargar_caso_real_simplex,
                 "Cargar y resolver el caso real"),
                ("Método de Vogel (transporte)", VOGEL, ir_a_vogel, cargar_caso_real_vogel,
                 "Cargar y resolver el caso real")):
            tarjeta = Tarjeta(contenedor, titulo)
            tarjeta.pack(fill="x", pady=(0, 12))
            for punto in puntos:
                tk.Label(tarjeta.cuerpo, text="•  " + punto, font=FUENTES["base"], bg=COLORES["superficie"],
                         fg=COLORES["texto"], anchor="w", justify="left", wraplength=820).pack(fill="x", pady=2)
            botones = tk.Frame(tarjeta.cuerpo, bg=COLORES["superficie"])
            botones.pack(fill="x", pady=(8, 0))
            ttk.Button(botones, text="Abrir", style="Primario.TButton",
                       command=lambda f=abrir: f() if f else None).pack(side="left", padx=(0, 8))
            ttk.Button(botones, text=texto_caso,
                       command=lambda f=caso: f() if f else None).pack(side="left")

        ttk.Button(contenedor, text="Ver la ayuda",
                   command=lambda: ir_a_ayuda() if ir_a_ayuda else None).pack(anchor="w", pady=(4, 0))
