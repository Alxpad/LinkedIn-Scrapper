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
class Paginador:
    def PagEscaner(self,webDriver):
        pags = webDriver.find_elements(By.CLASS_NAME, 'artdeco-pagination__indicator--number')
        numPags = len(pags)
        return int(numPags)
    
    def PagNavegador(self,WebDriver,i):
        IdBtn = str(i+1)
        stringBtn = "[aria-label='Página {}']".format(IdBtn)
        BtnPag = WebDriver.find_element_by_css_selector(stringBtn)
        BtnPag.click()
        
          
