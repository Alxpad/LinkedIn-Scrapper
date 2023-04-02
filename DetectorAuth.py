import chime
import time

def AuthPage(DriverPcpal, popup = None):    #   Checks if the user has left the login page.
    try:
        URL = DriverPcpal.current_url
    
    except:
        raise ValueError("ERROR: Could not retrieve current URL")

    while URL != "https://www.linkedin.com/jobs/":
        time.sleep(5)
        URL = DriverPcpal.current_url
        if URL== "https://www.linkedin.com/feed/":
            DriverPcpal.get("https://www.linkedin.com/jobs/")

def AuthPage_omitir(DriverPcpal):   #   This function is used if the user has chosen manual login
    URL = DriverPcpal.current_url
    if URL != "https://www.linkedin.com/feed/":
        return False
    
    else:
        return True    