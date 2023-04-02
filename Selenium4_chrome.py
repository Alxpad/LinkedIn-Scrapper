import time
from selenium import webdriver

def selenium_launch():      #   Function used to launch selenium driver. 
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(
        options=options
    )
    return driver
        
