from Selenium4_chrome import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from DetectorAuth import *
import chime
import Oferta
import escaner
import PagEscaner

keywords = "Electricista"
#location = "Málaga, España"
email="****"
password = "****"

try:
    driver.get('https://www.linkedin.com/login')
except:
    chime.error()
    print("No se pudo abrir la URL")

time.sleep(3)
driver.find_element(By.ID,'username').send_keys(email)
driver.find_element(By.ID,'password').send_keys(password)
driver.find_element(By.ID,'password').send_keys(Keys.ENTER)

driver.get("https://linkedin.com/jobs")
time.sleep(3)
AuthPage(driver)
paginador = PagEscaner.Paginador()
escaner = escaner.escaner(driver)

escaner.Iniciar_Busqueda(driver,keywords)
count = paginador.PagEscaner(driver)

for t in range(1,count):
    paginador.PagNavegador(driver,t)
    escaner.Listado(driver)
    time.sleep(2)
