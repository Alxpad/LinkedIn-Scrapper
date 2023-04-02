from itertools import count
from numpy import empty
from Selenium4_chrome import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from DetectorAuth import *
import chime
import Oferta

driver = webdriver.Chrome()

def PagEscaner(webDriver, escaner):
    pags = webDriver.find_elements(By.CLASS_NAME, 'artdeco-pagination__indicator')
    if len(pags) > 1:
        print("Detectadas más de una página")
        PagNavigator(webDriver, len(pags), escaner)
    else:
        print("Todas las páginas detectadas se han revisado")

def PagNavigator(WebDriver,NumPags, escaner):
    for i in range(0,NumPags):
        WebDriver.find_elements(By.XPATH("//li[@data-test-pagination-page-btn='"+i+"']"))
        escaner.scan()

        # Función Capturar()