"""
vista/reportes/reporte_vogel.py
===============================
Informe en texto del método de Vogel: el problema, cada paso, la tabla
final, el costo total y la comparación con la mejor solución (MODI).
"""
from __future__ import annotations

from ..explicaciones import textos_transporte as TT
from .utilidades import bloques_a_texto, encabezado_texto, seccion_texto, tabla_texto


def _tabla_transporte_texto(d: dict) -> str:
    """Dibuja la tabla en texto. Cada celda dice «cantidad (costo)»."""
    encabezado = ["Origen \\ Destino"] + list(d["destinos"]) + ["Oferta"]
    tiene_penal = d.get("penal_filas") is not None and d.get("penal_filas") != {}
    if tiene_penal:
        encabezado.append("Penalización")
    if d.get("u") is not None:
        encabezado.append("u_i")
    filas = [encabezado]
    for i, origen in enumerate(d["origenes"]):
        fila = [origen]
        for j in range(len(d["destinos"])):
            centro = (d.get("asignaciones") or {}).get((i, j), (d.get("reducidos") or {}).get((i, j), ""))
            marca = "*" if d.get("celda_elegida") == (i, j) else ""
            fila.append(f"{marca}{centro} ({d['costos'][i][j]})" if centro != "" else f"({d['costos'][i][j]})")
        fila.append(d["oferta"][i] if d.get("oferta") else "")
        if tiene_penal:
            fila.append(d["penal_filas"].get(i, ""))
        if d.get("u") is not None:
            fila.append(d["u"][i])
        filas.append(fila)
    fila = ["Demanda"] + list(d.get("demanda") or [""] * len(d["destinos"])) + [d.get("total") or ""]
    filas.append(fila)
    if tiene_penal:
        filas.append(["Penalización"] + [d["penal_columnas"].get(j, "") for j in range(len(d["destinos"]))] + [""])
    if d.get("v") is not None:
        filas.append(["v_j"] + list(d["v"]) + [""])
    return tabla_texto(filas)


def texto_vogel(resultado, modi, fmt) -> str:
    p = resultado.problema
    partes = [encabezado_texto(f"INFORME · MÉTODO DE VOGEL · {p.nombre}")]
    partes.append(seccion_texto("1. El problema y su balance"))
    partes.append(bloques_a_texto(TT.bloques_planteamiento(resultado, fmt)))
    partes.append("\nCostos (" + p.unidad_costo + " por " + p.unidad_producto + ")\n")
    partes.append(_tabla_transporte_texto({**TT.datos_tabla_final(resultado, fmt), "asignaciones": {}}))
    partes.append(seccion_texto("2. Paso a paso"))
    for k in range(len(resultado.pasos)):
        partes.append("\n" + _tabla_transporte_texto(TT.datos_tabla_paso(resultado, k, fmt)))
        partes.append("   * = celda escogida en este paso; formato: asignación (costo unitario)\n")
        partes.append(bloques_a_texto(TT.bloques_paso(resultado, k, fmt)))
    partes.append(seccion_texto("3. Tabla final y costo total"))
    partes.append(_tabla_transporte_texto(TT.datos_tabla_final(resultado, fmt)))
    partes.append(bloques_a_texto(TT.bloques_resultado(resultado, fmt)))
    for caso in resultado.casos:
        partes.append(f"\n[{caso.nivel.upper()}] {caso.titulo}\n    {caso.mensaje}\n")
    if modi is not None:
        partes.append(seccion_texto("4. Comparación con la mejor solución (MODI)"))
        for k in range(len(modi.iteraciones)):
            partes.append("\n" + _tabla_transporte_texto(TT.datos_tabla_modi(resultado, modi, k, fmt)))
            partes.append(bloques_a_texto(TT.bloques_modi(resultado, modi, k, fmt)))
        partes.append(f"\nCosto con Vogel = {fmt.num(modi.costo_inicial)} {p.unidad_costo}\n"
                      f"Mejor costo (MODI) = {fmt.num(modi.costo_optimo)} {p.unidad_costo}\n"
                      f"Diferencia = {fmt.num(modi.ahorro)} {p.unidad_costo}\n")
        for caso in modi.casos:
            partes.append(f"\n[{caso.nivel.upper()}] {caso.titulo}\n    {caso.mensaje}\n")
    return "".join(partes)
