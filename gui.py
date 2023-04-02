import threading
import PySimpleGUI as sg      
from Selenium4_chrome import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from DetectorAuth import *
import PagEscaner
import escaner

#This file includes everything related to UI in the program


class guiwindow_login:      # First window with login data form
    def __init__(self):
        # This variables contain data neccesary to log in into linkedin. They are not saved elsewhere. You can omit this step and login directly from the web.
        # In that case, the scrapper will wait for you.

        self.email = ''
        self.passw = ''
        self.logdata = False

    def load(self, searchInstance, ScanInstance, pagInstance):
        sg.theme('DarkAmber')
        layout = [[sg.Text('Introduzca datos de login u omita éste paso')],
                [sg.VPush()],      
                [sg.Text('Email de login'), sg.Input(key='-MAIL-')],
                [sg.Text('Password de login'), sg.Input(key='-PAS-', password_char="*")],      
                [sg.Button('Listo'), sg.Exit(), sg.Push(), sg.Button('Omitir éste paso',key='-OMITIR-',button_color= 'orange')]]
        
        logwindow = sg.Window('Buscador de ofertas en LinkedIn', layout,auto_size_text=True, element_justification='left')      

        while True:                             # Login window events loop
            event, values = logwindow.read()
            
            if event == sg.WIN_CLOSED or event == 'Exit':
                break

            elif event == 'Listo':              # If user clicks on "Listo" (Ready in spanish)
                if values['-MAIL-'] and values['-PAS-'] :
                    self.email = values['-MAIL-']
                    self.passw = values['-PAS-']
                    self.logdata = True
                    searchInstance.load(False,pagInstance,ScanInstance,self.logdata, self.email, self.passw)
                else:
                    sg.popup('Por favor, introduzca algún dato')    #"Please, introduce any data" popup. Shows up if fields are empty


            elif event == '-OMITIR-':
                # If you click on "Omitir" (skip in spanish) button, the scrapper will request you to log in through LinkedIn web. It will continue automatically once you do.
               logwindow.close()
               searchInstance.load(True,pagInstance,ScanInstance,self.logdata, self.email, self.passw)

class guiwindow_search:     # Window that shows up once you have introduced your data, or omitted it.
    def __init__(self):
        self.kwords = ''
        self.locat=''
        self.logdata = ''
        self.mail = ''
        self.passw = ''
        self.ScanPage = ''
        self.PagInstance = ''
        self.searchwindow = ''
        self.resultList_c = []
        self.driver = ''
        self.selectedLink = ''
        self.omitir = False
        self.searchLimit = 5

    def load(self,omitir,paginatorInstance,ScanPage,logdata, email=None, passw=None):
        self.omitir = omitir
        self.ScanInstance = ScanPage
        self.PagInstance = paginatorInstance
        sg.theme('DarkAmber')   
        col = [
            [sg.Text('Introduzca datos de búsqueda')],
            [sg.Push()],
            [sg.Push()],
            [sg.Text('Palabras de búsqueda'), sg.Input(key='-KW-')], 
            [sg.Text('Localización'), sg.Input(key='-LOC-')],
            [sg.Text('Límite de páginas a indexar'), sg.Combo(enable_events=True,values=[2,3,4,5,10,15,20,25,30,35,40,"todas"], default_value=3, key='-LIMIT-')],
            [sg.Button('Buscar'), sg.Exit('Salir')],
            ]
        
        layout = [sg.vtop(sg.Column(col)), sg.Listbox(key="-RESULT-",enable_events=True,values=['Inicie la búsqueda'],size= (50,7))],[sg.VPush(),[sg.Push(),sg.Text("",key="-NRESULTADOS-")],[sg.Text("", justification='center',key = "-EMPLEADOR-"),sg.Push(),sg.Button('Ir al enlace', visible=False, key='-BTN_VISIT-')]]

        self.searchwindow = sg.Window('Buscador de ofertas en LinkedIn', layout, resizable=True, auto_size_text=True)

        while True:                             # Events loop for search window
            event, values = self.searchwindow.read()

            if event == sg.WIN_CLOSED or event == 'Salir':  # Loop for exit button
                break
            
            elif event == '-LIMIT-':        # Limit of pages scanned
                limit = values['-LIMIT-']
                if limit == "todas":         # "Todas" stands for "all pages"
                    self.searchLimit = -1

                else:
                    self.searchLimit = limit

            elif event == 'Buscar':         # If user clicks on "Buscar" (Search in spanish) button"
                if not self.omitir:
                    if values['-KW-'] and values['-LOC-']:
                        self.kwords = values['-KW-']
                        self.locat = values['-LOC-']
                        self.search(self.omitir,email, passw)

                    else:
                        sg.popup('Por favor, introduzca todos los datos')

                else:
                    self.kwords = values['-KW-']
                    self.locat = values['-LOC-']
                    self.search(self.omitir)

            elif event == '-RESULT-':                           # Event when user clicks on result list
                value = self.searchwindow['-RESULT-'].get()     # First it gets the data referred to the offer selected on the list
                for oferta in self.resultList_c:                # Looks for the offer in the dictionary of results obtained after the scanning (function show_search)
                    if oferta["titulo"] == value[0]:        
                        self.searchwindow["-EMPLEADOR-"].update(oferta["empresa"])
                        self.searchwindow["-BTN_VISIT-"].update(visible=True)
                        self.selectedLink = oferta["link"]
                        
                # The text area is updated with the company name, below the results list.
                # The button with the key "BTN_VISIT" leads the user to the selected offer, so that he can check it in more detail
            
            elif (event == '-BTN_VISIT-'):
               self.NewTab(self.selectedLink)
               

    def NewTab(self,link):                               # Function used to open a new tab with the visited offer
       self.driver.execute_script("window.open('');")

       # Obtains identifier of the new tab
       nueva_pestana = self.driver.window_handles[-1]

       # Change the focus of the controller to the new tab
       self.driver.switch_to.window(nueva_pestana)

       # Load a URL in the new tab
       self.driver.get(link)
        

    def showSearch(self):                   # Function that loads the result list from escaner object
        ResultList = self.ScanInstance.PrintEscaner()
        TitleList = []
        if ResultList == 0:
            self.searchwindow['-RESULT-'].update(values='No se han encontrado resultados.')

        else:               # The search results are saved in a list. This function extracts the offer data to a dictionary.
            id = 0
            for x in ResultList:
                dicc_oferta = {
                    "id_list":id,
                    "titulo": x.titulo,
                    "empresa":x.empresa,
                    "link": x.href
                }
                id +=1
                
                self.resultList_c.append(dicc_oferta)

        for j in self.resultList_c:
            TitleList.append(j['titulo'])

        self.searchwindow['-RESULT-'].update(values=TitleList)
        self.searchwindow['-NRESULTADOS-'].update(str(len(ResultList)) + " resultados.")
            

    def search(self, omitir, mail=None, passw=None):    # This function check if the user has omitted his login data. It will send the data to login page, or wait until the users logs himself manually.
        try:
            self.driver = selenium_launch()
            self.driver.get('https://linkedin.com/login')
            time.sleep
        except:
            raise ValueError("No se pudo abrir la URL de login")
            time.sleep(1)
            exit()

        time.sleep(2)
        if omitir == False:         # User entered login data
            self.driver.find_element(By.ID,'username').send_keys(mail)
            self.driver.find_element(By.ID,'password').send_keys(passw)
            self.driver.find_element(By.ID,'password').send_keys(Keys.ENTER)
            AuthPage(self.driver)

        else:                       # User omitted his data.
            layout = [[sg.Text('El programa está a la espera de que realice el login manualmente.')],
            [sg.Text('Esta ventana se cerrará automáticamente cuando se complete el login.')]]

            window = sg.Window('Login manual', layout, finalize=True)
            window.bring_to_front()

            while True:
                if AuthPage_omitir(self.driver):
                    window.close()
                    break

                else:
                    time.sleep(2)
        
        SearchKwords = self.kwords # Everything it's OK. This is the OK bell. Program go on.    
        LocKwords = self.locat
        self.ScanInstance.Iniciar_Busqueda(self.driver,SearchKwords,LocKwords)  # The search starts here
        self.PagInstance.PagEscaner(self.driver, self.ScanInstance,self.searchLimit)    # Instance of the object which scans the web.
        self.showSearch()
    
