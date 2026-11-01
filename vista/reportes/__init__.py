"""Reportes en texto que se ven en la pestaña «Reporte»."""
from .reporte_simplex import html_simplex, texto_simplex
from .reporte_vogel import texto_vogel

__all__ = ["texto_simplex", "html_simplex", "texto_vogel"]
