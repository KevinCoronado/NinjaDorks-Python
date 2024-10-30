from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as GoogleService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time


class BrowserAutoSearch:
    def __init__(self):
        self.browser = self._initialize_browser()
        
    def _initialize_browser(self):
        browsers = {
            "firefox": {
                "manager":GeckoDriverManager,
                "service": FirefoxService,
                "options": webdriver.FirefoxOptions(),
                "driver": webdriver.Firefox
            },
            "chrome": {
                "manager":ChromeDriverManager,
                "service":GoogleService,
                "options": webdriver.ChromeOptions(),
                "driver": webdriver.Chrome
            }
        }
        
        #Inicializamos los navegadores
        
        for browser_name, browser_info in browsers.items():
            try:
                return browser_info["driver"](service=browser_info["service"](browser_info["manager"]().install()), options=browser_info["options"])
            except Exception as e:
                print(f"Error al inicializar el navegador {browser_name} : {e}")
        raise Exception("No se pudo iniciar ningun navegador, porfavor instala Firefox o Chrome")
    
    def accept_cookies(self,button_selector):
        """Acepta el anuncion de cookies de un buscador"""
        try:
            accept_button = WebDriverWait(self.browser,10).until(
            EC.element_to_be_clickable((By.ID,button_selector))
            )
            accept_button.click()
        except Exception as e:
            print(f"Error al encontrar el boton de aceptar cookies: {e}")
            
    def search_google(self, query):
        """Realiza una busqueda en google"""
        self.browser.get("http://www.google.com")
        self.accept_cookies(button_selector='L2AGLb')
            
        #Encuentra el cuadro de busqueda
        search_box = self.browser.find_element(By.NAME, 'q')
        search_box.send_keys(query + Keys.ENTER)

        time.sleep(5)

    def google_search_results(self):
        """Extrae lso resultados de google"""
        #Extraemos los enlaces y descripciones de los primeros resultados
        results = self.browser.find_elements(By.CSS_SELECTOR, 'div.g')
        custom_results = []
        for result in results:
            try:
                cresult = {}
                cresult["title"] = result.find_element(By.CSS_SELECTOR, 'h3')
                cresult["link"] = result.find_element(By.TAG_NAME, 'a').get_attribute('href')
                cresult["description"] = result.find_element(By.CSS_SELECTOR, 'div.VwiC3b').text
                custom_results.append(cresult)
            except Exception as e:
                print(f"Un elemento no pudo ser extraido: {e}")
                continue
        return custom_results
        #Cerramos el navegador
    
    
    def quit(self):
        self.browser.quit()




    