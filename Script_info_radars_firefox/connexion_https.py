from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service 
import os
import os.path
import ESW
import SR
import deplacement_web as DW

#Fonction qui se connecte au radar en https
#Actuellement, Si on est en HTTPS, on est forcement dans un radar ESW
def connexion_https(ip_radar):
    try :
        service = Service(executable_path=os.path.join(os.getcwd(), 'geckodriver.exe'))  #Construit l'objet webdriver avec les options
        firefox_options = Options()        #Permet d'ajouter des options de connexion
        firefox_options.add_argument("--headless")     #Permet de se connecter sans afficher l'interface web
        firefox_options.add_argument("--log-level=3")      #N'affiche pas les message de logs
        firefox_options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        driver = webdriver.Firefox(service=service,options=firefox_options)
        driver.get(f"https://{ip_radar}")       #Se connecte au radar depuis l'interface web avec les options
        print(f"#######################################################\nconnexion au radar {ip_radar} en HTTPS")
        driver = DW.web_page_connexion_privee(driver)      #Fonction qui vérifie l'url, et qui va passer la page qui indique que la connexion n'est pas sécurisé
        return driver       #Retourne le webdriver(la page web)
    except Exception as e:
        print(f"il y a une erreur pour se connecter en https : {e} \nNouvelle essaie avec http")
        return False
    

#Fonction qui récupere les informations (https)
def recupere_info_radar_https(driver, login, password, temp_tab, tab_resultat):
    try :
        driver = DW.connexion_radar(login, password, driver)
        WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-backdrop cdk-overlay-dark-backdrop")))
        numero_serie = ESW.recupere_numero_serie_https(driver)
        temp_tab.append(" ESW")                  #Tous les radars en HTTPS sont des ESW (pour l'instant)
        temp_tab.append(ESW.recupere_firmware_version_https(driver))
        driver = DW.acces_page_operation(driver)
        temp_tab.append(ESW.recupere_distance_https(driver))
        temp_tab.append(ESW.recupere_mode_channel_https(driver))
        temp_tab.append(ESW.recupere_mode_frequence_ESW(driver))
        temp_tab.append("Non disponible")
        temp_tab.append(numero_serie)
        tab_resultat.append(temp_tab)
        driver.quit()  
        return tab_resultat
    except Exception as e :
        print(f"Erreur pour récuperer les éléments : {e}")
        driver.quit()


