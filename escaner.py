from typing import List
from numpy import empty
from Selenium4_chrome import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from DetectorAuth import *
import chime
import Oferta
import time

class escaner:
    def __init__(self,WebDriver):
        self.list_item = list()
        self.dicc_ofertas = dict()
        self.driver = WebDriver
        self.actions = ActionChains(driver)

    def Iniciar_Busqueda(self, WebDriver, keywords):
        
        search_bars= WebDriver.find_elements(By.CLASS_NAME,'jobs-search-box__text-input')
        search_bars[0].send_keys(keywords)
        time.sleep(1)
        self.actions.send_keys(Keys.TAB)
        self.actions.perform()
        time.sleep(1)
        self.actions.send_keys("Málaga")
        self.actions.perform()
        time.sleep(0.5)
        self.actions.send_keys(Keys.ENTER)
        self.actions.perform()
        time.sleep(3)
        self.Listado(WebDriver)
    
    def Listado(self, WebDriver):
        self.list_item = WebDriver.find_elements(By.CLASS_NAME,"occludable-update")
        time.sleep(2)
        for x in range(0,len(self.list_item)):
            TxtLong = self.list_item[x].text
            TxtSplit = TxtLong.split('\n')
            if TxtSplit[0] != '':
                Ofer_obj = Oferta.ClaseOferta()
                Ofer_obj.titulo = TxtSplit[0]
                Ofer_obj.empresa = TxtSplit[1]
                self.dicc_ofertas[x] = Ofer_obj

        for i in range(len(self.dicc_ofertas)):
            self.dicc_ofertas[i].mostrar(i)
        #TODO: Pasar diccionario de ofertas en variable externa
        #TODO: Evitar capturar mensajes de la web