"""
vista/tema.py
=============
Tema visual de la aplicación: colores, fuentes y estilos ttk.
"""
from __future__ import annotations

import sys
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk

COLORES = {
    # Generales
    "fondo": "#EEEEEC",
    "superficie": "#FFFFFF",
    "superficie_alt": "#F6F6F4",
    "borde": "#D4D4D0",
    "borde_fuerte": "#B4B4AE",
    "texto": "#1C1C1C",
    "texto_suave": "#555555",
    "texto_tenue": "#8C8C88",
    "primario": "#2F5D82",
    "primario_hover": "#254B69",
    "primario_suave": "#E3EAF1",
    "primario_texto": "#1F4261",
    "secundario": "#4F7A99",
    # Barra lateral
    "lateral": "#DDDDD9",
    "lateral_hover": "#CFCFCA",
    "lateral_activo": "#FFFFFF",
    "lateral_texto": "#2A2A2A",
    "lateral_titulo": "#1C1C1C",
    "lateral_tenue": "#6B6B66",
    # Avisos
    "exito": "#2F6B3B", "exito_suave": "#E6F0E7", "exito_borde": "#B5CFB8",
    "advertencia": "#8A5A00", "advertencia_suave": "#FAF2DA", "advertencia_borde": "#DFCB8E",
    "error": "#A12A2A", "error_suave": "#F7E4E4", "error_borde": "#E0B1B1",
    "info": "#2F5D82", "info_suave": "#E3EAF1", "info_borde": "#B4C7D8",
    # Tablas
    "tabla_encabezado": "#3F4549",
    "tabla_encabezado_texto": "#FFFFFF",
    "tabla_sub": "#E2E2DE",
    "tabla_lateral": "#EEEEEA",
    "tabla_par": "#FFFFFF",
    "tabla_impar": "#F7F7F5",
    "tabla_rejilla": "#C8C8C2",
    "col_pivote": "#D8E5F0",
    "fila_pivote": "#F8EDC8",
    "celda_pivote": "#B26A00",
    "entra": "#2F5D82",
    "sale": "#A0471D",
    "razon_minima": "#F2E0A0",
    "zj": "#EEEEEA",
    "cjzj": "#DCE5EE",
    "optimo": "#D9EBDB",
    "optimo_texto": "#1F5A2B",
    "alternativo": "#E9DFEF",
    "alternativo_texto": "#6A3F82",
    "no_acotado": "#F3D8D8",
    # Transporte
    "tachado": "#E4E4E0",
    "tachado_texto": "#9A9A94",
    "asignada": "#D9EBDB",
    "elegida": "#2F6B3B",
    "linea_elegida": "#DCE5EE",
    "ficticio": "#F1ECF4",
    "costo_caja": "#EEEEEA",
    "prohibida": "#F3D8D8",
    "ciclo": "#6A3F82",
    "ciclo_mas": "#2F6B3B",
    "ciclo_menos": "#A12A2A",
}

FUENTES: dict[str, tkfont.Font] = {}
ESCALA = {"factor": 1.0}      # 1.0 = pantalla normal; 1.5 = Windows con escala al 150 %


def px(valor: float) -> int:
    """Convierte un tamaño en píxeles según la escala de la pantalla."""
    return int(round(valor * ESCALA["factor"]))


def _elegir_familia(disponibles, preferidas, respaldo):
    for familia in preferidas:
        if familia in disponibles:
            return familia
    return respaldo


def _familias():
    """Familias de letra según el sistema operativo."""
    if sys.platform.startswith("win"):
        return ["Segoe UI", "Calibri", "Arial"], ["Cascadia Mono", "Consolas", "Courier New"]
    if sys.platform == "darwin":
        return ["Helvetica Neue", "Helvetica", "Arial"], ["Menlo", "Monaco", "Courier"]
    return (["DejaVu Sans", "Inter", "Noto Sans", "Ubuntu", "Liberation Sans", "Arial"],
            ["DejaVu Sans Mono", "Noto Sans Mono", "Liberation Mono", "Ubuntu Mono"])


def crear_fuentes(raiz: tk.Misc) -> None:
    """Crea las fuentes con nombre usadas en toda la aplicación."""
    disponibles = set(tkfont.families(raiz))
    preferidas, monoespaciadas = _familias()
    base = _elegir_familia(disponibles, preferidas, "TkDefaultFont")
    mono = _elegir_familia(disponibles, monoespaciadas, "TkFixedFont")
    especificacion = {
        "base": (base, 10, "normal"),
        "base_negrita": (base, 10, "bold"),
        "pequena": (base, 9, "normal"),
        "pequena_negrita": (base, 9, "bold"),
        "mini": (base, 8, "normal"),
        "titulo": (base, 15, "bold"),
        "subtitulo": (base, 11, "normal"),
        "h2": (base, 11, "bold"),
        "h3": (base, 11, "bold"),
        "boton": (base, 10, "bold"),
        "lateral": (base, 11, "normal"),
        "lateral_negrita": (base, 11, "bold"),
        "logo": (base, 12, "bold"),
        "grande": (base, 15, "bold"),
        "mono": (mono, 10, "normal"),
        "mono_negrita": (mono, 10, "bold"),
        "tabla": (base, 10, "normal"),
        "tabla_negrita": (base, 10, "bold"),
        "tabla_pequena": (base, 8, "normal"),
        "asignacion": (base, 12, "bold"),
    }
    for nombre, (familia, tamano, peso) in especificacion.items():
        FUENTES[nombre] = tkfont.Font(raiz, family=familia, size=tamano, weight=peso)


def aplicar_tema(raiz: tk.Tk) -> None:
    """Configura los estilos ttk (botones, pestañas, listas, barras de desplazamiento...)."""
    crear_fuentes(raiz)
    try:
        ESCALA["factor"] = max(1.0, min(3.0, raiz.winfo_fpixels("1i") / 96.0))
    except tk.TclError:
        ESCALA["factor"] = 1.0
    c = COLORES
    estilo = ttk.Style(raiz)
    try:
        estilo.theme_use("clam")          # tema más personalizable en Windows, macOS y Linux
    except tk.TclError:
        pass
    raiz.configure(bg=c["fondo"])
    raiz.option_add("*TCombobox*Listbox.font", FUENTES["base"])
    raiz.option_add("*TCombobox*Listbox.selectBackground", c["primario"])
    raiz.option_add("*Font", FUENTES["base"])
    raiz.option_add("*Frame.highlightColor", c["borde"])      # los recuadros no cambian de color al recibir foco

    estilo.configure(".", font=FUENTES["base"], background=c["fondo"], foreground=c["texto"],
                     bordercolor=c["borde_fuerte"], focuscolor=c["primario"])
    estilo.configure("TFrame", background=c["fondo"])
    estilo.configure("Tarjeta.TFrame", background=c["superficie"])
    estilo.configure("TLabel", background=c["fondo"], foreground=c["texto"])
    estilo.configure("Tarjeta.TLabel", background=c["superficie"])

    # Botones
    estilo.configure("TButton", font=FUENTES["boton"], padding=(14, 7), background=c["superficie"],
                     foreground=c["texto"], bordercolor=c["borde_fuerte"], lightcolor=c["superficie"],
                     darkcolor=c["superficie"], relief="flat")
    estilo.map("TButton",
               background=[("disabled", c["fondo"]), ("pressed", c["borde"]), ("active", c["superficie_alt"])],
               foreground=[("disabled", c["texto_tenue"])],
               bordercolor=[("active", c["primario"])])
    estilo.configure("Primario.TButton", background=c["primario"], foreground="#FFFFFF",
                     bordercolor=c["primario"], lightcolor=c["primario"], darkcolor=c["primario"],
                     padding=(18, 8))
    estilo.map("Primario.TButton",
               background=[("disabled", c["borde_fuerte"]), ("pressed", c["primario_texto"]),
                           ("active", c["primario_hover"])],
               lightcolor=[("active", c["primario_hover"])], darkcolor=[("active", c["primario_hover"])],
               foreground=[("disabled", "#FFFFFF")])
    estilo.configure("Exito.TButton", background=c["elegida"], foreground="#FFFFFF",
                     bordercolor=c["elegida"], lightcolor=c["elegida"], darkcolor=c["elegida"],
                     padding=(18, 8))
    estilo.map("Exito.TButton", background=[("active", c["exito"]), ("pressed", c["exito"])],
               lightcolor=[("active", c["exito"])], darkcolor=[("active", c["exito"])])
    estilo.configure("Chico.TButton", font=FUENTES["pequena_negrita"], padding=(10, 4), width=0)

    # Pestañas
    estilo.configure("TNotebook", background=c["fondo"], borderwidth=0, tabmargins=(0, 6, 0, 0))
    estilo.configure("TNotebook.Tab", font=FUENTES["base_negrita"], padding=(10, 7),
                     background=c["borde"], foreground=c["texto_suave"], bordercolor=c["borde"],
                     lightcolor=c["borde"])
    estilo.map("TNotebook.Tab",
               background=[("selected", c["superficie"]), ("active", c["superficie_alt"])],
               foreground=[("selected", c["primario"]), ("active", c["texto"])],
               lightcolor=[("selected", c["superficie"])],
               expand=[("selected", (0, 2, 0, 0))])

    # Campos
    for nombre in ("TEntry", "TCombobox", "TSpinbox"):
        estilo.configure(nombre, fieldbackground=c["superficie"], background=c["superficie"],
                         foreground=c["texto"], bordercolor=c["borde_fuerte"], lightcolor=c["superficie"],
                         darkcolor=c["superficie"], arrowcolor=c["texto_suave"], padding=5,
                         insertcolor=c["texto"])
        estilo.map(nombre, bordercolor=[("focus", c["primario"])], lightcolor=[("focus", c["primario"])],
                   fieldbackground=[("readonly", c["superficie"]), ("disabled", c["fondo"])],
                   foreground=[("disabled", c["texto_tenue"])])
    estilo.configure("TRadiobutton", background=c["superficie"], foreground=c["texto"],
                     font=FUENTES["base"], indicatorcolor=c["superficie"])
    estilo.map("TRadiobutton", indicatorcolor=[("selected", c["primario"])],
               background=[("active", c["superficie"])])
    estilo.configure("TCheckbutton", background=c["superficie"], foreground=c["texto"])
    estilo.map("TCheckbutton", indicatorcolor=[("selected", c["primario"])],
               background=[("active", c["superficie"])])
    estilo.configure("Lateral.TRadiobutton", background=c["lateral"], foreground=c["lateral_texto"],
                     indicatorcolor=c["lateral_hover"], font=FUENTES["pequena"])
    estilo.map("Lateral.TRadiobutton", background=[("active", c["lateral"])],
               foreground=[("active", "#FFFFFF")],
               indicatorcolor=[("selected", "#818CF8")])

    # Barras de desplazamiento y paneles
    for orientacion in ("Vertical", "Horizontal"):
        estilo.configure(f"{orientacion}.TScrollbar", troughcolor=c["fondo"], background=c["borde_fuerte"],
                         bordercolor=c["fondo"], lightcolor=c["borde_fuerte"], darkcolor=c["borde_fuerte"],
                         arrowcolor=c["texto_suave"], gripcount=0)
        estilo.map(f"{orientacion}.TScrollbar", background=[("active", c["texto_tenue"])])
    estilo.configure("TPanedwindow", background=c["fondo"])
    estilo.configure("Sash", sashthickness=6, background=c["borde"])
    estilo.configure("TSeparator", background=c["borde"])

    # Listas (Treeview)
    estilo.configure("Treeview", font=FUENTES["base"], rowheight=28, background=c["superficie"],
                     fieldbackground=c["superficie"], bordercolor=c["borde"])
    estilo.configure("Treeview.Heading", font=FUENTES["base_negrita"], background=c["tabla_sub"],
                     foreground=c["texto"], relief="flat", padding=6)
    estilo.map("Treeview", background=[("selected", c["primario_suave"])],
               foreground=[("selected", c["primario_texto"])])
