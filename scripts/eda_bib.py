from pybtex.database import parse_file
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import plotly.express as px

def convert_bib_to_df(file_paths):
    # Lista para almacenar los datos extraídos de todos los archivos
    all_data = []

    # Procesar cada archivo .bib
    for file_path in file_paths:
        # Cargar archivo .bib
        bib_data = parse_file(file_path)

        # Extraer los datos relevantes (incluyendo el país y la institución si están presentes)
        for key, entry in bib_data.entries.items():
            title = entry.fields.get('title', '')
            year = entry.fields.get('year', '')

            # Extraer autores
            authors = ' y '.join(str(person) for person in entry.persons.get('author', []))
            abstract = entry.fields.get('abstract', '')

            # Extraer keywords
            keywords = entry.fields.get('Keywords', '')

            # Extraer institución y país (asumiendo que pueden estar en varios campos)
            institution = entry.fields.get('institution', entry.fields.get('affiliation', ''))
            country = entry.fields.get('address', '')  # A veces el país puede estar en 'address' o 'location'
            journal = entry.fields.get('journal', '')

            # Agregar los datos extraídos a la lista
            all_data.append({
                'Key': key, 
                'Title': title, 
                'Authors': authors, 
                'Year': year, 
                'Abstract': abstract, 
                'Keywords': keywords, 
                'Institution': institution,
                'Country': country,
                'Journal': journal,
                'Language': entry.fields.get('language', '')
            })

    # Crear un DataFrame de pandas con todos los datos extraídos
    df = pd.DataFrame(all_data)
    df.drop_duplicates(subset='Title', inplace=True)
    return df

def keywords_word_cloud(df):
    # Concatenar todos los abstracts en una sola cadena
    text = " ".join(abstract for abstract in df['Abstract'] if abstract != 'Resumen no disponible')

    # Generar la nube de palabras con mayor tamaño y detalle
    wordcloud = WordCloud(max_font_size=100, max_words=200, background_color="white", width=1600, height=800).generate(text)
    plt.figure(figsize=(16, 8), dpi=300)
    # Mostrar la nube de palabras 
    plt.imshow(wordcloud, interpolation="hanning")
    plt.axis("off")  # Desactivar los ejes
    plt.show()

def bar_chart_keywords(df):
    # Convertir los keywords de cada artículo en una lista
    df['Keywords_list'] = df['Keywords'].apply(lambda x: [kw.strip() for kw in x.split(',')])

    # Eliminar keywords vacías (cadenas vacías "")
    df['Keywords_list'] = df['Keywords_list'].apply(lambda kw_list: [kw for kw in kw_list if kw])

    # Contar la frecuencia de cada keyword en todo el DataFrame
    all_keywords = df['Keywords_list'].explode()
    keyword_counts = Counter(all_keywords)

    # Convertir los datos a un DataFrame
    keyword_df = pd.DataFrame(keyword_counts.items(), columns=['Keyword', 'Frequency'])

    # Ordenar por frecuencia
    keyword_df = keyword_df.sort_values(by='Frequency', ascending=False).head(20)
    keyword_df = keyword_df.sort_values(by='Frequency', ascending=True)

    # Crear la gráfica de barras horizontales
    plt.figure(figsize=(12, 8))  # Ajustar el tamaño de la figura
    plt.barh(keyword_df['Keyword'], keyword_df['Frequency'], color='pink')

    # Títulos y etiquetas
    plt.title('Top 20 Keywords más usados', fontsize=18)
    plt.xlabel('Frecuencia de uso', fontsize=14)
    plt.ylabel('Keywords', fontsize=14)

    # Mostrar la gráfica
    plt.show()

def insert_line_break(text):
    words = text.split()  # Dividir el texto en palabras
    result = []
    # Agrupamos las palabras de dos en dos y añadimos un salto de línea
    for i in range(0, len(words), 2):
        result.append(" ".join(words[i:i+2]))  # Tomar de dos en dos
    return "<br>".join(result)  # Unir con un salto de línea

def journal_tree_map(df):
    journal_count = df.groupby('Journal').size().reset_index(name='Count')

    # Aplicar la función que inserta los saltos de línea a las etiquetas de los journals
    journal_count['Journal'] = journal_count['Journal'].apply(insert_line_break)

    # Crear el gráfico de Treemap
    fig = px.treemap(
        journal_count, 
        path=['Journal'], 
        values='Count', 
        color='Journal', 
        title='Treemap de Fuentes de Publicaciones (Journal)',
        color_discrete_sequence=px.colors.qualitative.Pastel  # Colores pastel para mejor contraste
    )

    fig.update_traces(
        textinfo="label+value", # Mostrar la etiqueta y el valor
        textfont_size=25,
        textfont_color='black',
        hovertemplate='<b>%{label}</b><br>Publicaciones: %{value}<extra></extra>',  # Personalizar tooltip
        marker=dict(line=dict(color='black', width=0.5))  # Añadir borde negro para más contraste
    )

    # Cambiar el tamaño de la gráfica para mejorar la visualización
    fig.update_layout(
        title_font_size=24,
        title_x=0.5,  # Centrar el título
        uniformtext=dict(minsize=11, mode='show'),
        margin=dict(t=50, l=25, r=25, b=25),  # Ajustar márgenes
        height=800,  # Ajustar la altura de la gráfica
        width=1200   # Ajustar el ancho de la gráfica
    )

    # Mostrar la gráfica
    fig.show()

def top_authors_chart(df):
    # Separar los autores en una lista
    df['Authors_list'] = df['Authors'].apply(lambda x: [author.strip() for author in x.split(' y ') if author.strip() != ''])

    # Explode para separar los autores en filas individuales
    df_exploded = df.explode('Authors_list')

    # Contar las publicaciones por autor y año
    author_year_counts = df_exploded.groupby(['Authors_list', 'Year']).size().reset_index(name='Publications')

    # Obtener los 20 autores más productivos
    top_authors = df_exploded['Authors_list'].value_counts().head(20).index
    top_author_data = author_year_counts[author_year_counts['Authors_list'].isin(top_authors)]
    top_author_data.loc[:, 'Year'] = pd.to_numeric(top_author_data['Year'], errors='coerce') # Convertir el año a numérico
    
    fig = px.scatter(
        top_author_data, 
        x='Year', 
        y='Authors_list', 
        size='Publications', 
        color='Authors_list', 
        hover_name='Authors_list', 
        title='Productividad de los 20 Autores Más Productivos',
        size_max=15,  # Tamaño máximo de los puntos
        category_orders={"Authors_list": top_authors}  
    )

    fig.update_layout(
        height=600,
        yaxis=dict(tickmode='linear'),
        xaxis=dict(type='category', categoryorder='category ascending')
    )

    # Mostrar el gráfico
    fig.show()
