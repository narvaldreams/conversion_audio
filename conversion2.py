import os
import re
from pydub import AudioSegment
from mutagen import File
from mutagen.id3 import ID3NoHeaderError
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER, TCON

# --- CONFIGURACIÓN ---
SOURCE_DIR = "./Conversion"       # Directorio donde están tus archivos de audio originales
DEST_DIR = "./Lista"              # Directorio donde se guardarán los MP3 convertidos
BITRATE = "320k"                  # Calidad del MP3 de salida (ej. "320k", "192k")
SEPARATOR = " - "                 # Separador entre artista y canción en el nombre del archivo
EXT = "mp3"                       # Extensión de formato de sonido
DELETE_PROCESSED = True           # Eliminar archivos originales después de conversión exitosa

# --- FUNCIONES ---
    
def clean_filename(filename):
    """Limpia una cadena para que sea un nombre de archivo válido.
    
    Args:
        filename (str): Nombre del archivo a limpiar.
        
    Returns:
        str: Nombre del archivo limpio, sin caracteres inválidos.
    """
    filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
    filename = re.sub(r'\.+', '_', filename)
    filename = re.sub(r'\s+', ' ', filename).strip()
    return filename

def get_metadata(filepath):
    """Extrae metadatos de un archivo de audio.
    
    Args:
        filepath (str): Ruta completa al archivo de audio.
        
    Returns:
        dict: Diccionario con los metadatos encontrados (artist, title, album, genre, track).
    """
    metadata = {'artist': None, 'title': None, 'album': None, 'genre': None, 'track': None, 'ID3': None}
    try:
        audio = File(filepath)
        if audio is None:
            print(f"  Advertencia: No se pudieron leer los metadatos de {os.path.basename(filepath)}")
            return metadata

        if filepath.lower().endswith('.mp3'):
            if 'TPE1' in audio: metadata['artist'] = audio['TPE1'].text[0]
            if 'TIT2' in audio: metadata['title'] = audio['TIT2'].text[0]
            if 'TALB' in audio: metadata['album'] = audio['TALB'].text[0]
            if 'TCON' in audio: metadata['genre'] = audio['TCON'].text[0]
            if 'TRCK' in audio: metadata['track'] = audio['TRCK'].text[0]
        elif filepath.lower().endswith(('.flac', '.ogg')):
            if 'artist' in audio: metadata['artist'] = audio.get('artist', [None])[0]
            if 'title' in audio: metadata['title'] = audio.get('title', [None])[0]
            if 'album' in audio: metadata['album'] = audio.get('album', [None])[0]
            if 'genre' in audio: metadata['genre'] = audio.get('genre', [None])[0]
            if 'tracknumber' in audio: metadata['track'] = audio.get('tracknumber', [None])[0]
        elif filepath.lower().endswith('.wma'):
            if 'Author' in audio: metadata['artist'] = str(audio['Author'][0])
            if 'Title' in audio: metadata['title'] = str(audio['Title'][0])
            if 'WM/AlbumTitle' in audio: metadata['album'] = str(audio['WM/AlbumTitle'][0])
            if 'WM/Genre' in audio: metadata['genre'] = str(audio['WM/Genre'][0])
            if 'WM/TrackNumber' in audio: metadata['track'] = str(audio['WM/TrackNumber'][0])

        return metadata
    except ID3NoHeaderError:
        print(f"  Advertencia: No se encontraron metadatos ID3 válidos en {os.path.basename(filepath)}")
        return metadata
    except Exception as e:
        print(f"  Error al leer metadatos de {os.path.basename(filepath)}: {e}")
        return metadata

def delete_processed_file(filepath):
    """Elimina un archivo original después de una conversión exitosa.
    
    Args:
        filepath (str): Ruta completa al archivo a eliminar.
        
    Returns:
        bool: True si se eliminó correctamente, False si hubo error.
    """
    if not DELETE_PROCESSED:
        return False
        
    try:
        os.remove(filepath)
        print(f"  Archivo original {os.path.basename(filepath)} eliminado.")
        return True
    except Exception as e:
        print(f"  Error al eliminar archivo original {os.path.basename(filepath)}: {e}")
        return False

def format_track_number(track):
    """Formatea el número de pista para asegurar consistencia.
    
    Args:
        track (str): Número de pista en cualquier formato.
        
    Returns:
        str: Número de pista formateado como dos dígitos (ej. '01', '12').
    """
    if not track:
        return None
        
    # Extraer solo los dígitos del número de pista
    digits = re.sub(r'\D', '', track)
    
    if not digits:
        return None
        
    # Formatear como dos dígitos
    return f"{int(digits):02d}"

def convert_and_rename_audio():
    """Función principal que convierte, renombra y etiqueta los archivos.
    
    Procesa todos los archivos de audio en el directorio origen, los convierte a MP3
    con los metadatos correspondientes, y opcionalmente elimina los originales.
    """
    print("Iniciando el proceso de conversión...")
    print(f"Directorio de origen: {SOURCE_DIR}")
    print(f"Directorio de destino: {DEST_DIR} (Calidad: {BITRATE})")
    print(f"Eliminar originales: {'Sí' if DELETE_PROCESSED else 'No'}")
    print("-" * 50)

    os.makedirs(DEST_DIR, exist_ok=True)
    supported_extensions = ('.mp3', '.flac', '.ogg', '.wma')

    for root, _, files in os.walk(SOURCE_DIR):
        for filename in files:
            if filename.lower().endswith(supported_extensions):
                filepath = os.path.join(root, filename)
                print(f"Procesando: {filename}")

                metadata = get_metadata(filepath)
                
                artist = metadata.get('artist')
                title = metadata.get('title')
                track = format_track_number(metadata.get('track'))

                if not artist or not title:
                    print(f"  Saltando '{filename}' por falta de metadatos (Artista o Título).")
                    print("-" * 50)
                    continue

                clean_artist = clean_filename(artist)
                clean_title = clean_filename(title)
                
                # Construir nuevo nombre de archivo con formato: <track>-<artist>-<title>
                if track:
                    new_filename = f"{track}{SEPARATOR}{clean_artist}{SEPARATOR}{clean_title}.{EXT}"
                else:
                    new_filename = f"{clean_artist}{SEPARATOR}{clean_title}.{EXT}"
                    
                new_full_path = os.path.join(DEST_DIR, new_filename)

                if os.path.exists(new_full_path):
                    print(f"  El archivo de destino ya existe: {new_filename}. Saltando.")
                    print("-" * 50)
                    continue

                print(f"  Convirtiendo '{filename}' a '{new_filename}'...")
                try:
                    audio_segment = AudioSegment.from_file(filepath)
                    audio_segment.export(new_full_path, format=EXT, bitrate=BITRATE)
                    
                    print("  Conversión exitosa. Actualizando metadatos...")

                    try:
                        audio_mp3 = ID3(new_full_path)
                    except ID3NoHeaderError:
                        audio_mp3 = ID3()

                    audio_mp3['TPE1'] = TPE1(encoding=3, text=[metadata['artist']])
                    audio_mp3['TIT2'] = TIT2(encoding=3, text=[metadata['title']])
                    if metadata['album']:
                        audio_mp3['TALB'] = TALB(encoding=3, text=[metadata['album']])
                    if metadata['genre']:
                        audio_mp3['TCON'] = TCON(encoding=3, text=[metadata['genre']])
                    if metadata['track']:
                        audio_mp3['TRCK'] = TRCK(encoding=3, text=[metadata['track']])

                    audio_mp3.save(new_full_path, v2_version=4)
                    print(f"  Metadatos actualizados en '{new_filename}'.")
                    
                    # Eliminar archivo original si la conversión fue exitosa
                    if DELETE_PROCESSED:
                        delete_processed_file(filepath)

                except Exception as e:
                    print(f"  ERROR durante la conversión de '{filename}': {e}")
                
                print("-" * 50)

    print("Proceso finalizado.")

if __name__ == "__main__":
    convert_and_rename_audio()