# Verifica si el entorno 'bib_analysis' ya existe
if conda info --envs | grep -q "bib_analysis"; then
    echo "El entorno 'bib_analysis' ya existe."
else
    echo "Creando el entorno 'bib_analysis'..."
    conda create --name bib_analysis python=3.11 -y
fi

# Activa el shell de conda
eval "$(conda shell.bash hook)"

# Activa el entorno (usando 'source' para asegurarse de que funcione en scripts)
echo "Activando el entorno 'bib_analysis'..."
source activate bib_analysis

# Instala el kernel de Jupyter
echo "Instalando ipykernel para Jupyter..."
conda install ipykernel -y

# Actualiza pip y setuptools
echo "Actualizando pip y setuptools..."
pip install --upgrade pip setuptools

# Instala las dependencias desde requirements.txt si existe
if [ -f "requirements.txt" ]; then
    echo "Instalando las dependencias desde requirements.txt..."
    pip install -r requirements.txt
else
    echo "El archivo 'requirements.txt' no se encuentra."
    exit 1
fi

# Verifica la instalación de las dependencias
echo "Verificando la instalación de las dependencias..."
pip check