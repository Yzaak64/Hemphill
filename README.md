# Analizador de Cuestionario Hemphill <a href="https://www.buymeacoffee.com/Yzaak64" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-green.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

Aplicación de escritorio desarrollada con Python y Tkinter para digitalizar, calificar y analizar los resultados del "Cuestionario de Descripción de Grupos" de J.K. Hemphill.

## Características

*   **Entrada Manual del Cuestionario:** Una interfaz guiada para responder las 150 preguntas del cuestionario para un participante individual.
*   **Procesamiento Masivo desde CSV:** Carga y procesa archivos CSV (por ejemplo, exportados desde Google Forms) que contienen las respuestas de múltiples participantes, calculando perfiles individuales y un promedio grupal.
*   **Análisis de 13 Dimensiones:** Calcula las puntuaciones crudas y las convierte a puntuaciones estaninas (1-9) para las 13 dimensiones del grupo: Autonomía, Control, Flexibilidad, Tono Hedónico, Homogeneidad, Intimidad, Participación, Permeabilidad, Polarización, Potencia, Estabilidad, Estratificación y Viscosidad.
*   **Visualización Gráfica:** Genera un gráfico de barras de perfil para cada resultado (individual o promedio), mostrando las puntuaciones estaninas con bandas de color para una interpretación rápida (Bajo, Promedio, Alto).
*   **Exportación de Resultados:** Permite exportar tanto la vista actual (el perfil de un participante o el promedio) como una tabla consolidada con todos los resultados de todos los participantes, ideal para análisis estadísticos.
*   **Generación de Plantillas:** Crea archivos CSV de ejemplo para facilitar la recolección de datos.
*   **Manual de Usuario Integrado:** Incluye un manual en PDF generado dinámicamente que explica el uso de la herramienta y la configuración de formularios.

## Requisitos (para ejecutar desde el código fuente)

*   Python 3.x
*   Librerías listadas en `requirements.txt`. Puedes instalarlas usando pip:
    ```bash
    pip install -r requirements.txt
    ```
    Las principales dependencias son:
    *   `pandas`
    *   `matplotlib`
    *   `reportlab`
    *   `Pillow`

## Uso

**Opción 1: Ejecutar desde el Código Fuente**

1.  Asegúrate de tener Python y las librerías requeridas instaladas.
2.  Clona o descarga este repositorio.
3.  Abre una terminal o símbolo del sistema en la carpeta del proyecto.
4.  Ejecuta el script principal:
    ```bash
    python Hemphill_App.py
    ```
5.  Sigue las opciones en la interfaz gráfica que aparecerá.

**Opción 2: Usar el Ejecutable (Windows)**

1.  Ve a la sección [**Releases**](https://github.com/TuUsuario/Hemphill-Questionnaire-Analyzer/releases) de este repositorio. *(Recuerda cambiar `TuUsuario` y el nombre del repo por los tuyos)*.
2.  Descarga el archivo `.zip` de la última versión disponible (ej. `Hemphill_v1.0.zip`).
3.  Descomprime la carpeta en tu computadora.
4.  Haz doble clic en el archivo `Hemphill.exe` para iniciar la aplicación. No requiere instalación de Python.

**Opción 3: Probar en Google Colab (Demo Online)**

1.  Haz clic en el siguiente enlace para abrir una versión del núcleo de la aplicación directamente en tu navegador usando Google Colab:
    [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/16CYD5wdEWsZd34SYYGjg1xdC-EM8JEas)
    *(O copia y pega esta URL: `https://colab.research.google.com/drive/16CYD5wdEWsZd34SYYGjg1xdC-EM8JEas`)*
2.  Es posible que Colab muestre una advertencia. Haz clic en "Ejecutar de todos modos".
3.  Ejecuta las celdas de código. **Nota:** Esta versión de Colab se enfoca en la lógica de cálculo y la generación del gráfico. Las funciones de la interfaz gráfica no estarán disponibles.

## Generación del Ejecutable (Instrucciones para desarrollador)

Si deseas crear el archivo `.exe` tú mismo desde el código fuente:

1.  Asegúrate de tener Python y las librerías de `requirements.txt` instaladas en tu entorno (preferiblemente un entorno virtual).
2.  Instala PyInstaller: `pip install pyinstaller`
3.  Navega a la carpeta raíz del proyecto en tu terminal.
4.  Asegúrate de que el archivo de ícono `Hemphill.ico` y la imagen `Buy_Coffe.png` estén presentes.
5.  Ejecuta el comando usando el archivo de configuración `.spec` (recomendado):
    ```bash
    pyinstaller Hemphill_App.spec
    ```
6.  La aplicación completa (`Hemphill.exe` y sus dependencias) se encontrará en la subcarpeta `dist/Hemphill`.

## Notas

*   El procesamiento de archivos CSV espera que la primera columna contenga el nombre del participante y las siguientes 150 columnas contengan las respuestas numéricas (de 1 a 5) en el orden correcto.
*   El botón "Ver Manual de Instrucciones" generará el archivo `manual_hemphill.pdf` en la misma carpeta del ejecutable si no existe, y luego lo abrirá.