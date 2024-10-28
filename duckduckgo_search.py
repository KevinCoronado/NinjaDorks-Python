from serpapi import GoogleSearch



class DuckDuckGoSearch:
    def __init__(self,api_key_duck):
        self.api_key_duck = api_key_duck

    def search(self,query):
        #Parametros que usaremos
        params = {
        "engine":"duckduckgo",
        "q":query,
        "kl": "us-en",
        "api_key":self.api_key_duck
        }
        search = GoogleSearch(params) 
        results = search.get_dict()
        organic_results = results["organic_results"]
        self.custom_results(organic_results)
        return organic_results
        
    def custom_results(self,organic_results):
        #Creamos un for donde enumeramos los resultados de organic results y empezamos en el primero
        for index, result in enumerate(organic_results, start=1):
            #Treamos los datos que queremos y agregamos un valor predeterminado en caso de no haber un dato
            title = result.get("title", "Sin título")
            link = result.get("link", "Sin enlace")
            snippet = result.get("snippet", "Sin descripción")
            #Imprimimos los datos
            print(f"Resultado ---------{index}:--------")
            print(f"  Título: {title}")
            print(f"  Enlace: {link}")
            print(f"  Descripción: {snippet}\n")









    