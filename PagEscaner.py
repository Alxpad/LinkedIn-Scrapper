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


class Paginador:        # This object is used to navigate through different result pages
    def PagEscaner(self,webDriver,escaner, limite):     
        if limite == -1:
            pages = webDriver.find_elements(By.CLASS_NAME, 'artdeco-pagination__indicator--number')
            lastPage = pages[-1]
            numPags = int(lastPage.text)

        else:
            numPags = limite     #  Pages limit. Received from search window (event with key '-LIMIT-')
        
        if numPags > 1:
            self.PagNavegador(webDriver,numPags,escaner)
        else:
            raise ValueError('ERROR: Limit of pages to scan was not defined: numPags < 1')
        
    def PagNavegador(self,WebDriver,i, escaner):    # Function that iterates through the pages, until the limit selected by the user is reached.
        for i in range (1,i):
            BtnPag = WebDriver.find_element(By.XPATH, f"//button[@aria-label='Página {i+1}']")
            BtnPag.click()
            time.sleep(1)
            escaner.scan(WebDriver)

            