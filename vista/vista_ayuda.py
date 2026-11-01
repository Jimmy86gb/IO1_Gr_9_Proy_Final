"""
vista/vista_ayuda.py
====================
Manual de uso dentro del programa.
"""
from __future__ import annotations

import tkinter as tk

from .componentes import TextoRico
from .tema import COLORES

AYUDA = [
    ("Manual de uso\n", "titulo"),
    ("1. Método Simplex (maximizar / minimizar)\n", "subtitulo"),
    ("• En «1 · Datos» escriba el nombre del problema, elija Maximizar o Minimizar y escriba qué mide z y su "
     "unidad (ej. «Utilidad semanal» en «COP/semana»).\n", "vineta"),
    ("• Elija el número de variables y de restricciones (1 a 8). Para cada variable escriba su nombre, su unidad "
     "y su coeficiente c_j (cuánto aporta a z cada unidad).\n", "vineta"),
    ("• Para cada restricción escriba su nombre, los coeficientes a_ij (cuánto recurso usa una unidad de cada "
     "variable), el valor disponible b_i y la unidad del recurso. Todas las restricciones son ≤ y b_i ≥ 0.\n",
     "vineta"),
    ("• Pulse «Resolver con Simplex». Revise: 2 · Modelo (forma estándar), 3 · Paso a paso (cada tabla con la "
     "variable que entra, la que sale y el pivote), 4 · Tablas (todas juntas), 5 · Solución, 6 · Sensibilidad y "
     "7 · Reporte.\n", "vineta"),
    ("\n2. Método de Vogel (transporte)\n", "subtitulo"),
    ("• En «1 · Datos» escriba la unidad del producto, la moneda, y el número de orígenes (de donde sale) y de "
     "destinos (a donde llega), de 1 a 8.\n", "vineta"),
    ("• En la tabla: arriba los destinos, a la izquierda los orígenes, en el centro el costo de enviar 1 unidad, "
     "a la derecha la oferta de cada origen y abajo la demanda de cada destino. Si una ruta está prohibida, escriba M.\n",
     "vineta"),
    ("• Debajo de la tabla se ve si el problema está balanceado. Si no lo está, el programa agrega solo un destino "
     "u origen ficticio con costo 0.\n", "vineta"),
    ("• Pulse «Resolver con Vogel». Revise: 2 · Modelo, 3 · Paso a paso (penalizaciones y celda escogida), "
     "4 · Tablas, 5 · Solución (envíos y costo total), 6 · MODI (compara con la mejor solución) y 7 · Reporte.\n",
     "vineta"),
    ("\n3. Cómo escribir los números\n", "subtitulo"),
    ("• Se aceptan: 12   -3   2.5   2,5   3/4   1e3. No use separador de miles (escriba 1250000, no 1.250.000).\n",
     "vineta"),
    ("• Si una casilla está vacía, tiene texto o un dato imposible (por ejemplo, un b negativo), el programa la "
     "marca en ROJO y explica el problema.\n", "vineta"),
    ("• En la barra lateral puede ver los resultados como fracciones exactas (5/3) o decimales (1.6667).\n", "vineta"),
    ("\n4. Casos especiales que el programa avisa\n", "subtitulo"),
    ("• Simplex: NO ACOTADO (ningún a_ik > 0 en la columna que entra), ÓPTIMOS ALTERNATIVOS (Cj − Zj = 0 en una no "
     "básica; se muestra la otra solución), DEGENERACIÓN (empate en la razón mínima o básica = 0) y ciclaje (regla "
     "de Bland).\n", "vineta"),
    ("• Sensibilidad: rangos infinitos (∞) y restricciones sin holgura (activas).\n", "vineta"),
    ("• Vogel: problema desbalanceado (origen o destino ficticio), empates entre penalizaciones, degeneración "
     "(menos envíos de los necesarios), rutas prohibidas (M) y problema sin solución.\n", "vineta"),
    ("\n5. Ejemplos y archivos\n", "subtitulo"),
    ("• Use la lista «Ejemplos» para probar los problemas de prueba.\n", "vineta"),
    ("• Con «Guardar…» puede guardar su problema como archivo .json; si lo guarda en la carpeta ejemplos/simplex/ "
     "(o ejemplos/transporte/ para Vogel) aparecerá en la lista de ejemplos. Con «Abrir…» carga un problema guardado.\n", "vineta"),
    ("\n6. Atajos de teclado\n", "subtitulo"),
    ("• Ctrl + Enter o F5: resolver el problema de la pantalla actual.   • Enter: pasar a la siguiente casilla.   "
     "• F1: abrir esta ayuda.\n", "vineta"),

    ("\nImportante: el programa no usa librerías que resuelvan el problema (SciPy, PuLP, OR-Tools, Solver de Excel...). "
     "Todo está programado desde cero; esas herramientas solo se usan aparte para verificar los resultados en el "
     "informe.\n", "info"),
]


class VistaAyuda(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=COLORES["fondo"])
        texto = TextoRico(self, alto=30)
        texto.pack(fill="both", expand=True, padx=24, pady=18)
        texto.mostrar(AYUDA)
