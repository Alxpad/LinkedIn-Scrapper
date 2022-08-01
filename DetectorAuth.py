import chime

def AuthPage(DriverPcpal):
    try:
        URL = DriverPcpal.current_url
    
    except:
        chime.error()
        print("ERROR: No se ha podido obtener URL actual")

    if URL != "https://www.linkedin.com/jobs/":
        chime.warning()
        input("Autorice el acceso a su cuenta desde el navegador y presione una tecla")

    else:
        chime.success()