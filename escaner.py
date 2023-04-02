from Selenium4_chrome import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from DetectorAuth import *
import chime
import Oferta
import time

class escaner:  # This class includes all the functions related to web scrapping
    def __init__(self):
        self.list_ofertas = list()
        self.Marker = []
        self.nresults = 0
        self.kw = ''
        self.loc=''
        self.webdriver = ''
          

    def Iniciar_Busqueda(self, driver, keywords, location):     # Search starts logging in linkedin account
        self.webdriver = driver
        self.kw = keywords
        self.loc = location
        actions = ActionChains(driver)
        time.sleep(1)
        search_bars= driver.find_elements(By.CLASS_NAME,'jobs-search-box__text-input')
        search_bars[0].clear()
        search_bars[0].send_keys(keywords)
        time.sleep(1)
        actions.send_keys(Keys.TAB)
        actions.perform()
        time.sleep(1)
        actions.send_keys(Keys.HOME)
        actions.perform()
        actions.send_keys(Keys.SHIFT, Keys.END)
        actions.perform()
        actions.send_keys(location)
        time.sleep(0.5)
        actions.send_keys(Keys.ARROW_DOWN)
        actions.perform()
        time.sleep(2)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(3)
        self.Listado(driver)

    def Check_Marker(self,Marker):      #   Checks if the page is the LinkedIn job offers feed or not
        if len(Marker)==0:
            return True

    def scan(self, results = None):     #   Scans linkedin.com/jobs
        WebDriver = self.webdriver
        list_empresas = list()
        list_enlaces = list()
        list_titles = list()
        #list_item = list()         # Variable for future features
        i = 0
        while i<8:
            WebDriver.execute_script("document.getElementsByClassName('jobs-search-results-list')[0].scrollBy(0,600);")
            i+=1

        repetition = 2      #   If 2 or more offers have the same title, it will be followed by this number in the results list
        time.sleep(0.3)
        num_cards = WebDriver.find_elements(By.CLASS_NAME,"job-card-list")
        Txt_titulo =  WebDriver.find_elements(By.CLASS_NAME,"job-card-list__title")
        Txt_empresa = list()

        for x in num_cards:             # This function saves the titles in a list
            Txt_empresa = x.text
            Txt_empresa_split = Txt_empresa.splitlines()
            empresa = Txt_empresa_split[1]

            if empresa == '':
                list_empresas.append('(Sin datos)')

            else:
                list_empresas.append(empresa)

        
        for h in Txt_titulo:             # This one gets the links in the titles
            link = h.get_attribute("href")
            if h.text not in list_titles:
                list_enlaces.append(link)
                list_titles.append(h.text)

            else:                       # Checks if the link is in the list already. If not, the link is added too.
                if link not in list_enlaces:
                    list_enlaces.append(link)
                    list_titles.append(h.text + " " + str(repetition))
                    repetition +=1
                
                else:
                    pass

        # Error check: Number of links, job offers and company names saved has to be the same. 
        if (len(list_empresas) != len(list_enlaces)):
            raise ValueError("ERROR: Number of links is different from number of company names: escaner.scan")
        
        elif (len(list_enlaces) != len(list_titles)):
            raise ValueError("ERROR: Number of links is different from number of job offers: escaner.scan")
        
        elif (len(list_empresas) != len(list_titles)):
            raise ValueError("ERROR: Number of company names is different from number of job offers: escaner.scan")
        self.nresults = len(list_enlaces)
        self.Fill_Dict(list_titles, list_enlaces, list_empresas)

    def contador(self):
        WebDriver = self.webdriver
        try:
            cuenta_resultados = WebDriver.find_element(By.XPATH, "//*[@id='main']/div/section[1]/header/div[1]/small").text
        except:
            time.sleep(1)
            self.Iniciar_Busqueda(WebDriver,self.kw, self.loc)
        self.scan()

    def Listado(self, WebDriver):  # Checks if current URL is the LinkedIn search page.
        self.contador()
        txt = WebDriver.current_url
        while not txt.startswith('https://www.linkedin.com/jobs/search/'):
            time.sleep(2)
            print("Loading...")
        
    def Fill_Dict(self, titulos, enlaces, empresas):    # Creates the dictionary to be sent to the results list
        for x in range(len(enlaces)):
            
            Ofer_obj = Oferta.ClaseOferta()
            Ofer_obj.titulo = titulos[x]
            Ofer_obj.empresa = empresas[x]
            Ofer_obj.href = enlaces[x]
            self.list_ofertas.append(Ofer_obj)
        print("Final fill_dict")

    def PrintEscaner(self):         # Optional function to print results in prompt.
        if len(self.list_ofertas) != 0:
            return self.list_ofertas
        
        else:
            return 0
        