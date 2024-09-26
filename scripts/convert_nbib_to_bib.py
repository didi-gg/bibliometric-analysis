from Bio import Medline
import re

# Lista de rutas de archivos NBIB
file_paths = [
    "./bibliography/ERIC nbib/e_Dropout_Prediction.nbib",
    "./bibliography/ERIC nbib/e_moodle.nbib",
    "./bibliography/ERIC nbib/e_processes.nbib",
    "./bibliography/ERIC nbib/e_Risk_Detection.nbib",
    "./bibliography/ERIC nbib/e_Student_Performance_Prediction.nbib",
]

# Función para extraer el año utilizando una expresión regular
def extract_year(date_string):
    # Patrón regex para capturar un año de 4 dígitos
    match = re.search(r'\b(19|20)\d{2}\b', date_string)
    if match:
        return match.group(0)  # Devuelve el primer match (el año)
    return "2020"  # Valor por defecto si no se encuentra el año

# Función para convertir NBIB a formato BIB
def convert_nbib_to_bib(file_path):
    with open(file_path, 'r') as nbib_file:
        records = Medline.parse(nbib_file)
        bib_entries = []
        
        for record in records:
            # Obtener el identificador (OID) y asegurarse de que sea una cadena
            oid = record.get('OID', 'Unknown')
            if isinstance(oid, list):
                oid = oid[0]  # Toma el primer elemento de la lista si es una lista
            
            # Inicializar la entrada
            entry = "@article{" + oid + ",\n"

            # Agregar el título
            entry += "Title = {" + record.get('TI', '') + "},\n"
            
            # Unir la lista de autores usando 'and'
            authors = record.get('AU', [])
            entry += "Author = {" + ' and '.join(authors) + "},\n"
            
            # Agregar el nombre de la revista
            entry += "Journal = {" + record.get('JT', '') + "},\n"
            
            # Extraer el año utilizando la función personalizada
            full_date = record.get('DP', '')
            year = extract_year(full_date)
            entry += "Year = {" + year + "},\n"
            
            # Agregar el volumen y las páginas
            entry += "Volume = {" + record.get('VI', '') + "},\n"
            entry += "Pages = {" + record.get('PG', '') + "},\n"
            
            # Agregar el DOI si está disponible
            entry += "DOI = {" + record.get('LID', '') + "},\n"
            
            # Agregar el abstract
            entry += "Abstract = {" + record.get('AB', '') + "},\n"
            
            # Extraer las palabras clave (descriptores)
            keywords = record.get('OT', [])
            if keywords:
                entry += "Keywords = {" + ', '.join(keywords) + "},\n"
            
            # Agregar ISSN y EISSN asegurándose de que no sean listas
            issn = record.get('ISSN', '')
            if isinstance(issn, list):
                issn = issn[0]  # Si es una lista, tomar el primer elemento
            if issn:
                entry += "ISSN = {" + issn + "},\n"
            
            eissn = record.get('EISSN', '')
            if isinstance(eissn, list):
                eissn = eissn[0]  # Si es una lista, tomar el primer elemento
            if eissn:
                entry += "EISSN = {" + eissn + "},\n"
            
            # Incluir el tipo de publicación (PT)
            pub_type = record.get('PT', [])
            if pub_type:
                entry += "Type = {" + ', '.join(pub_type) + "},\n"
            
            # Incluir el idioma (LA) asegurándose de que no sea una lista
            language = record.get('LA', '')
            if isinstance(language, list):
                language = language[0]  # Si es una lista, tomar el primer elemento
            if language:
                entry += "Language = {" + language + "},\n"
            
            # Finalizar la entrada
            entry += "}\n"
            bib_entries.append(entry)

    return "\n\n".join(bib_entries)

# Convertir todos los archivos NBIB y guardarlos como archivos BIB
converted_files = {}
for file_path in file_paths:
    bib_content = convert_nbib_to_bib(file_path)
    output_path = file_path.replace('.nbib', '.bib')
    with open(output_path, 'w') as bib_file:
        bib_file.write(bib_content)
    converted_files[file_path] = output_path

# Imprimir archivos convertidos
print("Archivos NBIB convertidos a BIB:")
for nbib, bib in converted_files.items():
    print(f"{nbib} -> {bib}")