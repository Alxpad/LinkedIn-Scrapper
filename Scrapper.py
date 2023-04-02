from Selenium4_chrome import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from DetectorAuth import *
import Oferta
import escaner
import PagEscaner
import gui

#-------------------------
#   Alejandro Padilla
#    March, 2023
#   LinkedIn TurboScrapper V1.0
#------------------------------------
# Program designed to search for job offers in LinkedIn easily.
# The user will be able to visit the selected offer with ease.
# ONLY COMPATIBLE WITH CHROME BROWSER (Version 111)
#
#
# ---------IMPORTANT NOTE ---------------------------------
# THE USER NEEDS TO HAVE A WORKING LINKEDIN USER ACCOUNT
# THIS PROGRAM DOES NOT COLLECT ANY INFORMATION ABOUT THE USER OR HIS PROFILE
# (Which might, in fact, be a crime... I'm not comfortable with that...).
#
# YOU CAN CHOOSE TO OMIT THE LOGIN FORM AND LOG MANUALLY INTO YOUR ACCOUNT
#
#--------- NEXT RELEASES--------------------------
#---- Detailed Information gathering about offers
#---- Capacity of saving searches and information in CSV format
#---- Compatible with browsers other than Chrome
#---- Focused on data collection and analysis through ML techniques

#------------------------ Program starts here --------
guilog = gui.guiwindow_login()
guisearch = gui.guiwindow_search()
pagescan = escaner.escaner()
paginator = PagEscaner.Paginador()

guilog.load(guisearch,pagescan,paginator)