from selenium import webdriver
from getpass import getpass
from selenium.webdriver.edge.options import Options  # Correction de l'import
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import openpyxl
import os

#################################################################
### Script qui récupere les informations du Radar : #############
### Il permet de récupérer la distance, le mode et la version ###
#################################################################

def main():
    login, password, ip_radars = get_info()
    try:
        ip_debut_radar, ip_fin_radar = ip_radars.split(' ')
    except :
        ip_debut_radar = ip_radars
        ip_fin_radar = ip_radars
    tab_resultat = []
    while True :
        driver = connection_https(ip_debut_radar)
        if driver == False:
            driver = connection_http(ip_debut_radar)
            if driver == False:
                print(f"Il y a eu une erreur, impossible de récuperer les informations de {ip_debut_radar}")
                return -1
        tab_resultat = recupere_info_radar(driver, login, password, ip_debut_radar, tab_resultat)
        ip_debut_radar = recupere_prochaine_ip(ip_debut_radar, ip_fin_radar)
        if ip_debut_radar == False :
            break
    creation_excel(tab_resultat)
    
def get_info():
    login = input("Entrer le login pour se connecter aux radars : ")
    password = getpass("Entrer le mot de passe pour se connecter aux radars : ")
    ip_radars = input("Entrer la plage d'adresse ip (192.168.0.1 192.168.0.25) : ")
    return login, password, ip_radars

#Fonctionne seulement pour les réseaux en /24 
def recupere_prochaine_ip(ip_radar, ip_fin_radar):
    octets = list(map(lambda x: int(x), ip_radar.split('.')))
    fin_octets = list(map(lambda x: int(x), ip_fin_radar.split('.')))
    if octets[-1] + 1 <= fin_octets[-1]:            #Verifie que le denrier bit +1 soit equal ou inférieur qu dernier bit maximal, evite de faire un tour de boucle supplémentaire
        octets[-1] += 1
        ip_adresse = (f"{octets[0]}.{octets[1]}.{octets[2]}.{octets[3]}")
        return ip_adresse
    elif octets[-2] == fin_octets[-2]:
        return False

def connection_https(ip_radar):
    try :
        edge_options = Options()
        edge_options.add_argument("--headless")
        edge_options.add_argument("--log-level=3")
        driver = webdriver.Edge(options=edge_options)
        driver.get(f"https://{ip_radar}")
        #print(f"##########################################\n### {ip_radar} HTTPS ### \n###################################")
        driver = web_page_connexion_privee(driver)
        return driver
    except Exception as e:
        print("il y a une erreur pour se connecter en https, nouvelle essaie avec http")
        return False

def connection_http (ip_radar):
    try :
        edge_options = Options()
        edge_options.add_argument("--headless")
        edge_options.add_argument("--log-level=3")
        driver = webdriver.Edge()
        driver.get(f"http://{ip_radar}")
        #print(f"##########################################\n### {ip_radar} HTTP ### \n###################################")
        driver = web_page_connexion_privee(driver)
        return driver
    except Exception as e:
        print(f"il y a une erreur lors de la connection http: {e}")
        return False

def web_page_connexion_privee(driver):
    try :
        bouton_avance = driver.find_element(By.ID, "details-button")
        bouton_avance = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "details-button")))
        bouton_avance.click()
        lien_vers_page_connexion = driver.find_element(By.ID, "proceed-link")
        lien_vers_page_connexion = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "proceed-link")))
        lien_vers_page_connexion.click()
        return driver
    except Exception as e :
        return driver

def recupere_info_radar(driver, login, password, ip_radar, tab_resultat):
    temp_tab = []
    temp_tab.append(ip_radar)
    current_url = False
    while current_url == False :
        try :
            current_url = driver.current_url
        except :
            current_url = False
    if "https" in current_url :
        tab_resultat = recupere_info_radar_https(driver, login, password, temp_tab, tab_resultat)
        return tab_resultat
    else : 
        tab_resultat = recupere_info_radar_http(driver, login, password, temp_tab, tab_resultat)
        return tab_resultat

def recupere_info_radar_http(driver, login, password, temp_tab, tab_resultat):
    try :
        login_label = driver.find_element(By.ID, "usernameInput")
        login_label = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "usernameInput")))
        login_label.click()
        login_label.send_keys(login)
        password_label = driver.find_element(By.ID, "passwordInput")
        password_label = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "passwordInput")))
        password_label.click()
        password_label.send_keys(password)
        valider_button = driver.find_element(By.CLASS_NAME, "mat-button-wrapper")
        valider_button.click()
        time.sleep(5)
        temp_tab.append(recupere_firmware_version_http(driver))
        temp_tab.append(recupere_distance_http(driver))
        temp_tab.append(recupere_mode_channel_http(driver))  
        tab_resultat.append(temp_tab)
        driver.quit()  
        return tab_resultat
    except Exception as e :
        print(f"Erreur pour récuperer les éléments : {e}")


def recupere_info_radar_https(driver, login, password, temp_tab, tab_resultat):
    try :
        login_label = driver.find_element(By.ID, "usernameInput")
        login_label = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "usernameInput")))
        login_label.click()
        login_label.send_keys(login)
        password_label = driver.find_element(By.ID, "passwordInput")
        password_label = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "passwordInput")))
        password_label.click()
        password_label.send_keys(password)
        valider_button = driver.find_element(By.CLASS_NAME, "mat-button-wrapper")
        valider_button.click()
        #fin de la connexion au radar
        time.sleep(5) #on attends 5s le temps que les informations se chargent
        numero_serie = (recupere_numero_serie_https(driver))
        temp_tab.append(recupere_firmware_version_https(driver))
        temp_tab.append(recupere_distance_https(driver))
        temp_tab.append(recupere_mode_channel_https(driver))
        temp_tab.append(numero_serie) 
        tab_resultat.append(temp_tab)
        driver.quit()  
        return tab_resultat
    except Exception as e :
        print(f"Erreur pour récuperer les éléments : {e}")

def recupere_numero_serie_https(driver):
    #trouve l'element numéro de série
    div_SN = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'SN')]")))
    numero_serie = div_SN.find_element(By.XPATH, "following-sibling::div")
    numero_serie = numero_serie.text.strip()
    #print(f"#######################################################\n Voici le numero de série : {numero_serie}")
    return numero_serie

def recupere_firmware_version_https(driver):
    # Trouver l'élément 'SYSTEM'
    firmware_element = driver.find_element(By.XPATH, "//div[contains(text(), 'SYSTEM')]")
    # Trouver la div suivante (la version du firmware)
    firmware_version_element = firmware_element.find_element(By.XPATH, "following-sibling::div")
    # Récupérer et afficher la version du firmware
    firmware_version = firmware_version_element.text.strip()
    #print(f"#######################################################\n Voici la version du firmware : {firmware_version}")
    return firmware_version

def recupere_distance_https(driver):
    #Accede a la page "Opération"
        page_réseau = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Opération")))
        page_réseau.click()
        #Récupere le channel du radar
        time.sleep(5)
        # Accès à l'élément input
        parametre_distance = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@formcontrolname='maxOperationalRange']"))
        )
        # Récupération de la valeur de l'input
        valeur_distance = parametre_distance.get_attribute("value")
        #print(f"#######################################################\n Voici la version de la distance : {valeur_distance}")
        return valeur_distance

def recupere_mode_channel_https(driver):
        for i in range(1,5,1):
            bouton = driver.find_elements(By.ID, f"mat-button-toggle-{i}-button")
            if bouton[0].get_attribute('aria-pressed') == 'true':
                img_element = bouton[0].find_element(By.TAG_NAME, 'img')
                img_src = img_element.get_attribute('src')
                break
        channel_mode = img_src.split('/')
        channel_mode = channel_mode[-1].split('.')
        #print(f"#######################################################\n Voici la version du mode du channel : {channel_mode[0]}")
        return channel_mode[0]

def recupere_firmware_version_http(driver):
    # Trouver l'élément 'FIRMWARE'
    firmware_element = driver.find_element(By.XPATH, "//div[contains(text(), 'FIRMWARE')]")
    # Trouver la div suivante (la version du firmware)
    firmware_version_element = firmware_element.find_element(By.XPATH, "following-sibling::div")
    # Récupérer et afficher la version du firmware
    firmware_version = firmware_version_element.text.strip()
    return firmware_version

def recupere_distance_http(driver):
        #Accede a la page "Opération"
        page_réseau = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Opération")))
        page_réseau.click()
        #Récupere le channel du radar
        time.sleep(5)
        # Accès à l'élément input
        parametre_distance = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@formcontrolname='scopeMax']"))
        )
        # Récupération de la valeur de l'input
        valeur_distance = parametre_distance.get_attribute("value")
        return valeur_distance

def recupere_mode_channel_http(driver):
        buttons = driver.find_elements(By.CLASS_NAME, "mat-button-toggle-button")
        # Parcourir tous les boutons pour trouver celui qui est "aria-pressed=true"
        for button in buttons:
            if button.get_attribute('aria-pressed') == 'true':
                # Récupérer l'image associée au mode
                img_element = button.find_element(By.TAG_NAME, 'img')
                img_src = img_element.get_attribute('src')
                break  # On peut arrêter la boucle après avoir trouvé le bouton pressé
        channel_mode = img_src.split('/')
        channel_mode = channel_mode[-1].split('.')
        return channel_mode[0]

def creation_excel(resultats):
    workbook = openpyxl.Workbook()
    nom_fichier = save_excel()
    #workbook = openpyxl.load_workbook(nom_fichier)
    sheet = workbook.active
    sheet = ajoute_info_dans_excel(sheet, resultats)
    workbook.save(nom_fichier)
    print(f"Le fichier excel : {nom_fichier}, est disponible ici {os.path}")

def save_excel():
# Tant que le fichier excel existe, on change le nom du fichier en ajoutant l'indice au nombre de fichier
    nom_fichier = "informations_radars.xlsx"
    i = 0
    while True:
        i += 1
        if not os.path.isfile(nom_fichier):
            return nom_fichier
        else:
            nom_fichier = f"informations_radars({i}).xlsx"

def ajoute_info_dans_excel(sheet, resultats):
    sheet = ajoute_titre_excel(sheet)
    sheet = ajoute_info_radar_excel(sheet, resultats)
    return sheet
    
def ajoute_titre_excel(sheet):
    sheet.title = "info_radars"
    sheet["A1"].value = "adresse ip radars"
    sheet["B1"].value = "Version Firmware"
    sheet["C1"].value = "Distance de la zone"
    sheet["D1"].value = "Mode du radar"
    sheet["E1"].value = "Numéro de série"
    sheet.column_dimensions['A'].width = 20
    sheet.column_dimensions['B'].width = 20
    sheet.column_dimensions['C'].width = 20
    sheet.column_dimensions['D'].width = 20
    sheet.column_dimensions['E'].width = 20
    return sheet

def ajoute_info_radar_excel(sheet, resultats):
    for lists in resultats :            # Récupere les tableaux dans le tableau
            sheet.append(lists)
    return sheet

if __name__ == '__main__':
    main()   