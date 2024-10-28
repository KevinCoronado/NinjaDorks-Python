import json
from rich.console import Console
from rich.table import Table

class ResultsParser:
    def __init__(self, resultados):
        self.resultados = resultados
        
    def exportar_html(self, archivo_salida):
        """Exporta los resultados a un archivo HTML basándose en una plantilla.

        Args:
            archivo_salida (str): El nombre del archivo de salida donde se guardará el HTML.
        """
        # Lectura de la plantilla de informe HTML.
        with open("html_template.html", 'r', encoding='utf-8') as f:
            plantilla = f.read()

        # Creación de los elementos HTML para cada resultado.
        elementos_html = ''
        for indice, resultado in enumerate(self.resultados, start=1):
            elemento = f'<div class="resultado">' \
                       f'<div class="indice">Resultado {indice}</div>' \
                       f'<h5>{resultado["title"]}</h5>' \
                       f'<p>{resultado["description"]}</p>' \
                       f'<a href="{resultado["link"]}" target="_blank">{resultado["link"]}</a>' \
                       f'</div>'
            elementos_html += elemento
        
        # Integración de los elementos en la plantilla y escritura al archivo de salida.
        informe_html = plantilla.replace('{{ resultados }}', elementos_html)
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            f.write(informe_html)
        print(f"Resultados exportados a HTML. Fichero creado: {archivo_salida}")        
        
    def exportar_json(self,archivo_salida):
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                json.dump(self.resultados, f, ensure_ascii=False, indent=4)  
            print("Resultados exportados a HTML. Fichero creado: {archivo_salida}") 
    
    def mostrar_pantalla(self):
        consola = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim")
        table.add_column("Titulo", width=50)
        table.add_column("Descripcion")
        table.add_column("Enlace")
        
        for indice, resultado in enumerate(self.resultados, start=1):
            table.add_row(str(indice), resultado['title'], resultado['description'], resultado['link'])
            table.add_row("","","","")
        consola.print(table)
        