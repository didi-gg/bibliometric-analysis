import bibtexparser
import os

queries = {
    'dropout_prediction': {
        'ERIC': './bibliography/ERIC/e_Dropout_Prediction.bib',
        'Sage Journals': './bibliography/Sage Journals/sj_Dropout_Prediction.bib',
        'Science Direct': './bibliography/Science Direct/sd_Dropout_Prediction.bib',
        'Web of Science': './bibliography/Web of Science/wos_Dropout_Prediction.bib'
    },
    'moodle': {
        'ERIC': './bibliography/ERIC/e_moodle.bib',
        'Sage Journals': './bibliography/Sage Journals/sj_moodle.bib',
        'Science Direct': './bibliography/Science Direct/sd_moodle.bib',
        'Web of Science': './bibliography/Web of Science/wos_moodle.bib'
    },
    'risk_detection': {
        'ERIC': './bibliography/ERIC/e_Risk_Detection.bib',
        'Sage Journals': './bibliography/Sage Journals/sj_Risk_Detection.bib',
        'Science Direct': './bibliography/Science Direct/sd_Risk_Detection.bib',
        'Web of Science': './bibliography/Web of Science/wos_Risk_Detection.bib'
    },
    'student_performance_prediction': {
        'ERIC': './bibliography/ERIC/e_Student_Performance_Prediction.bib',
        'Sage Journals': './bibliography/Sage Journals/sj_Student_Performance_Prediction.bib',
        'Science Direct': './bibliography/Science Direct/sd_Student_Performance_Prediction.bib',
        'Web of Science': './bibliography/Web of Science/wos_Student_Performance_Prediction.bib'
    },
    'processes': {
        'ERIC': './bibliography/ERIC/e_processes.bib',
        'Science Direct': './bibliography/Science Direct/sd_processes.bib',
        'Web of Science': './bibliography/Web of Science/wos_processes.bib'
    }
}

# Función para cargar un archivo .bib y agregar etiqueta según la base de datos
def cargar_bibtex_con_etiqueta(file_path, etiqueta):
    with open(file_path) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    # Agregar la etiqueta de la base de datos de origen
    for entry in bib_database.entries:
        entry['database'] = etiqueta

    return bib_database.entries

# Función para eliminar duplicados basados en el título o DOI
def eliminar_duplicados(articulos):
    articulos_unicos = []
    seen = set()

    for articulo in articulos:
        # Verificar duplicados con el DOI y el título
        unique_key = articulo.get('title', '').lower() or articulo.get('doi', '').lower()
        
        if unique_key and unique_key not in seen:
            articulos_unicos.append(articulo)
            seen.add(unique_key)

    return articulos_unicos

# Función para consolidar varios archivos .bib de un grupo
def consolidar_archivos_bib(grupo_bib):
    articulos_consolidados = []

    for base_de_datos, archivo in grupo_bib.items():
        articulos = cargar_bibtex_con_etiqueta(archivo, base_de_datos)
        articulos_consolidados.extend(articulos)

    # Eliminar duplicados
    articulos_unicos = eliminar_duplicados(articulos_consolidados)
    
    return articulos_unicos

# Función para guardar los resultados en un archivo .bib consolidado
def guardar_bibtex(articulos, output_path):
    bib_database = bibtexparser.bibdatabase.BibDatabase()
    bib_database.entries = articulos

    with open(output_path, 'w') as bibtex_file:
        writer = bibtexparser.bwriter.BibTexWriter()
        bibtex_file.write(writer.write(bib_database))
    print(f"Archivo .bib consolidado guardado en: {output_path}")

# Función principal para consolidar todos los archivos .bib según los grupos de queries
def consolidar_todos_los_grupos(queries):
    for grupo, archivos_bib in queries.items():
        # Consolidar archivos dentro de cada grupo
        articulos_consolidados = consolidar_archivos_bib(archivos_bib)
        
        # Guardar el archivo consolidado para cada grupo
        output_file = f'resultados_consolidados/{grupo}_consolidado.bib'
        guardar_bibtex(articulos_consolidados, output_file)

# Crear el directorio de salida si no existe
if not os.path.exists('resultados_consolidados'):
    os.makedirs('resultados_consolidados')

# Ejecutar la consolidación para todos los grupos
consolidar_todos_los_grupos(queries)
