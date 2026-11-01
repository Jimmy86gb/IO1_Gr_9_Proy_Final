"""
vista/explicaciones/textos_transporte.py
========================================
Textos que explican cada paso de Vogel y de MODI, y los datos para
dibujar las tablas de transporte.
"""
from __future__ import annotations

from modelo.transporte import (COLUMNA, CRITERIO_MAYOR_ASIGNACION, CRITERIO_MENOR_COSTO, FILA,
                               MODO_CEROS, MODO_PENALIZACION, MODO_UNICA_COLUMNA, MODO_UNICA_FILA,
                               ResultadoMODI, ResultadoVogel)


def _b(texto, *etiquetas):
    return (texto, etiquetas)


def nombre_linea(r: ResultadoVogel, linea) -> str:
    tipo, k = linea
    return f"fila «{r.origenes[k]}»" if tipo == FILA else f"columna «{r.destinos[k]}»"


def nombre_celda(r: ResultadoVogel, celda) -> str:
    i, j = celda
    return f"({r.origenes[i]} → {r.destinos[j]})"


def _texto_criterio(criterio) -> str:
    return {CRITERIO_MENOR_COSTO: "se elige la de MENOR costo",
            CRITERIO_MAYOR_ASIGNACION: "se elige la que permite enviar MÁS unidades"}.get(
        criterio, "se elige la primera (filas antes que columnas)")


# ----------------------------------------------------------- planteamiento
def bloques_planteamiento(r: ResultadoVogel, fmt) -> list:
    p = r.problema
    u = p.unidad_producto
    bloques = [_b(f"{p.nombre}\n", "titulo")]
    if p.descripcion:
        bloques.append(_b(p.descripcion + "\n\n", "suave"))
    bloques.append(_b("El problema\n", "subtitulo"))
    bloques.append(_b(f"  x_ij = {u} que se envían del origen i al destino j;  c_ij = costo por unidad "
                      f"({p.unidad_costo} por {u}).\n", "vineta"))
    bloques.append(_b("  Costo total mínimo:  Z = suma de c_ij · x_ij\n", "formula"))
    bloques.append(_b("  Cada origen envía como máximo su oferta; cada destino recibe al menos su demanda; x_ij ≥ 0\n",
                      "formula"))
    bloques.append(_b("\nPaso 0. ¿Está balanceado?\n", "subtitulo"))
    oferta = " + ".join(fmt.num(x) for x in p.oferta)
    demanda = " + ".join(fmt.num(x) for x in p.demanda)
    bloques.append(_b(f"  Oferta total = {oferta} = {fmt.num(p.total_oferta)} {u}\n", "formula"))
    bloques.append(_b(f"  Demanda total = {demanda} = {fmt.num(p.total_demanda)} {u}\n", "formula"))
    if r.ficticio is None:
        bloques.append(_b("  Oferta = Demanda → el problema está BALANCEADO.\n", "exito"))
    elif r.ficticio == "destino":
        bloques.append(_b(f"  Oferta > Demanda → DESBALANCEADO. Se agrega «{r.destinos[-1]}» con demanda "
                          f"{fmt.num(r.cantidad_ficticia)} {u} y costo 0 (lo que se le asigne queda sin "
                          f"enviar).\n", "advertencia"))
    else:
        bloques.append(_b(f"  Demanda > Oferta → DESBALANCEADO. Se agrega «{r.origenes[-1]}» con oferta "
                          f"{fmt.num(r.cantidad_ficticia)} {u} y costo 0 (lo que «envíe» es demanda "
                          f"insatisfecha).\n", "advertencia"))
    prohibidas = p.rutas_prohibidas()
    if prohibidas:
        lista = ", ".join(f"{p.origenes[i]} → {p.destinos[j]}" for i, j in prohibidas)
        bloques.append(_b(f"  Rutas prohibidas (costo M, un número enorme para que no se usen): {lista}.\n", "vineta"))
    bloques.append(_b(f"\n  Tamaño: {r.m} × {r.n}. Una solución completa tiene {r.m} + {r.n} − 1 = "
                      f"{r.m + r.n - 1} envíos.\n", "vineta"))
    bloques.append(_b("\nCómo funciona Vogel\n", "subtitulo"))
    for regla in ("Cada fila y columna tiene una penalización = segundo costo más bajo − costo más bajo.",
                  "Se elige la fila o columna con la MAYOR penalización (si hay empate: menor costo, luego "
                  "más unidades, luego la primera).",
                  "En esa fila o columna se envía lo máximo posible por la celda de MENOR costo: x = mín(oferta, demanda).",
                  "Se tacha la fila o columna que ya quedó completa (si se completan las dos a la vez, se tacha "
                  "solo una: es degeneración).",
                  "Se repite hasta llenar la tabla."):
        bloques.append(_b(f"  • {regla}\n", "vineta"))
    return bloques


# ----------------------------------------------------------------- pasos
def datos_tabla_paso(r: ResultadoVogel, indice: int, fmt) -> dict:
    """Datos para dibujar la tabla de un paso de Vogel."""
    paso = r.pasos[indice]
    tachadas_antes_f = {i for i in range(r.m) if i not in paso.filas_activas}
    tachadas_antes_c = {j for j in range(r.n) if j not in paso.columnas_activas}
    oferta, demanda = [], []
    for i in range(r.m):
        antes, despues = paso.oferta_antes[i], paso.oferta_despues[i]
        oferta.append(f"{fmt.num(antes)} → {fmt.num(despues)}" if antes != despues else fmt.num(despues))
    for j in range(r.n):
        antes, despues = paso.demanda_antes[j], paso.demanda_despues[j]
        demanda.append(f"{fmt.num(antes)} → {fmt.num(despues)}" if antes != despues else fmt.num(despues))
    penal_f = {i: fmt.num(info.penalizacion) for i, info in paso.penalizaciones_filas.items()}
    penal_c = {j: fmt.num(info.penalizacion) for j, info in paso.penalizaciones_columnas.items()}
    hay_penal = paso.modo == MODO_PENALIZACION
    return dict(
        origenes=r.origenes, destinos=r.destinos,
        costos=[[fmt.num(c) for c in fila] for fila in r.costos],
        asignaciones={c: fmt.num(x) for c, x in paso.asignaciones.items()},
        oferta=oferta, demanda=demanda,
        penal_filas=penal_f if hay_penal else {}, penal_columnas=penal_c if hay_penal else {},
        penal_resaltada=paso.linea if hay_penal else None,
        filas_tachadas=tachadas_antes_f, columnas_tachadas=tachadas_antes_c,
        tachada_ahora=paso.tachada, linea_resaltada=paso.linea, celda_elegida=paso.celda,
        fila_ficticia=r.m - 1 if r.ficticio == "origen" else None,
        columna_ficticia=r.n - 1 if r.ficticio == "destino" else None,
        prohibidas={(i, j) for i in range(r.m) for j in range(r.n) if r.costos[i][j].tiene_m},
        total=f"{fmt.num(sum(paso.oferta_despues))}",
    )


def datos_tabla_final(r: ResultadoVogel, fmt, asignaciones=None) -> dict:
    asignaciones = r.asignaciones if asignaciones is None else asignaciones
    return dict(
        origenes=r.origenes, destinos=r.destinos,
        costos=[[fmt.num(c) for c in fila] for fila in r.costos],
        asignaciones={c: fmt.num(x) for c, x in asignaciones.items()},
        oferta=[fmt.num(x) for x in r.oferta], demanda=[fmt.num(x) for x in r.demanda],
        fila_ficticia=r.m - 1 if r.ficticio == "origen" else None,
        columna_ficticia=r.n - 1 if r.ficticio == "destino" else None,
        prohibidas={(i, j) for i in range(r.m) for j in range(r.n) if r.costos[i][j].tiene_m},
        total=f"{fmt.num(sum(r.oferta))}",
    )


def titulo_paso(r: ResultadoVogel, indice: int) -> str:
    paso = r.pasos[indice]
    modo = {MODO_PENALIZACION: "penalizaciones", MODO_UNICA_FILA: "queda una sola fila",
            MODO_UNICA_COLUMNA: "queda una sola columna", MODO_CEROS: "envíos en cero"}[paso.modo]
    return f"Paso {paso.numero} de {len(r.pasos)} — {modo}"


def bloques_paso(r: ResultadoVogel, indice: int, fmt) -> list:
    p = r.problema
    u = p.unidad_producto
    paso = r.pasos[indice]
    i, j = paso.celda
    bloques = [_b(titulo_paso(r, indice) + "\n", "titulo")]

    if paso.modo == MODO_PENALIZACION:
        bloques.append(_b("1) Penalizaciones (segundo costo más bajo − costo más bajo)\n",
                          "subtitulo"))
        for tipo, diccionario, nombres in ((FILA, paso.penalizaciones_filas, r.origenes),
                                           (COLUMNA, paso.penalizaciones_columnas, r.destinos)):
            for k, info in diccionario.items():
                costos = ", ".join(fmt.num(c) for c in info.costos_activos)
                texto = (f"  {'Fila' if tipo == FILA else 'Columna'} {nombres[k]}: costos {costos} → "
                         f"{fmt.num(info.segundo)} − {fmt.par(info.menor)} = {fmt.num(info.penalizacion)}")
                elegida = paso.linea == (tipo, k)
                bloques.append(_b(texto + ("   ← mayor" if elegida else "") + "\n", "formula",
                                  *(("resaltado",) if elegida else ())))
        bloques.append(_b("2) Fila o columna con la MAYOR penalización\n", "subtitulo"))
        info = (paso.penalizaciones_filas[paso.linea[1]] if paso.linea[0] == FILA
                else paso.penalizaciones_columnas[paso.linea[1]])
        if paso.empate_lineas:
            empatadas = ", ".join(nombre_linea(r, l) for l in paso.empate_lineas)
            bloques.append(_b(f"  Empate de penalización ({fmt.num(info.penalizacion)}) entre {empatadas}. "
                              f"Para desempatar: {_texto_criterio(paso.criterio_desempate)}.\n",
                              "advertencia"))
        bloques.append(_b(f"  Se escoge la {nombre_linea(r, paso.linea)} con penalización "
                          f"{fmt.num(info.penalizacion)}.\n", "vineta", "negrita"))
        numero = 3
    elif paso.modo in (MODO_UNICA_FILA, MODO_UNICA_COLUMNA):
        bloques.append(_b(f"1) Solo queda la {nombre_linea(r, paso.linea)}: ya no hacen falta penalizaciones; "
                          f"se llenan sus celdas empezando por la más barata.\n", "vineta"))
        numero = 2
    else:
        bloques.append(_b("1) Ya no queda nada por enviar. Para completar los envíos necesarios se pone 0 en la "
                          "celda libre más barata.\n", "vineta"))
        numero = 2

    bloques.append(_b(f"{numero}) Celda más barata y cantidad a enviar\n", "subtitulo"))
    if paso.empate_celdas:
        celdas = ", ".join(nombre_celda(r, c) for c in paso.empate_celdas)
        bloques.append(_b(f"  Empate de costo entre {celdas}: {_texto_criterio(paso.criterio_celda)}.\n",
                          "advertencia"))
    bloques.append(_b(f"  Celda escogida: {nombre_celda(r, paso.celda)} con costo {fmt.num(paso.costo)} "
                      f"{p.unidad_costo}/{u}.\n", "vineta"))
    bloques.append(_b(f"  x = mín(oferta {fmt.num(paso.oferta_antes[i])}, demanda {fmt.num(paso.demanda_antes[j])}) "
                      f"= {fmt.num(paso.cantidad)} {u}\n", "formula", "negrita"))
    bloques.append(_b(f"{numero + 1}) Se actualiza lo que queda\n", "subtitulo"))
    bloques.append(_b(f"  Oferta restante de {r.origenes[i]}: {fmt.num(paso.oferta_antes[i])} − {fmt.num(paso.cantidad)} = "
                      f"{fmt.num(paso.oferta_despues[i])}\n", "formula"))
    bloques.append(_b(f"  Demanda restante de {r.destinos[j]}: {fmt.num(paso.demanda_antes[j])} − {fmt.num(paso.cantidad)} = "
                      f"{fmt.num(paso.demanda_despues[j])}\n", "formula"))
    bloques.append(_b(f"  Se tacha la {nombre_linea(r, paso.tachada)}.\n", "vineta", "negrita"))
    if paso.simultaneo and len(paso.filas_activas) + len(paso.columnas_activas) > 2:
        otra = (COLUMNA, j) if paso.tachada[0] == FILA else (FILA, i)
        bloques.append(_b(f"  Degeneración: la fila y la columna se completan al mismo tiempo. Se tacha solo "
                          f"una; la {nombre_linea(r, otra)} queda con 0 y más adelante recibirá un envío de 0.\n", "advertencia"))
    return bloques


def bloques_resultado(r: ResultadoVogel, fmt) -> list:
    p = r.problema
    u = p.unidad_producto
    bloques = [_b("Resultado de Vogel\n", "titulo"), _b("Envíos\n",
                                                                     "subtitulo")]
    for i, j, x, costo in r.envios():
        nota = ""
        if r.es_fila_ficticia(i):
            nota = "  (demanda sin atender)"
        elif r.es_columna_ficticia(j):
            nota = "  (queda sin enviar)"
        bloques.append(_b(f"  • {r.origenes[i]} → {r.destinos[j]}: {fmt.num(x)} {u} × "
                          f"{fmt.num(r.costos[i][j])} = {fmt.num(costo)} {p.unidad_costo}{nota}\n", "vineta"))
    if r.celdas_cero:
        celdas = ", ".join(nombre_celda(r, c) for c in r.celdas_cero)
        bloques.append(_b(f"  Envíos de 0 (degeneración): {celdas}\n", "advertencia"))
    terminos = " + ".join(f"{fmt.par(r.costos[i][j])}·{fmt.num(x)}" for (i, j), x in sorted(r.asignaciones.items())
                          if x > 0)
    bloques.append(_b("\nCosto total\n", "subtitulo"))
    bloques.append(_b(f"  Z = {terminos}\n", "formula"))
    bloques.append(_b(f"  Z = {fmt.num(r.costo_total)} {p.unidad_costo}\n", "exito"))
    positivas = sum(1 for x in r.asignaciones.values() if x > 0)
    bloques.append(_b(f"\n  Envíos necesarios: {r.m + r.n - 1}; registrados: {len(r.asignaciones)}; "
                      f"con cantidad mayor que 0: {positivas}.\n", "vineta"))
    return bloques


# ---------------------------------------------------------------------- MODI
def orden_potenciales(basicas, fila_referencia):
    """Orden en que se calculan u_i y v_j (el mismo que usa el modelo)."""
    conocidos_u, conocidos_v = {fila_referencia}, set()
    pendientes = sorted(basicas)
    orden = []
    while pendientes:
        avance = False
        for celda in list(pendientes):
            i, j = celda
            if i in conocidos_u and j not in conocidos_v:
                orden.append((celda, "v"))
                conocidos_v.add(j)
            elif j in conocidos_v and i not in conocidos_u:
                orden.append((celda, "u"))
                conocidos_u.add(i)
            elif i in conocidos_u and j in conocidos_v:
                orden.append((celda, "="))
            else:
                continue
            pendientes.remove(celda)
            avance = True
        if not avance:
            break
    return orden


def datos_tabla_modi(r: ResultadoVogel, modi: ResultadoMODI, indice: int, fmt) -> dict:
    it = modi.iteraciones[indice]
    datos = datos_tabla_final(r, fmt, it.asignaciones)
    datos.update(
        u=[fmt.num(x) for x in it.u], v=[fmt.num(x) for x in it.v],
        reducidos={c: f"d = {fmt.num(d)}" for c, d in it.costos_reducidos.items()},
        reducidos_negativos={c for c, d in it.costos_reducidos.items() if d < 0},
        reducidos_cero={c for c, d in it.costos_reducidos.items() if d == 0},
        ciclo=it.ciclo, celda_elegida=None,
    )
    return datos


def bloques_modi(r: ResultadoVogel, modi: ResultadoMODI, indice: int, fmt) -> list:
    p = r.problema
    it = modi.iteraciones[indice]
    u_ref = it.fila_referencia
    titulo = "solución de Vogel" if it.numero == 0 else f"después de la mejora {it.numero}"
    bloques = [_b(f"Revisión {it.numero} de MODI — {titulo}\n", "titulo"),
               _b(f"  Costo actual = {fmt.num(it.costo)} {p.unidad_costo}\n", "negrita")]
    bloques.append(_b(f"1) Valores u y v: en las celdas con envío, u_i + v_j = costo (se toma u de {r.origenes[u_ref]} = 0)\n", "subtitulo"))
    for (i, j), tipo in orden_potenciales(list(it.asignaciones.keys()), u_ref):
        c = r.costos[i][j]
        if tipo == "v":
            texto = f"  {nombre_celda(r, (i, j))}: v{j + 1} = c − u{i + 1} = {fmt.num(c)} − {fmt.par(it.u[i])} = {fmt.num(it.v[j])}"
        elif tipo == "u":
            texto = f"  {nombre_celda(r, (i, j))}: u{i + 1} = c − v{j + 1} = {fmt.num(c)} − {fmt.par(it.v[j])} = {fmt.num(it.u[i])}"
        else:
            texto = f"  {nombre_celda(r, (i, j))}: u{i + 1} + v{j + 1} = {fmt.num(c)} (comprobación)"
        bloques.append(_b(texto + "\n", "formula"))
    bloques.append(_b("2) Para las celdas sin envío: d_ij = costo − u_i − v_j\n", "subtitulo"))
    for (i, j), d in sorted(it.costos_reducidos.items()):
        marca = "   ← entra" if it.entra == (i, j) else ""
        bloques.append(_b(f"  {nombre_celda(r, (i, j))}: {fmt.num(r.costos[i][j])} − {fmt.par(it.u[i])} − "
                          f"{fmt.par(it.v[j])} = {fmt.num(d)}{marca}\n", "formula",
                          *(("resaltado",) if marca else ())))
    if not it.costos_reducidos:
        bloques.append(_b("  (no hay celdas no básicas)\n", "formula"))
    bloques.append(_b("3) ¿Se puede mejorar? (no, si todos los d_ij son ≥ 0)\n", "subtitulo"))
    if it.es_optima:
        bloques.append(_b("  Todos los d_ij ≥ 0 → esta es la MEJOR solución.\n", "exito"))
        ceros = [c for c, d in it.costos_reducidos.items() if d == 0]
        if ceros:
            bloques.append(_b(f"  Hay d_ij = 0 en {', '.join(nombre_celda(r, c) for c in ceros)}: existe otra "
                              f"distribución con el mismo costo.\n", "alternativo"))
        return bloques
    if it.entra is None:
        bloques.append(_b("  Se llegó al límite de revisiones.\n", "error"))
        return bloques
    bloques.append(_b(f"  Hay d_ij negativos: se usará la celda {nombre_celda(r, it.entra)} con d = "
                      f"{fmt.num(it.costos_reducidos[it.entra])} (cada unidad enviada por ahí baja el costo en "
                      f"{fmt.num(abs(it.costos_reducidos[it.entra]))}).\n", "vineta"))
    bloques.append(_b("4) Camino cerrado (+ − + − ...)\n", "subtitulo"))
    ciclo = "  →  ".join(f"{nombre_celda(r, c)}({'+' if k % 2 == 0 else '−'})" for k, c in enumerate(it.ciclo))
    bloques.append(_b(f"  {ciclo}\n", "formula"))
    menos = ", ".join(f"{fmt.num(it.asignaciones[c])}" for c in it.ciclo[1::2])
    bloques.append(_b(f"5) Cantidad a mover θ = la menor de las celdas (−) = mín({menos}) = {fmt.num(it.theta)}\n", "subtitulo"))
    bloques.append(_b(f"  Se suma θ en las celdas (+) y se resta en las (−). Deja de usarse {nombre_celda(r, it.sale)}.\n",
                      "vineta"))
    if it.theta == 0:
        bloques.append(_b("  θ = 0: cambia la distribución pero no el costo.\n", "advertencia"))
    nuevo = it.costo + it.costos_reducidos[it.entra] * it.theta
    bloques.append(_b(f"  Nuevo costo = {fmt.num(it.costo)} + ({fmt.num(it.costos_reducidos[it.entra])})·"
                      f"{fmt.num(it.theta)} = {fmt.num(nuevo)} {p.unidad_costo}\n", "formula", "negrita"))
    return bloques
