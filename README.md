# Bibliometrics Analysis

Este repositorio contiene el análisis bibliométrica del proyecto **Desarrollo de un Modelo Predictivo para la Identificación Temprana de Estudiantes en Riesgo de Fracaso Escolar**. A través de la bibliometría, se analiza la literatura científica sobre sistemas de alerta temprana, modelos predictivos y factores de riesgo escolar.

El análisis incluye la consolidación de datos bibliográficos, extracción de palabras clave y autores relevantes, visualizaciones como nubes de palabras, gráficos de barras y treemaps, y el uso de técnicas NLP para identificar los artículos más relevantes. Todo el análisis ha sido realizado utilizando `pyBibX` y bibliotecas de análisis de Python como `pandas` y `plotly`.

## Estructura del Proyecto

### Carpeta `resultados_consolidados/`
Contiene archivos `.bib` y `.ris` que consolidan los resultados de las bases de datos bibliográficas consultadas. Cada archivo representa un tema específico relacionado con el proyecto.

- **Archivos .bib y .ris**: Exportaciones de diferentes bases de datos científicas como ERIC, Web of Science, y otras. Estos archivos son la fuente primaria para los análisis.

Archivos relevantes:
- `dropout_prediction_consolidado.bib`: Contiene la bibliografía relacionada con predicción de deserción escolar.
- `moodle_consolidado.bib`: Contiene la bibliografía relacionada con Moodle y su uso en la educación.
- `processes_consolidado.bib`: Contiene la bibliografía sobre procesos educativos.
- `risk_detection_consolidado.bib`: Enfocado en la detección de riesgos tempranos en el ámbito educativo.
- `student_performance_prediction_consolidado.bib`: Contiene la bibliografía sobre la predicción del rendimiento estudiantil.

### Notebooks de análisis (_analysis.ipynb)

Cada uno de los notebooks contiene análisis detallados de la bibliografía consolidada en distintos temas. Estos notebooks realizan las siguientes tareas:

- **Consolidación por tema**: Cada notebook agrupa y procesa la bibliografía relevante de un tema particular (p. ej., predicción de deserción escolar, Moodle, procesos educativos).
- **Nube de palabras**: Se generan nubes de palabras para destacar los términos clave más usados en la literatura consultada.
- **Gráfico de barras de keywords**: Se visualizan las palabras clave más frecuentes en la literatura.
- **Treemap de journals**: Visualización de las fuentes de publicación (journals) más frecuentes en la bibliografía.
- **Gráfica de autores más productivos**: Identificación y visualización de los autores más activos en el campo.
- **Visualización con VOSviewer**: Se utiliza el software VOSviewer para generar mapas de co-citación y co-ocurrencia, lo cual facilita la identificación de patrones y relaciones entre autores, temas y palabras clave.

Notebooks clave:
- `dropout_analysis.ipynb`: Análisis de bibliografía sobre deserción escolar.
- `moodle_analysis.ipynb`: Análisis de bibliografía relacionada con el uso de Moodle en el ámbito educativo.
- `processes_analysis.ipynb`: Análisis sobre los procesos educativos en general.
- `risk_detection_analysis.ipynb`: Análisis sobre la detección de riesgos tempranos.
- `student_performance_prediction_analysis.ipynb`: Análisis sobre la predicción del rendimiento estudiantil.

### Archivo `most_relevant_bibliography.ipynb`

Este notebook contiene todos los análisis relacionados con el procesamiento de lenguaje natural (NLP) para identificar los artículos más relevantes. Utiliza métodos de NLP para calcular la relevancia de los artículos basándose en keywords y otros criterios de búsqueda.

### Scripts adicionales

- **`convert_nbib_to_bib.py`**: Script para convertir archivos en formato NBIB a BIB.
- **`merge_bib.py`**: Script que permite consolidar múltiples archivos `.bib` en uno solo, eliminando duplicados y facilitando el manejo de la bibliografía.

## Instalación

Para ejecutar los notebooks y scripts de este repositorio, asegúrate de instalar todas las dependencias necesarias. Puedes hacer esto ejecutando el siguiente comando:

```bash
pip install -r requirements.txt
```