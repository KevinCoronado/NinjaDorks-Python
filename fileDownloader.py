import os
import requests
import re

class FileDownloader:
    def __init__(self, directorio_destino):
        self.directorio = directorio_destino
        self.crear_directorio()
        
    def crear_directorio(self):
        if not os.path.exists(self.directorio):
            os.makedirs(self.directorio)
    
    def limpiar_nombre_archivo(self, nombre_archivo):
        # Elimina caracteres no permitidos en nombres de archivos
        nombre_limpio = re.sub(r'[<>:"/\\|?*]', '_', nombre_archivo)
        return nombre_limpio

    def descargar_archivo(self, url):
        nombre_archivo = url.split("/")[-1].split("?")[0]  # Evita los parámetros de la URL
        nombre_archivo = self.limpiar_nombre_archivo(nombre_archivo)
        
        try:
            respuesta = requests.get(url)
            respuesta.raise_for_status()  # Verifica si la solicitud fue exitosa
            ruta_completa = os.path.join(self.directorio, nombre_archivo)
            
            with open(ruta_completa, 'wb') as archivo:
                archivo.write(respuesta.content)
            print(f"Archivo {nombre_archivo} descargado en {ruta_completa}.")
        except requests.exceptions.RequestException as e:
            print(f"Error al descargar {url}: {e}")

    def filtrar_descargas_archivos(self, urls, tipos_archivos=["all"]):
        if tipos_archivos == ["all"]:
            for url in urls:
                self.descargar_archivo(url)
        else:
            for url in urls:
                if any(url.endswith(f".{tipo}") for tipo in tipos_archivos):
                    self.descargar_archivo(url)
