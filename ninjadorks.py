#Cargar las variables del entorno
from dotenv import load_dotenv, set_key
import os
import sys
#clases
from ai_agent import OpenAIGenerator, GPT4AllGenerator, IAAgent
from browserautosearch import BrowserAutoSearch
from google_search import GoogleSearch
from duckduckgo_search import DuckDuckGoSearch
from results_parser import ResultsParser
from fileDownloader import FileDownloader
from smartsearch import SmartSearch
import argparse

#El codigo funciona con chrome principalmente, duckduckgo solo funciona los resultados en consola

def env_config():
    """
    Configurar el archivo .env con los valores proporcionados.
    """
    api_key = input("Introduce tu API KEY de Google: ")
    engine_id = input("Introduce el ID del buscador personalizado de Google")
    set_key(".env","API_KEY_GOOGLE", api_key)
    set_key(".env","SEARCH_ENGINE_ID", engine_id)
    #set_key(".env","API_KEY_DUCKDUCKGO", Duck_id)
 
 
def openai_config():
    """Configura la API KEY de OpenAI"""   
    api_key = input("Intorduce la API KEY de OpenAI")
    set_key(".env","OPENAI_API_KEY",api_key)
    
def load_env(configure_env):
    #Comprobamos si existe el ficher .env
    env_exists = os.path.exists(".env")
    
    if not env_exists or configure_env:
        env_config()
        print("Archivo .env configurado satisfactoriamente.")
        sys.exit(1)
    
    #Cargamos las variables en el entorno
    load_dotenv()

    #----------Google---------------------
    #Leemos la clave API (max. 100 peticiones/dia)
    API_KEY_GOOGLE = os.getenv("API_KEY_GOOGLE")

    #Leemos el id del buscador
    SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")


    #---------Duck Duck Go--------------
    #Leemos la clave API de Duck Duck Go
    #API_KEY_DUCKDUCKGO = os.getenv("API_KEY_DUCKDUCKGO")
   
        
    if not API_KEY_GOOGLE or not SEARCH_ENGINE_ID:
        print("ERROR: Falta la API_KEY o el SEARCH_ENGINE_ID. Por favor, ejecuta la opción --configure para configurar el archivo .env.")
        sys.exit(1) 

    return(API_KEY_GOOGLE, SEARCH_ENGINE_ID)
        


def main(query,configure_env, start_page, pages, lang, output_json, output_html, download, gen_dork,dir_path, regex, prompt, model, max_tokens,selenium):
    
       

    #Si hay directorio señalado es porque va a usar la IA para buscar en el fichero
    if dir_path:
        searcher = SmartSearch(dir_path)
        if regex:
            resultados = searcher.regex_search(regex)   
            print()
            for file, results in resultados.items():
                print(file)
                for r in results:
                    print(f"\t- {r}")

        if args.prompt:
            resultados = searcher.ia_search(prompt, model, max_tokens)
            print()
            if resultados:
                for file, results in resultados.items():
                    print(file)
                    for r in results:
                        print(f"\t- {r}")
            else:
                print("No se ha realizado ningun movimiento y por lo tanto no ha habido cobro")
        print("Falto seleccionar el prompt o regex")
        sys.exit(1)
    
    
    
    if gen_dork:
        #Preguntamos si el usuario quiere utilizar un modelo local o OPENAI
        respuesta=""
        while respuesta.lower() not in ("y","yes","no","n"):
            respuesta = input("Quieres utilizar GPT-4 de OpenAI (y/n): ")
        
        if respuesta.lower() in ("y","yes"):
            #Comprobamos si esta definida la API KEY de OpenAI en el fichero .env
            load_dotenv()
            if not "OPENAI_API_KEY" in os.environ:
                openai_config()
                load_dotenv()
            #Generacion del dork
            openai_generator =OpenAIGenerator()
            ia_agent = IAAgent(openai_generator)
        else:
            print("Utilizando gpt4all y ejecutando la generacion en local. Puede tardar varios minutos...")
            gpt4all_generator = GPT4AllGenerator()
            ia_agent = IAAgent(gpt4all_generator)
        
        respuesta = ia_agent.generate_gdork(gen_dork)
        print(f"\nResultado:\n{respuesta}")
        sys.exit(1)
        
        
                
            

    
    
    #---------Busquedas------------------
    if not query:
        print("Indica una consulta con el comando -q. Utiliza el comando -h para mostrar la ayuda")
        sys.exit(1)    
        
        #Mostrar los resultados en linea por consola
        rparser.mostrar_pantalla()
    elif selenium:
        browser = BrowserAutoSearch()
        browser.search_google(query=query)
        googleResultados = browser.google_search_results()
        browser.quit()
    else: 
        API_KEY_GOOGLE, SEARCH_ENGINE_ID = load_env(configure_env=configure_env)
        gsearch = GoogleSearch(API_KEY_GOOGLE,SEARCH_ENGINE_ID)
        googleResultados = gsearch.search(query,start_page=start_page,pages=pages,lang=lang)

        #duckSearch = DuckDuckGoSearch(API_KEY_DUCKDUCKGO)
        #duckResultados = duckSearch.search(query)
        
        rparser = ResultsParser(googleResultados)
        #rparser = ResultsParser(duckResultados)
        rparser.mostrar_pantalla()
        
        
    if output_html:
        rparser.exportar_html(output_html)
    if output_json:
        rparser.exportar_json(output_json)
    if download:
        #Separar las extenciones de los archivos en una lista
        file_types = download.split(",")
        #Nos quedamos solamente con las urls de los resultados obtenidos
        urls = [resultado['link'] for resultado in googleResultados]
        fdownloader = FileDownloader("Descargas")
        fdownloader.filtrar_descargas_archivos(urls, file_types)
        
   
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Herramienta para realizar búsquedas avanzadas en Google de forma automática.")
    parser.add_argument("-q", "--query", type=str, help="Especifica el dork que deseas buscar. Ejemplo: -q \"filetype:sql 'MySQL dump' (pass|password|passwd|pwd)\"")
    parser.add_argument("-c", "--configure", action="store_true", help="Configura o actualiza el archivo .env. Utiliza esta opción sin otros argumentos para configurar las claves.")
    parser.add_argument("--start-page", type=int, default=1, help="Página de inicio para los resultados de búsqueda. Por defecto es 1.")
    parser.add_argument("--pages", type=int, default=1, help="Número de páginas de resultados a retornar. Por defecto es 1.")
    parser.add_argument("--lang", type=str, default="lang_es", help="Código de idioma para los resultados de búsqueda. Por defecto es 'lang_es' (español).")
    parser.add_argument("--json", type=str, help="Exporta los resultados en formato JSON en el fichero especificado.")
    parser.add_argument("--html", type=str, help="Exporta los resultados en formato HTML en el fichero especificado.")
    parser.add_argument("--download", type=str,help="Especifica las extenciones de los archios que quieres descargar separadas entre coma. Ej: --download 'pdf,doc,sql")
    parser.add_argument("-gd","--generate-dork",type=str,help="Genera un dork a partir de una descripcion proporcionada por el usuario. \nEj: -gd 'Listado de usuarios y passwords en ficheros de textp'")
    #SmartSearch
    parser.add_argument("--dir_path", type=str, help="Ruta al directorio de archivos para buscar.")
    parser.add_argument("-r", "--regex", type=str, help="Expresión regular para búsqueda en archivos.")
    parser.add_argument("-p", "--prompt", type=str, help="Prompt para búsqueda con IA en archivos.")
    parser.add_argument("-m", "--model", type=str, default="gpt-3.5-turbo-0125", help="Modelo de OpenAI.")
    parser.add_argument("--max_tokens", type=int, default=100, help="Número máximo de tokens.")
    parser.add_argument("--selenium",action="store_true",default=False,help="Utiliza Selenium para realizar la busqueda de un navegador de manera automatica")
    args = parser.parse_args()

    main(query=args.query, 
         configure_env=args.configure, 
         start_page=args.start_page, 
         pages=args.pages, 
         lang=args.lang,
         output_html=args.html,
         output_json=args.json,
         download=args.download,
         gen_dork=args.generate_dork,
         dir_path=args.dir_path,
         regex=args.regex,
         prompt=args.prompt,
         model=args.model,
         max_tokens=args.max_tokens,
         selenium=args.selenium)
