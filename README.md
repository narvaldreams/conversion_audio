# conversion_audio
Script para covertir archivos de audio mp3, flac, ogg o wma a mp3 o flac dejando un formato &lt;track>-&lt;artist>-&lt;title>
## Instalación

```bash
git clone https://github.com/usuario/nombre-del-proyecto.git
cd nombre-del-proyecto
# Instala las dependencias
Instarlar python3, pydub, mutagen
npm install   # o pip install -r requirements.txt según el lenguaje
```

## Uso

## CONFIGURACIÓN

SOURCE_DIR = "./musica_origen"       # Directorio donde están tus archivos de audio originales

DEST_DIR = "./musica_destino"        # Directorio donde se guardarán los MP3 convertidos

BITRATE = "320k"                  # Calidad del MP3 de salida (ej. "320k", "192k")

SEPARATOR = " - "                 # Separador entre artista y canción en el nombre del archivo

EXT = "mp3"                       # Extensión de formato de sonido, ahorita solo funciona con mp3 y flac

DELETE_PROCESSED = True           # Eliminar archivos originales después de conversión exitosa

```bash
# Ejemplo de cómo ejecutar el proyecto
source .venv/bin/activate
python3 conversion2.py 
```

## Ejemplo

~/Música$ python3 conversion2.py 
Iniciando el proceso de conversión...
Directorio de origen: ./Conversion
Directorio de destino: ./Lista (Calidad: 320k)
Eliminar originales: Sí
--------------------------------------------------
Procesando: 11.Muñequita Sintetica.mp3
  Convirtiendo '11.Muñequita Sintetica.mp3' a '11 - Luis Alvarez - Muñequita Sintetica.mp3'...
  Conversión exitosa. Actualizando metadatos...
  Metadatos actualizados en '11 - Luis Alvarez - Muñequita Sintetica.mp3'.
  Archivo original 11.Muñequita Sintetica.mp3 eliminado.
--------------------------------------------------
Procesando: 16.No Tengo Tiempo.mp3
  Convirtiendo '16.No Tengo Tiempo.mp3' a '16 - Rodrigo Gonzalez - No Tengo Tiempo.mp3'...
  Conversión exitosa. Actualizando metadatos...
  Metadatos actualizados en '16 - Rodrigo Gonzalez - No Tengo Tiempo.mp3'.
  Archivo original 16.No Tengo Tiempo.mp3 eliminado.
--------------------------------------------------

```

## Contribuir

¿Quieres contribuir? Consulta [CONTRIBUTING.md](CONTRIBUTING.md).

## Licencia

Este proyecto está bajo la licencia MIT.
