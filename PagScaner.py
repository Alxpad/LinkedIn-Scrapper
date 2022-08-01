from itertools import count
from numpy import empty
from Selenium4_chrome import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from DetectorAuth import *
import chime
import Oferta
import chime

driver = webdriver.Chrome()

def PagEscaner(webDriver):
    pags = webDriver.find_element(By.CLASS_NAME, 'artdeco-pagination__indicator')
    return len(pags)

def PagNavigator(WebDriver,NumPags ):
    for i in range(0,PagEscaner(WebDriver)):
        #TODO: por cada página, repetir la captura
        WebDriver.click()
        # Función Capturar()

