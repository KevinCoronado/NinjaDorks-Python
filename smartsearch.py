import os
import re
from transformers import GPT2Tokenizer
from openai import OpenAI


class SmartSearch:
    def __init__(self,dir_path):
        self.dir_path = dir_path
        self.files = self._read_files()
        
    def _read_files(self):
        """Lee el contenido de los ficheros que se encuentran en un directorio"""
        files = {}
        #Listar los ficheros del directorio
        for archivo in os.listdir(self.dir_path):
            file_path = os.path.join(self.dir_path, archivo)
            try:
                with open(file_path,'r', encoding='utf8') as f:
                    files[archivo] = f.read()
            except Exception as e:
                print(f"Error al leer el archivo {file_path} : {e}")
        return files
    
    def  regex_search(self,regex):
        """Busca informacion utilizando expresiones regulares."""
        coincidencias = {}
        #Recorremos el recorrido de todos los ficheros del directorio
        for file, text in self.files.items():
            respuesta = ""
            while respuesta not in ("y","n","yes","no"):
                respuesta = input(f"El fichero {file} tiene una longitud de {len(text)} caracteres, quieres procesarlo? (y/n)")
            if respuesta in ("n","no"):
                continue
            matches = re.findall(regex,text, re.IGNORECASE)
            if not matches == []:
                coincidencias[file] = matches
        return coincidencias 
    
    def ia_search(self,prompt,model_name="gpt-3.5-turbo-0125", max_tokens=100):
        """Realiza busquedas en ficheros con Inteligencia Artificial."""
        coincidencias = {}
        for file, text in self.files.items():
            respuesta=""
            tokens, coste = self._calcular_coste(text,prompt,model_name,max_tokens)
            while respuesta not in ("y","n","yes","no"):
                respuesta = input(f"El fichero {file} tiene una longitud de {tokens} tokens (aprox. {coste}$). Quieres continuar? (y/n)")
            if respuesta in ("n","no"):
                continue
            #Dividimos el fichero en segmentos 
            file_segments = self._split_file(text,model_name)
            
            
            #Inicializamos el cliente de OpenAI
            client = OpenAI()
            
            resultados_segmentos = []
            
            for index, segment in enumerate(file_segments):
                print(f"Procesando el segmento {index + 1}/{len(file_segments)}...")
                chat_completion = client.chat.completions.create(
                    messages = [
                        {
                            "role":"user",
                            "content":f"{prompt}\n\nTexto:\n{segment}",
                        }
                    ],
                    model = model_name,
                    max_tokens=max_tokens,
                    n=1, 
                )    
                
                resultados_segmentos.append(chat_completion.choices[0].message.content)    
            coincidencias[file] = resultados_segmentos    
            return coincidencias
    
    def _split_file(self,file_text,model_name):
        """Divide el contenido del fichero en segmentos."""
        context_window_sizes = {
            "gpt-4-0125-preview": 128000,
            "gpt-4-1106-preview": 128000,
            "gpt-4": 16000,
            "gpt-4-32k": 32000,
            "gpt-3.5-turbo-0125": 16000,
            "gpt-3.5-turbo-instruct": 4000
        }
        return[file_text[i:i+context_window_sizes[model_name]]
               for i in range(0,len(file_text), context_window_sizes[model_name])]
        
    
        
    def _calcular_coste(self, text,prompt, model_name,max_tokens):
        """Calcula el coste para un modelo de OpenAI"""
        precios = {
            "gpt-4-0125-preview": {"input_cost": 0.01, "output_cost": 0.03},
            "gpt-4-1106-preview": {"input_cost": 0.01, "output_cost": 0.03},
            "gpt-4-1106-vision-preview": {"input_cost": 0.01, "output_cost": 0.03},
            "gpt-4": {"input_cost": 0.03, "output_cost": 0.06},
            "gpt-4-32k": {"input_cost": 0.06, "output_cost": 0.12},
            "gpt-3.5-turbo-0125": {"input_cost": 0.0005, "output_cost": 0.0015},
            "gpt-3.5-turbo-instruct": {"input_cost": 0.0015, "output_cost": 0.002}
        }   
        #Tokenizamos el texto perteneciente a larchivo
        tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        len_tokens_prompt= len(tokenizer.tokenize(prompt))
        len_tokens_text = len(tokenizer.tokenize(text)) 
        #Calculamos el coste de la prediccion
        input_cost = ((len_tokens_prompt + len_tokens_text) / 1000) * precios[model_name]["input_cost"]
        output_cost = (max_tokens / 1000) * precios[model_name]["output_cost"]
        return(len_tokens_text + len_tokens_prompt, input_cost + output_cost)
        

    

    
    