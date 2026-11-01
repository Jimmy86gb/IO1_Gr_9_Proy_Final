"""
controlador/controlador_principal.py
====================================
Crea la ventana, las pantallas y los controladores (Simplex y Vogel),
y maneja la navegación y los atajos de teclado.
"""
from __future__ import annotations

from modelo.repositorio import RepositorioProblemas
from vista.simplex.vista_simplex import VistaSimplex
from vista.ventana_principal import VentanaPrincipal
from vista.vista_ayuda import VistaAyuda
from vista.vista_inicio import VistaInicio
from vista.vogel.vista_vogel import VistaVogel

from .controlador_simplex import ControladorSimplex
from .controlador_vogel import ControladorVogel

MENSAJES = {
    "inicio": "Inicio.",
    "simplex": "Método Simplex (maximizar / minimizar), hasta 8 variables y 8 restricciones.",
    "vogel": "Método de Vogel (transporte), hasta 8 orígenes y 8 destinos.",
    "ayuda": "Manual de uso.",
}


class ControladorPrincipal:
    def __init__(self):
        self.repositorio = RepositorioProblemas()
        self.ventana = VentanaPrincipal(al_navegar=self.mostrar_vista)
        contenedor = self.ventana.contenedor_central

        self.vista_simplex = VistaSimplex(contenedor)
        self.ctrl_simplex = ControladorSimplex(self.vista_simplex, self.repositorio,
                                               cb_estado=self.ventana.actualizar_estado)
        self.vista_vogel = VistaVogel(contenedor)
        self.ctrl_vogel = ControladorVogel(self.vista_vogel, self.repositorio,
                                           cb_estado=self.ventana.actualizar_estado)
        self.vista_inicio = VistaInicio(
            contenedor,
            ir_a_simplex=lambda: self.mostrar_vista("simplex"),
            cargar_caso_real_simplex=self._abrir_caso_real,
            ir_a_vogel=lambda: self.mostrar_vista("vogel"),
            cargar_caso_real_vogel=self._abrir_caso_real_vogel,
            ir_a_ayuda=lambda: self.mostrar_vista("ayuda"),
        )
        self.vista_ayuda = VistaAyuda(contenedor)
        self._vistas = {"inicio": self.vista_inicio, "simplex": self.vista_simplex, "vogel": self.vista_vogel,
                        "ayuda": self.vista_ayuda}
        self._actual = None

        self.ctrl_simplex.cargar_caso_real_por_defecto()
        self.ctrl_vogel.cargar_primer_ejemplo()
        self.ventana.bind("<Control-Return>", self._atajo_resolver)
        self.ventana.bind("<F5>", self._atajo_resolver)
        self.ventana.bind("<F1>", lambda e: self.mostrar_vista("ayuda"))
        self.mostrar_vista("inicio")

    def mostrar_vista(self, clave: str) -> None:
        if clave not in self._vistas:
            return
        for vista in self._vistas.values():
            vista.pack_forget()
        self._vistas[clave].pack(fill="both", expand=True)
        self._actual = clave
        self.ventana.resaltar_boton_nav(clave)
        self.ventana.actualizar_estado(MENSAJES[clave])

    def _abrir_caso_real(self) -> None:
        self.mostrar_vista("simplex")
        self.ctrl_simplex.cargar_caso_real_por_defecto()
        self.ctrl_simplex.resolver()

    def _abrir_caso_real_vogel(self) -> None:
        self.mostrar_vista("vogel")
        self.ctrl_vogel.cargar_primer_ejemplo()
        self.ctrl_vogel.resolver()

    def _atajo_resolver(self, _evento=None) -> None:
        if self._actual == "simplex":
            self.ctrl_simplex.resolver()
        elif self._actual == "vogel":
            self.ctrl_vogel.resolver()

    def iniciar(self) -> None:
        self.ventana.mainloop()
