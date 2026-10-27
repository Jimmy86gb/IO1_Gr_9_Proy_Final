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
3. **MUY IMPORTANTE:** marque **☑ Add python.exe to PATH**.
4. Pulse **Install Now** (deje marcada la opción *tcl/tk and IDLE*, es la que dibuja la ventana).
5. Al terminar, cierre y vuelva a abrir la terminal y compruebe con `python --version`.

### macOS

1. Descargue el instalador **macOS 64-bit universal2** desde **https://www.python.org/downloads/** y siga los pasos.
2. Compruebe con `python3 --version`.

> Si instaló Python con **Homebrew**, Tkinter puede no venir incluido: `brew install python-tk`

### Linux (Ubuntu / Debian)

```bash
sudo apt update
sudo apt install python3 python3-tk
```

En Fedora: `sudo dnf install python3 python3-tkinter`

---

## 4. Descargar el proyecto

1. Descargue `IO1_Grupo9.zip` (plataforma del curso o repositorio).
2. **Clic derecho → Extraer todo…** (Windows) o doble clic (macOS).
3. Abra la carpeta extraída y **verifique que adentro esté `main.py`** junto a las carpetas `modelo`, `vista`, `controlador`, `ejemplos` y `tests`.

> **Atención:** a veces queda una carpeta dentro de otra con el mismo nombre (`IO1_Grupo9/IO1_Grupo9/`). La correcta es **la que contiene `main.py`**.

```
IO1_Grupo9/
├── main.py          ← archivo que se ejecuta
├── README.md
├── requirements.txt
├── controlador/
├── ejemplos/
├── modelo/
├── tests/
└── vista/
```

---

## 5. Ejecutar el programa

En todos los casos se ejecuta **`main.py`**. Se abre una ventana con una barra lateral que dice **"IO1 · Grupo 9"** y el menú **Inicio · Método Simplex · Ayuda**.

| Entorno | Cómo ejecutar |
|---|---|
| **PyCharm** | Abrir la carpeta que contiene `main.py` (**File → Open…**), configurar el intérprete (Python 3.10+) y clic derecho en `main.py` → **Run 'main'** |
| **VS Code** | Instalar la extensión *Python*, **File → Open Folder…**, abrir `main.py` y pulsar **▶ Run Python File** (o **Ctrl + F5**) |
| **CMD / PowerShell** | En la carpeta del proyecto: `python main.py` (o `py main.py`) |
| **Terminal macOS / Linux** | `cd ruta/a/IO1_Grupo9` y luego `python3 main.py` |
| **IDLE** | Abrir `main.py` → **F5** |

> Consejo: en Windows, abra la carpeta en el Explorador, escriba `cmd` en la barra de dirección y presione **Enter**; se abre una consola ya ubicada ahí.

**(Opcional) entorno virtual:** `python -m venv .venv` → activar (`.venv\Scripts\activate` en Windows, `source .venv/bin/activate` en macOS/Linux) → `python main.py`. No es obligatorio porque no hay dependencias.

---

## 6. Ejecutar las pruebas automáticas

Se usa `unittest`, que viene con Python. **Las pruebas no abren la ventana**: solo muestran texto.

| Entorno | Cómo |
|---|---|
| **PyCharm** | Clic derecho en la carpeta **`tests`** → **Run 'Python tests in tests'** |
| **VS Code** | Ícono **Testing** → **Configure Python Tests** → **unittest** → carpeta **tests** → patrón `test_*.py` |
| **Consola** (en la carpeta del proyecto) | `python -m unittest discover -s tests -v` |

Resultado esperado: **25 pruebas, OK**.

| Archivo | N.º | Qué comprueba |
|---|---|---|
| `test_numeros.py` | 4 | Lectura de números (`12`, `2,5`, `3/4`, `1e3`) y rechazo de textos inválidos (`abc`, `1.250.000`, `3/0`) |
| `test_simplex.py` | 9 | Maximización clásica (z = 36), minimización (z = −11), no acotado, óptimos alternativos, degeneración, que la solución cumpla las restricciones, tamaño máximo **8 × 8** y que **todos los ejemplos precargados** den el resultado esperado (caso real: **Z = 86.000**) |
| `test_sensibilidad.py` | 6 | Precios sombra, dualidad (Σ bᵢ·yᵢ = z), rangos de cⱼ y de bᵢ, sensibilidad en minimización y que exija una solución óptima |
| `test_validacion.py` | 6 | Campos vacíos, texto en vez de números, b negativo, más de 8 variables, nombres repetidos y signo ≥ no permitido |

---

## 7. Manual de uso del programa

### 7.1 Pantalla principal

| Zona | Función |
|---|---|
| **Barra lateral** | Navegar entre **Inicio**, **Método Simplex** y **Ayuda** |
| **Números** | Ver los resultados en **fracciones** (5/3) o **decimales** (1.6667). Se actualiza todo al instante |
| **Barra de estado** | Mensaje de lo último que hizo el programa (abajo) |
| **Pestañas 1 a 7** | Datos, modelo, paso a paso, tablas, solución, sensibilidad y reporte |

### 7.2 Cómo ingresar un problema

1. En la barra lateral pulse **Método Simplex** y quédese en la pestaña **1 · Datos**.
2. Para empezar de cero pulse **Limpiar**; para usar un ejemplo, elíjalo en **Ejemplos** y pulse **Cargar ejemplo**.
3. Complete **1. Datos generales**:

| Campo | Qué escribir |
|---|---|
| Nombre del problema | Título del problema |
| Objetivo | **Maximizar** o **Minimizar** |
| ¿Qué mide z? | Qué representa la función objetivo |
| Unidad de z | Unidad de la función objetivo |
| Número de variables | De **1 a 8** |
| Número de restricciones | De **1 a 8** |

4. Complete **2. Modelo**:

| Fila / columna | Significado | Unidad |
|---|---|---|
| **Nombre de la variable** | Qué decide cada xⱼ | — |
| **Unidad** | Cómo se mide la variable | ej. lotes de 10 m³/semana |
| **cⱼ** | Aporte a z por **una** unidad de la variable | unidad de z por unidad de variable |
| **Nombre de la restricción** | Recurso que limita | — |
| **aᵢⱼ** | Cuánto del recurso i usa **una** unidad de la variable j (escriba **0** si no lo usa) | unidad del recurso por unidad de variable |
| **bᵢ (disponible)** | Cantidad disponible del recurso (debe ser **≥ 0**) | unidad del recurso |

5. Revise la **3. Vista previa del modelo matemático** (se actualiza mientras escribe).
6. Pulse **Resolver con Simplex ►** (o **Ctrl + Enter** / **F5**).

### 7.3 Pestañas de resultados

| Pestaña | Contenido |
|---|---|
| **2 · Modelo** | Modelo matemático, forma estándar con holguras y reglas del método |
| **3 · Paso a paso** | Cada tabla con **columna pivote**, **fila pivote** y **elemento pivote** resaltados; explicación de Zj, Cj − Zj, variable que entra, razones, variable que sale y operaciones de fila. Botones **◄ Anterior / Siguiente ►** |
| **4 · Tablas** | Todas las tablas una debajo de otra |
| **5 · Solución** | Plan óptimo con nombres y unidades, uso de recursos, holguras, avisos de casos especiales y comprobación |
| **6 · Sensibilidad** | Precios sombra, costos reducidos, rangos de cada **cⱼ** y de cada **bᵢ**, matriz B⁻¹ y una frase de interpretación para cada uno |
| **7 · Reporte** | Todo el procedimiento en texto (solo lectura). Se puede seleccionar y copiar con **Ctrl + C** |

### 7.4 Cómo escribir los números

| Se acepta | Ejemplo | No se acepta | Por qué |
|---|---|---|---|
| Enteros | `12`, `-3` | `1.250.000` | No use separador de miles: escriba `1250000` |
| Decimal con punto | `2.5` | `1,5.2` | Mezcla coma y punto |
| Decimal con coma | `2,5` | `abc` | No es un número |
| Fracción | `3/4` | `3/0` | División por cero |
| Notación científica | `1e3` | (vacío) | Toda casilla numérica debe tener un valor |

### 7.5 Botones y atajos

| Botón / atajo | Acción |
|---|---|
| **Cargar ejemplo** | Llena el formulario con el ejemplo elegido |
| **Abrir…** | Abre un problema guardado (`.json`) |
| **Guardar…** | Guarda el problema actual en `.json` |
| **Limpiar** | Borra el formulario |
| **Rellenar vacíos con 0** | Pone 0 en todas las casillas numéricas vacías |
| **Ctrl + Enter** o **F5** | Resolver (desde la pantalla del Simplex) |
| **Enter** | Pasar a la siguiente casilla |
| **F1** | Abrir la ayuda |
| **Shift + rueda del ratón** | Desplazar horizontalmente una tabla ancha |

---

## 8. Ejemplos precargados

Están en `ejemplos/simplex/` como archivos `.json`. Se cargan desde **Ejemplos → Cargar ejemplo**.

| N.º | Ejemplo | Tipo |
|---|---|---|
| **01** | **Caso real: Cementos Argos – producción semanal de concreto** | Maximizar · 3 × 4 |
| 02 | Minimización del costo neto de tres mezclas | Minimizar · 3 × 3 |
| 03 | Caso especial: problema **NO ACOTADO** | Maximizar · 2 × 2 |
| 04 | Caso especial: **óptimos ALTERNATIVOS** | Maximizar · 2 × 2 |
| 05 | Caso especial: **DEGENERACIÓN** (empate en la razón mínima) | Maximizar · 2 × 2 |
| 06 | Prueba de **tamaño máximo 8 × 8** | Maximizar · 8 × 8 |

### Guardar un problema nuevo

Escriba los datos en **1 · Datos**, pulse **Guardar…** y guárdelo en `ejemplos/simplex/`. Aparecerá en la lista de ejemplos. **No hay que modificar el código.**

---

## 9. Estructura del proyecto

```
IO1_Grupo9/
├── main.py                            Archivo principal que se ejecuta
├── README.md                          Guía
├── requirements.txt
│
├── modelo/                            ── MATEMÁTICA DEL MÉTODO ──
│   ├── numeros.py                     Números exactos (fracciones)
│   ├── excepciones.py                 Errores de validación y de archivos
│   ├── caso_especial.py               Avisos de casos especiales
│   ├── repositorio.py                 Leer y guardar problemas en JSON
│   └── simplex/
│       ├── problema_pl.py             Clases del problema de PL
│       ├── validador_pl.py            Validación de datos del PL
│       ├── tabla_simplex.py           Tabla Simplex: Zj, Cj − Zj y pivoteo de Gauss-Jordan
│       ├── solver_simplex.py          MÉTODO SIMPLEX paso a paso
│       └── sensibilidad.py            Precios sombra, costos reducidos, rangos de cj y bi
│
├── vista/                             ── INTERFAZ GRÁFICA ──
│   ├── tema.py                        Colores, fuentes y estilos
│   ├── formato.py                     Formato fracción/decimal
│   ├── ventana_principal.py           Ventana, barra lateral y navegación
│   ├── vista_inicio.py                Pantalla de inicio
│   ├── vista_ayuda.py                 Ayuda dentro del programa
│   ├── componentes/                   Tablas, tarjetas, avisos, reporte
│   ├── explicaciones/                 Textos del paso a paso (Simplex y sensibilidad)
│   ├── reportes/                      Reporte en texto
│   └── simplex/                       Pestañas del Método Simplex
│
├── controlador/                       ── CONEXIÓN VISTA ↔ MODELO ──
│   ├── controlador_principal.py       Crea la ventana, la navegación y los atajos de teclado
│   └── controlador_simplex.py         Acciones del Simplex
│
├── ejemplos/
│   └── simplex/                       Caso real Argos más problemas de prueba
│
└── tests/                             ── PRUEBAS AUTOMÁTICAS ──
    ├── test_numeros.py
    ├── test_simplex.py
    ├── test_sensibilidad.py
    └── test_validacion.py
```

---

## 10. Declaración de uso de IA

El grupo declara que utilizó herramientas de inteligencia artificial únicamente como **apoyo**, no para resolver los métodos.

El modelo matemático, la formulación del caso real, la lógica de los algoritmos, la interpretación de los resultados y las conclusiones son trabajo propio del grupo.

| Herramienta | Para qué se usó | Cómo se verificó |
|---|---|---|
| Asistente de IA (Claude) | Sugerencias para estructurar el código en el patrón MVC y ayuda para redactar los comentarios y este manual (README). | El grupo revisó que la separación en Modelo, Vista y Controlador fuera correcta, revisó cada comentario y comprobó que el README describe fielmente el proyecto. |
| Asistente de IA (Claude) | Ayuda para identificar errores de ejecución (depuración), corregir referencias rotas entre archivos y explicar mensajes de error de Python y PyCharm. | Se ejecutó el programa y las pruebas automáticas después de cada corrección, y se revisó cada pantalla a mano. |
| Validación con Libro de Taha, *Investigación de Operaciones* (Pearson) | Referencia académica para comprobar que el software resuelve correctamente, usando ejercicios ya resueltos del libro. | El software coincidió con el libro: modelo Reddy Mikks (Simplex). |
