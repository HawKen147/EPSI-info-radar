from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service 
import os
import os.path
import deplacement_web as DW
import ESW
import SR

#Fonction qui se connecte au radar depuis l'interface web en http
def connexion_http(ip_radar):
    try :
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--log-level=3")
        firefox_options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        service = Service(executable_path=os.path.join(os.getcwd(), 'geckodriver.exe'))
        driver = webdriver.Firefox(service=service,options=firefox_options)
        driver.get(f"http://{ip_radar}")
        print(f"#######################################################\nconnexion au radar {ip_radar} en HTTP")
        driver = DW.web_page_connexion_privee(driver)
        return driver
    except Exception as e:
        print(f"il y a une erreur lors de la connexion http: {e}")
        return False 

#Fonction qui récupere les informations des radars (http)
def recupere_info_radar_http(driver, login, password, temp_tab, tab_resultat):
    try :
        driver = DW.connexion_radar(login, password, driver)
        WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-backdrop cdk-overlay-dark-backdrop")))
        type_radar = recupere_type_radar_http(driver)
        temp_tab.append(type_radar)           #Fonction qui récupere le type de radar
        temp_tab.append(ESW.recupere_firmware_version_http(driver))     #Fonction qui récupere la version du firmware
        driver = DW.acces_page_operation(driver)
        if "ESW" in type_radar :
            temp_tab.append(ESW.recupere_distance_http(driver))             #Fonction qui récupere la distance de la zone
            temp_tab.append(ESW.recupere_mode_channel_http(driver))
            temp_tab.append(ESW.recupere_mode_frequence_ESW(driver))
            temp_tab.append("Non disponible")                           #Le ESW n'a pas d'ouverture maximal
            temp_tab.append("Non disponible")                           #Pas de numéro de serie sur les version antérieur a 1.5.2
        elif "SR" in type_radar:
            temp_tab.append(SR.recupere_portee_max(driver))
            temp_tab.append("Non disponible")                       #Le SR n'a pas de mode de channel
            temp_tab.append(SR.recupere_mode_frequence_SR(driver))
            temp_tab.append(SR.recupere_ouverture_max(driver))
            temp_tab.append("Non disponible")
        else :
            temp_tab.append(ESW.recupere_mode_channel_http(driver))         #Fonction qui récupere le mode du radar
            temp_tab.append("Non disponible")                                                                                      #Les PSR-200 et PSR-500 n'ont pas ses fonctionnalitées
            for i in range(5):
                temp_tab.append("non disponible")
        tab_resultat.append(temp_tab)
        driver.quit()       #Ferme le navigateur
        return tab_resultat
    except Exception as e :
        print(f"Erreur pour récuperer les éléments : {e}")
        driver.quit()

#récupere le type du radar (ESW, SR, PSR-200, PSR-500)
def recupere_type_radar_http(driver):
    try :
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-main-layout/div/header/app-header/div/div[2]/span")))
        balise_type_radar = driver.find_element(By.XPATH, "/html/body/app-root/app-main-layout/div/header/app-header/div/div[2]/span")
        WebDriverWait(driver, 10).until(
            lambda driver: balise_type_radar.find_element(By.XPATH, "/html/body/app-root/app-main-layout/div/header/app-header/div/div[2]/span").text.strip() != ""
        )
        balise_type_radar = driver.find_element(By.XPATH, "/html/body/app-root/app-main-layout/div/header/app-header/div/div[2]/span").text.strip()
        type_radar = balise_type_radar.split(':')
        print(f"#######################################################\nLe type du radar : {type_radar[-1]}")
        return type_radar[-1]
    except Exception as e :
        print(f"Impossible de récuperer le type de radar : {e}")
        return "Erreur"