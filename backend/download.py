import sys
import subprocess
import os
import json
from pathlib import Path
import time
from urllib.parse import urlparse, parse_qs, urlencode

# Directorio para caché
CACHE_DIR = Path.home() / '.yt_downloader_cache'
COOKIES_CACHE = CACHE_DIR / 'cookies.json'

def ensure_cache_dir():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

def cache_cookies():
    """Extrae y cachea las cookies de Firefox"""
    if COOKIES_CACHE.exists() and time.time() - COOKIES_CACHE.stat().st_mtime < 3600:  # 1 hora de caché
        return str(COOKIES_CACHE)
    
    ensure_cache_dir()
    temp_cookie_file = CACHE_DIR / 'temp_cookies.txt'
    
    subprocess.run([
        'yt-dlp',
        '--cookies-from-browser', 'firefox',
        '--cookies', str(temp_cookie_file),
        'https://www.youtube.com'
    ], capture_output=True)
    
    if temp_cookie_file.exists():
        temp_cookie_file.rename(COOKIES_CACHE)
        return str(COOKIES_CACHE)
    return None

def list_formats(url):
    print("Obteniendo formatos disponibles...")
    command = [
        'yt-dlp',
        '-F',
        '--cookies-from-browser', 'firefox',
        '--no-check-certificates',
        '--no-warnings',
        '--ignore-config',
        url
    ]
    subprocess.run(command)

def clean_youtube_url(url: str) -> str:
    """
    Limpia una URL de YouTube para mantener solo el ID del video.
    Remueve parámetros como 'list' e 'index' usados en playlists.
    """
    try:
        # Parsear la URL
        parsed_url = urlparse(url)
        # Obtener los parámetros
        params = parse_qs(parsed_url.query)
        
        # Verificar si existe el parámetro 'v' (ID del video)
        if 'v' not in params:
            return url  # Si no hay ID de video, retornar la URL original
            
        # Reconstruir la URL solo con el parámetro 'v'
        clean_params = {'v': params['v'][0]}
        clean_query = urlencode(clean_params)
        
        # Reconstruir la URL limpia
        clean_url = f"https://www.youtube.com/watch?{clean_query}"
        print(f"URL original: {url}")
        print(f"URL limpia: {clean_url}")
        return clean_url
        
    except Exception as e:
        print(f"Error limpiando URL: {e}")
        return url  # En caso de error, retornar la URL original

def download_video(url, progress_hooks=None):
    print("\nIniciando descarga...")
    start_time = time.time()
    
    # Limpiar la URL antes de procesar
    url = clean_youtube_url(url)
    
    # Configura y limpia el directorio temporal
    temp_dir = Path("temp_downloads")
    temp_dir.mkdir(exist_ok=True)
    
    # Limpiar archivos antiguos
    for old_file in temp_dir.glob('*.mp4'):
        try:
            old_file.unlink()
        except Exception as e:
            print(f"Error limpiando archivo antiguo: {e}")
    
    command = [
        'yt-dlp',
        '--cookies-from-browser', 'firefox',
        '--no-check-certificates',
        '--no-warnings',
        '--ignore-config',
        '--force-ipv4',
        '--buffer-size', '16K',
        '-f', 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        '--merge-output-format', 'mp4',
        '-o', str(temp_dir / '%(title)s.%(ext)s'),
        '--progress',
        url
    ]
    
    try:
        result = subprocess.run(command, check=True)
        
        # Encuentra el archivo descargado
        files = list(temp_dir.glob('*.mp4'))
        if not files:
            raise Exception("No se encontró el archivo descargado")
        
        file_path = files[0]
        original_filename = file_path.name  # Guardamos el nombre original
        
        # Verificar que el archivo existe y tiene tamaño
        if not file_path.exists() or not file_path.stat().st_size:
            raise Exception("Error: archivo descargado inválido")
        
        end_time = time.time()
        duration = end_time - start_time
        print(f"\nTiempo total de descarga: {duration:.2f} segundos ({duration/60:.2f} minutos)")
        
        return str(file_path), original_filename  # Retornamos ambos
        
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error en la descarga: {e}")
    except Exception as e:
        raise Exception(f"Error inesperado: {e}")

def main():
    total_start_time = time.time()
    
    if len(sys.argv) < 2:
        print("Por favor proporciona la URL del video")
        sys.exit(1)
        
    url = sys.argv[1]
    
    # Ya no necesitamos mostrar formatos ni pedir input
    print("\nDescargando mejor calidad disponible...")
    download_video(url)
    
    total_end_time = time.time()
    total_duration = total_end_time - total_start_time
    print(f"\nTiempo total del proceso: {total_duration:.2f} segundos ({total_duration/60:.2f} minutos)")

if __name__ == "__main__":
    main() 