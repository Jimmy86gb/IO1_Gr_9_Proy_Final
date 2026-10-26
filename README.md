# Proyecto Final · Investigación de Operaciones I · Grupo 9

Software de escritorio en **Python** que resuelve, paso a paso, problemas de **Programación Lineal con el Método Simplex (maximizar y minimizar)**.

| Dato                   | Detalle                                                               |
|------------------------|-----------------------------------------------------------------------|
| **Universidad**        | Universidad Distrital Francisco José de Caldas                        |
| **Asignatura**         | Investigación de Operaciones I · Grupo 020-82 (IO1-82)                |
| **Docente**            | Lilian Bejarano                                                       |
| **Periodo**            | 2026-3                                                                |
| **Grupo del proyecto** | Grupo 9 · Método de esta entrega: **Simplex** · Lenguaje: **Python**  |
| **Caso real**          | Cementos Argos S.A. – Línea de Concreto Premezclado (Regional Bogotá) |
| **Ciudad**             | Bogotá D.C., Colombia                                                 |
| **Segunda Entrega**    | 27 de Octubre de 2026                                                 |

### Integrantes

| Nombre | Código |
|---|---|
| Diego Alejandro Parra Díaz | 20212020091 |
| Alejandro Sánchez Escobar | 20222020252 |
| Juan Andrés Villada Saray | 20242020261 |
| Jimmy Alejandro Granados Becerra | 20251020034 |

---

## Contenido

1. [¿Qué hace el software?](#1-qué-hace-el-software)
2. [Requisitos](#2-requisitos)
3. [Instalar Python](#3-instalar-python)
4. [Descargar el proyecto](#4-descargar-el-proyecto)
5. [Ejecutar el programa](#5-ejecutar-el-programa)
6. [Ejecutar las pruebas automáticas](#6-ejecutar-las-pruebas-automáticas)
7. [Manual de uso del programa](#7-manual-de-uso-del-programa)
8. [Ejemplos precargados](#8-ejemplos-precargados)
9. [Estructura del proyecto](#9-estructura-del-proyecto)
10. [Declaración de uso de IA](#10-declaración-de-uso-de-ia)

---

## 1. ¿Qué hace el software?

Resuelve problemas de **Programación Lineal con el Método Simplex**, programado **desde cero**.

| Método | Problema que resuelve | Tamaño máximo | Qué muestra | Casos especiales que avisa |
|---|---|---|---|---|
| **Simplex (max / min)** | Programación lineal con restricciones **≤** y b ≥ 0 | **8 variables × 8 restricciones** | Forma estándar; **cada tabla** con variable que **entra**, variable que **sale** y elemento **pivote**; cálculo de Zj y Cj − Zj; operaciones de fila; solución final y z; **análisis de sensibilidad** | No acotado · Óptimos alternativos · Degeneración · Ciclaje |

> **Importante:** no se usan librerías ni programas que resuelvan el problema (**no se usa SciPy, PuLP, OR-Tools, NumPy ni el Solver de Excel**). Toda la matemática está escrita por el grupo en la carpeta `modelo/`. Esas herramientas solo se usan **aparte**, para comprobar los resultados en el informe.

**Características principales**

* Funciona con **cualquier problema** que escriba el usuario: los datos **nunca están dentro del código**.
* Cálculos con **fracciones exactas**: no hay errores de redondeo en empates, degeneración ni óptimos alternativos.
* Resultados con los **nombres y unidades** del problema (no solo x1, x2).
* **Validación**: casillas vacías, texto o datos imposibles se marcan en rojo con un mensaje claro y el programa **no se cierra**.
* **Ejemplos precargados** (caso real + problemas de prueba), y opción de **guardar y abrir** problemas en archivos `.json`.

---

## 2. Requisitos

| Requisito | Detalle |
|---|---|
| **Sistema operativo** | Windows 10/11, macOS o Linux |
| **Python** | **3.10 o superior** |
| **Tkinter** | Viene **incluido** con Python de [python.org](https://www.python.org/downloads/) en Windows y macOS |
| **Librerías externas** | **Ninguna.** No hay que instalar nada con `pip` (ver `requirements.txt`) |
| **Pantalla** | Recomendado 1280 × 720 o más |
| **Espacio** | Menos de 1 MB |

---

## 3. Instalar Python

Para saber si ya lo tiene, abra una terminal (en Windows: tecla **Windows**, escriba `cmd` y **Enter**) y escriba:

```bash
python --version
```

Si aparece `Python 3.10` o superior, pase a la [sección 4](#4-descargar-el-proyecto). Si no, instálelo así:

### Windows

1. Entre a **https://www.python.org/downloads/** y pulse **Download Python 3.x**.
2. Abra el instalador descargado.
3. **MUY
