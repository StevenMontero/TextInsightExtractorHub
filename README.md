# TextInsightExtractorHub

NLPKeyExtractor es una herramienta de procesamiento de lenguaje natural diseñada para analizar textos y extraer información clave de manera eficiente. La aplicación utiliza técnicas avanzadas de procesamiento de texto y algoritmos de extracción de palabras y frases significativas.

## Estructura del Proyecto

```
\---hot-words-project
|   .gitignore
|   docker-compose.yml
|   Dockerfile
|   estructura_proyecto.txt
|   README.md
|   requirements.txt
|   
\---src
    |   main.py
    |   __init__.py
    |   
    +---config
    |   |   common_word.py
    |   |   config.yml
    |   |   config_loader.py
    |   |   __init__.py
    |   |   
    |   \---__pycache__
    |           common_word.cpython-38.pyc
    |           __init__.cpython-38.pyc
    |           
    +---schemas
    |   |   schemas.py
    |   |   __init__.py
    |   |   
    |   \---__pycache__
    |           KeyPhrases.cpython-38.pyc
    |           KeyTokens.cpython-38.pyc
    |           schemas.cpython-38.pyc
    |           __init__.cpython-38.pyc
    |           
    \---__pycache__
            common_word.cpython-38.pyc
            main.cpython-38.pyc

```


- **.gitignore**: Archivo de configuración de git para ignorar archivos/directorios específicos.
- **docker-compose.yml**: Archivo de configuración para Docker Compose.
- **Dockerfile**: Archivo de configuración para construir la imagen Docker.
- **estructura_proyecto.txt**: Descripción de la estructura del proyecto.
- **README.md**: Este archivo, proporcionando información sobre el proyecto.
- **requirements.txt**: Archivo que enumera las dependencias del proyecto.
- **src/**: Directorio principal del código fuente.
  - **main.py**: Archivo principal que contiene la lógica principal de la aplicación.
  - **__init__.py**: Archivo de inicialización para el paquete src.
  - **config/**: Directorio que contiene archivos relacionados con la configuración.
    - **common_word.py**: Archivo con palabras comunes.
    - **config.yml**: Archivo de configuración YAML.
    - **config_loader.py**: Archivo para cargar configuraciones.
    - **__init__.py**: Archivo de inicialización para el paquete config.
  - **schemas/**: Directorio que contiene esquemas de datos.
    - **schemas.py**: Archivo que define los esquemas.
    - **__init__.py**: Archivo de inicialización para el paquete schemas.
  - **__pycache__**: Directorio que almacena archivos compilados (puedes agregarlo a .gitignore).

## Cómo Ejecutar el Proyecto con Docker

Asegúrate de tener Docker y Docker Compose instalados en tu máquina.

1. Clona el repositorio:

    ```bash
    git clone https://github.com/tu_usuario/tu_proyecto.git
    cd tu_proyecto
    ```

2. Construye la imagen Docker:

    ```bash
    docker-compose build
    ```

3. Ejecuta el contenedor:

    ```bash
    docker-compose up
    ```

    El servicio estará disponible en [http://localhost:8000](http://localhost:8000).

    El la documentación del servicio estará disponible en [http://localhost:8000/docs#/](http://localhost:8000/docs#/).

4. Para detener el servicio, presiona `Ctrl + C` en la terminal y ejecuta:

    ```bash
    docker-compose down
    ```



# Instalación de Docker en caso de no tenerlo

Docker es una plataforma que facilita la creación, implementación y ejecución de aplicaciones en contenedores. A continuación, se detallan los pasos para instalar Docker en diferentes sistemas operativos:

## Instalación en Linux

1. Actualiza el índice de paquetes:

    ```bash
    sudo apt-get update
    ```

2. Instala los paquetes necesarios para permitir que APT utilice un repositorio sobre HTTPS:

    ```bash
    sudo apt-get install \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    ```

3. Agrega la clave GPG oficial de Docker:

    ```bash
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    ```

4. Configura el repositorio estable de Docker:

    ```bash
    echo \
        "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    ```

5. Actualiza el índice de paquetes nuevamente y luego instala Docker:

    ```bash
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io
    ```

6. Verifica la instalación ejecutando el contenedor "hello-world":

    ```bash
    sudo docker run hello-world
    ```

## Instalación en macOS

1. Descarga [Docker Desktop for Mac](https://desktop.docker.com/mac/stable/Docker.dmg) desde el sitio web oficial de Docker.

2. Abre el archivo descargado (Docker.dmg) y arrastra Docker a la carpeta de Aplicaciones.

3. Abre Docker desde la carpeta de Aplicaciones.

4. Verifica la instalación ejecutando el contenedor "hello-world" desde un terminal:

    ```bash
    docker run hello-world
    ```

## Instalación en Windows

1. Descarga [Docker Desktop for Windows](https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe) desde el sitio web oficial de Docker.

2. Ejecuta el instalador descargado y sigue las instrucciones.

3. Verifica la instalación ejecutando el contenedor "hello-world" desde PowerShell o el símbolo del sistema:

    ```powershell
    docker run hello-world
    ```

¡Ahora estás listo para utilizar Docker en tu sistema operativo!


# Ejmplo de uso con python
```python

import pandas as pd
import requests
import json
import numpy as np

df_mayo = pd.read_csv('../data/raw/HistorialGenesysAbril.csv',low_memory=False)
# URL de tu API local
url = "http://localhost:8000/extract_keywords"  # Ajusta el puerto si es diferente

# Datos para enviar en la solicitud POST
data = df_mayo['Mensaje'].head(1000).tolist()

# Convertir números especiales a representaciones legales antes de la serialización JSON
def handle_special_floats(obj):
    if isinstance(obj, (float, np.floating)) and (np.isinf(obj) or np.isnan(obj)):
        return str(obj)  # Convertir infinito a una cadena
    return obj

# Convertir números especiales antes de enviar los datos
data = [handle_special_floats(value) for value in data]


json_data = {
  
  "messages_list": data
}


# Hacer la solicitud POST
response = requests.post(url, json=json_data)

# Verificar el código de estado de la respuesta
if response.status_code == 200:
    # Imprimir los resultados
    print(response.json())
else:
    print(f"Error en la solicitud: {response.status_code}")
    print(response.text)


```

### Resultado:

![Alt text](image.png)





