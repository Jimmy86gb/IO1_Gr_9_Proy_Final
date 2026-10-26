"""
controlador/controlador_principal.py
====================================
Coordinador de la aplicación: crea la ventana, las pantallas y el controlador
del Simplex, y se encarga de la navegación y de los atajos de teclado.
"""
from __future__ import annotations

from modelo.repositorio import RepositorioProblemas
from vista.simplex.vista_simplex import VistaSimplex
from vista.ventana_principal import VentanaPrincipal
from vista.vista_ayuda import VistaAyuda
from vista.vista_inicio import VistaInicio

from .controlador_simplex import ControladorSimplex

MENSAJES = {
    "inicio": "Inicio.",
    "simplex": "Método Simplex (maximizar / minimizar), hasta 8 variables y 8 restricciones.",
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
        self.vista_inicio = VistaInicio(
            contenedor,
            ir_a_simplex=lambda: self.mostrar_vista("simplex"),
            cargar_caso_real_simplex=self._abrir_caso_real,
            ir_a_ayuda=lambda: self.mostrar_vista("ayuda"),
        )
        self.vista_ayuda = VistaAyuda(contenedor)
        self._vistas = {"inicio": self.vista_inicio, "simplex": self.vista_simplex, "ayuda": self.vista_ayuda}
        self._actual = None

        self.ctrl_simplex.cargar_caso_real_por_defecto()
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

    def _atajo_resolver(self, _evento=None) -> None:
        if self._actual == "simplex":
            self.ctrl_simplex.resolver()

    def iniciar(self) -> None:
        self.ventana.mainloop()
