from selenium import webdriver
from getpass import getpass
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service 
import time
import openpyxl
import os
import os.path

#################################################################
### Script qui récupere les informations du Radar : #############
### Il permet de récupérer la distance, le mode et la version ###
### Le script ne fonctionne que pour les réseaux /24 ############
#################################################################


#Fonction principale 
def main():
    login, password, ip_radars = get_info()     #Récupere les informations de connexions
    try:
        ip_debut_radar, ip_fin_radar = ip_radars.split(' ')     #Vérifie si il y'a une plage d'adresse ip (deux adresses ip)
    except :
        ip_debut_radar = ip_radars
        ip_fin_radar = ip_radars
    tab_resultat = []           #List des informations qui seront ajouté dans le fichier excel
    while True :
        print(f"Tentative de connexion au radar {ip_debut_radar}")
        driver = connexion_https(ip_debut_radar)       #Se connecte au radar en https
        if driver == False:
            driver = connexion_http(ip_debut_radar)        #Se connecte au radar en http
            if driver == False:
                print(f"Il y a eu une erreur, impossible de récuperer les informations de {ip_debut_radar}")
                return -1
        tab_resultat = recupere_info_radar(driver, login, password, ip_debut_radar, tab_resultat)       #Fonction qui récupère les informations des radars
        ip_debut_radar = recupere_prochaine_ip(ip_debut_radar, ip_fin_radar)        #Fonction qui vérifie si la prochaine IP est dans la plage IP
        if ip_debut_radar == False :        #Si la prochaine IP est FALSE, on sort de la boucle
            break
    creation_excel(tab_resultat)        #Fonction qui crée le fichier excel

#Récupere les infos, login, mot de passe et la plage d'ip radar et les retourne
def get_info():
    login = input("Entrer le login pour se connecter aux radars : ")
    password = getpass("Entrer le mot de passe pour se connecter aux radars : ")
    ip_radars = input("Entrer la plage d'adresse ip (192.168.0.1 192.168.0.25) : ")
    return login, password, ip_radars

#Fonctionne seulement pour les réseaux en /24
def recupere_prochaine_ip(ip_radar, ip_fin_radar):
    octets = list(map(lambda x: int(x), ip_radar.split('.')))       #Transforme l'adresse ip en list d'entier -> 192.168.1.12 -> [192, 168, 1, 12]
    fin_octets = list(map(lambda x: int(x), ip_fin_radar.split('.')))
    if octets[-1] + 1 <= fin_octets[-1]:            #Verifie que le denrier bit +1 soit equal ou inférieur qu dernier bit maximal, evite de faire un tour de boucle supplémentaire
        octets[-1] += 1
        ip_adresse = (f"{octets[0]}.{octets[1]}.{octets[2]}.{octets[3]}")
        return ip_adresse
    elif octets[-2] == fin_octets[-2]:
        return False

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
        print(f"#######################################################\nconnexion au radar {ip_radar} en  HTTPS")
        driver = web_page_connexion_privee(driver)      #Fonction qui vérifie l'url, et qui va passer la page qui indique que la connexion n'est pas sécurisé
        return driver       #Retourne le webdriver(la page web)
    except Exception as e:
        print(f"il y a une erreur pour se connecter en https : {e} \nNouvelle essaie avec http")
        return False

#Fonction qui se connecte au radar depuis l'interface web en http
def connexion_http(ip_radar):
    try :
        firefox_options = Options()
        #firefox_options.add_argument("--headless")
        firefox_options.add_argument("--log-level=3")
        firefox_options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        service = Service(executable_path=os.path.join(os.getcwd(), 'geckodriver.exe'))
        driver = webdriver.Firefox(service=service,options=firefox_options)
        driver.get(f"http://{ip_radar}")
        print(f"#######################################################\nconnexion au radar {ip_radar} en HTTP")
        driver = web_page_connexion_privee(driver)
        return driver
    except Exception as e:
        print(f"il y a une erreur lors de la connexion http: {e}")
        return False

#Fonction qui vérifie si navigateur internet demande a l'utilisateur de confirmer son choix meme si la page web n'est pas sécurisé
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

#Fonction qui récupère les informations du radar
def recupere_info_radar(driver, login, password, ip_radar, tab_resultat):
    temp_tab = []       #List qui stock toutes les informations
    temp_tab.append(ip_radar)
    current_url = False
    #Boucle infinie qui vérifie que l'url soit bien disponible, sinon on ne peut pas récuperer les informations
    while current_url == False :
        try :
            current_url = driver.current_url    #Si on arrive a récuperer l'url, la page web est donc chargé. ### Créér des erreurs dans le terminal 
        except :
            current_url = False
    if "https" in current_url :
        tab_resultat = recupere_info_radar_https(driver, login, password, temp_tab, tab_resultat)       #Récupere les informations des radars avec la connexion https (balises http son differentes selon les versions http et https)   
        return tab_resultat
    else : 
        tab_resultat = recupere_info_radar_http(driver, login, password, temp_tab, tab_resultat)        #Récuperer les informations des radars avec la connexion http
        return tab_resultat

#Fonction qui récupere les informations des radars (http)
def recupere_info_radar_http(driver, login, password, temp_tab, tab_resultat):
    try :
        driver = connexion_radar(login, password, driver)
        WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-backdrop cdk-overlay-dark-backdrop")))
        type_radar = recupere_type_radar_http(driver)
        temp_tab.append(type_radar)           #Fonction qui récupere le type de radar
        temp_tab.append(recupere_firmware_version_http(driver))     #Fonction qui récupere la version du firmware
        if "ESW" in type_radar or "SR" in type_radar:
            temp_tab.append(recupere_distance_http(driver))             #Fonction qui récupere la distance de la zone
            if type_radar == "SR":
                temp_tab.append("Non disponible")                       #Le SR n'a pas de mode de channel
                temp_tab.append(recupere_mode_frequence(driver))
                temp_tab.append(recupere_ouverture_max(driver))
            else :
                temp_tab.append(recupere_mode_channel_http(driver))         #Fonction qui récupere le mode du radar
                temp_tab.append(recupere_mode_frequence(driver))
                temp_tab.append("Non disponible")                           #Le ESW n'a pas d'ouverture maximal
            
        else :
            for i in range(4):
                temp_tab.append("non disponible")
        tab_resultat.append(temp_tab)
        driver.quit()       #Ferme le navigateur
        return tab_resultat
    except Exception as e :
        print(f"Erreur pour récuperer les éléments : {e}")
        driver.quit()

#Fonction qui permet de se logger a l'interface web du radar
def connexion_radar(login, password, driver):
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
        return driver
    except Exception as e :
        print(f"Erreur lors de la connexion au radar : {e}")

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

#Fonction qui récupere les informations (https)
def recupere_info_radar_https(driver, login, password, temp_tab, tab_resultat):
    try :
        driver = connexion_radar(login, password, driver)
        WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-backdrop cdk-overlay-dark-backdrop")))
        numero_serie = recupere_numero_serie_https(driver)
        temp_tab.append("ESW")                  #Tous les radars en HTTPS sont des ESW (pour l'instant)
        temp_tab.append(recupere_firmware_version_https(driver))
        temp_tab.append(recupere_distance_https(driver))
        temp_tab.append(recupere_mode_channel_https(driver))
        temp_tab.append(recupere_mode_frequence(driver))
        temp_tab.append("Non disponible")
        temp_tab.append(numero_serie) 
        tab_resultat.append(temp_tab)
        driver.quit()  
        return tab_resultat
    except Exception as e :
        print(f"Erreur pour récuperer les éléments : {e}")
        driver.quit()

def recupere_numero_serie_https(driver):
    try :
        #trouve l'element numéro de série
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'SN')]")))
        div_numero_serie = driver.find_element(By.XPATH, "//div[contains(text(), 'SN')]")
        WebDriverWait(driver, 30).until(
            lambda driver: div_numero_serie.find_element(By.XPATH, "following-sibling::div").text.strip() != ""
        )
        # Une fois que le texte n'est plus vide, vous pouvez continuer avec d'autres actions
        numero_serie = div_numero_serie.find_element(By.XPATH, "following-sibling::div").text.strip()
        if numero_serie == "" :
            return False
        print(f"#######################################################\n Voici le numero de série : {numero_serie}")
        return numero_serie
    except Exception as e :
        print(f"Impossible de récuperer le numéro de serie : {e}")
        return "Erreur"

def recupere_firmware_version_https(driver):
    try :
        # Trouver l'élément 'SYSTEM'
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'SYSTEM')]")))
        firmware_element = driver.find_element(By.XPATH, "//div[contains(text(), 'SYSTEM')]")
        # Trouver la div suivante (la version du firmware)
        WebDriverWait(driver, 30).until(
            lambda driver: firmware_element.find_element(By.XPATH, "following-sibling::div").text.strip() != ""
        )
        # Récupérer et afficher la version du firmware
        firmware_version = firmware_element.find_element(By.XPATH, "following-sibling::div").text.strip()
        print(f"#######################################################\n Voici la version du firmware : {firmware_version}")
        return firmware_version
    except Exception as e :
        print(f"Impossible de récuperer la version du firmware : {e}")
        return "Erreur"

def recupere_distance_https(driver):
    try :
        WebDriverWait(driver, 30).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-backdrop"))
        )
        #Accede a la page "Opération"
        page_réseau = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Opération")))#Change de page, on va sur la page Opération
        page_réseau.click()
        #Récupere le channel du radar
        time.sleep(5)
        # Accès à l'élément input
        parametre_distance = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@formcontrolname='maxOperationalRange']"))
        )
        # Récupération de la valeur de l'input
        valeur_distance = parametre_distance.get_attribute("value")
        print(f"#######################################################\n Voici la distance : {valeur_distance}")
        return valeur_distance
    except Exception as e :
        print(f"Impossible de récuperer la distance de la zone : {e}")
        return "Erreur"

def recupere_mode_channel_https(driver):
        try:
            for i in range(1,5,1):
                bouton = driver.find_elements(By.ID, f"mat-button-toggle-{i}-button")
                if bouton[0].get_attribute('aria-pressed') == 'true':
                    img_element = bouton[0].find_element(By.TAG_NAME, 'img')
                    img_src = img_element.get_attribute('src')
                    break
            channel_mode = img_src.split('/')
            channel_mode = channel_mode[-1].split('.')
            print(f"#######################################################\n Voici le mode du channel : {channel_mode[0]}")
            return channel_mode[0]
        except Exception as e:
            print(f"Impossible de récuperer le mode du channel : {e}")
            return "Erreur"

def recupere_firmware_version_http(driver):
    try:
        # Trouver l'élément 'FIRMWARE'
        WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'FIRMWARE')]"))
            )
        firmware_element = driver.find_element(By.XPATH, "//div[contains(text(), 'FIRMWARE')]")
        # Trouver la div suivante (la version du firmware)
        WebDriverWait(driver, 30).until(
            lambda driver: firmware_element.find_element(By.XPATH, "following-sibling::div").text.strip() != ""
        )
        # Une fois que le texte n'est plus vide, vous pouvez continuer avec d'autres actions
        firmware_version = firmware_element.find_element(By.XPATH, "following-sibling::div").text.strip()
        print(f"#######################################################\n Voici la version du firmware : {firmware_version}")
        return firmware_version
    except Exception as e :
        print(f"Impossible de récuperer la version du firmware : {e}")
        return "Erreur"

def recupere_distance_http(driver):
    try :    
        #Accede a la page "Opération"
        WebDriverWait(driver, 30).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-backdrop"))
    )
        page_réseau = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, "Opération")))
        page_réseau.click()
        #Récupere le channel du radar
        time.sleep(5)
        # Accès à l'élément input
        parametre_distance = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@formcontrolname='scopeMax']"))
        )
        # Récupération de la valeur de l'input
        valeur_distance = parametre_distance.get_attribute("value")
        print(f"#######################################################\n Voici la distance : {valeur_distance}")
        return valeur_distance
    except Exception as e :
        print(f"Impossible de récuperer la distance de la zone : {e}")
        return "Erreur"

def recupere_mode_channel_http(driver):
    try :
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
        print(f"#######################################################\n Voici le mode du channel : {channel_mode[0]}")
        return channel_mode[0]
    except Exception as e :
        print(f"Impossible de récuperer le mode : {e}")
        return "Erreur"

#Fonction qui récupere l'ouverture maximal, disponible que pour les radars SR
def recupere_ouverture_max(driver):
    try:
        ouverture_max = WebDriverWait(driver, 10).until(EC.presence_of_element_located(By.ID, "mat-input-4")).text
        print(f"#######################################################\n Voici l'ouverture maximal du SR' : {ouverture_max}")
    except Exception as e :
        print(f"Impossible de récuperer l'ouverture maximal pour le SR : {e}")
        return "Erreur"

#Fonction qui fait HTTP et HTTPS
def recupere_mode_frequence(driver):
    try:
        frequence_channel  = driver.find_element(By.XPATH, "//div[@id='mat-select-value-1']//span[contains(@class, 'mat-select-value-text')]//span").text
        print(f"#######################################################\n Voici la frequence du channel : {frequence_channel}")
        return frequence_channel
    except Exception as e :
        print(f"Impossible de récuperer le channel de la fréquence : {e}")
        return "Erreur"

def creation_excel(resultats):
    print(f"#######################################################\nCréation du fichier excel...\n#######################################################")
    workbook = openpyxl.Workbook()
    nom_fichier = save_excel()
    sheet = workbook.active
    sheet = ajoute_info_dans_excel(sheet, resultats)
    creer_dossier_data()
    workbook.save(f"{os.getcwd()}\\data\\{nom_fichier}")
    print(f"Le fichier excel : {nom_fichier}, est disponible ici {os.getcwd()}\\data")
    print(f"####################################################### Fin execution du script #######################################################")

def save_excel():
# Tant que le fichier excel existe, on change le nom du fichier en ajoutant l'indice au nombre de fichier
    nom_fichier = "informations_radars.xlsx"
    i = 0
    while True:
        i += 1
        if not os.path.isfile(f"{os.getcwd()}\\data\\{nom_fichier}"):
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
    sheet["B1"].value = "Type du radar"
    sheet["C1"].value = "Version Firmware"
    sheet["D1"].value = "Distance de la zone"
    sheet["E1"].value = "Mode du radar"
    sheet["F1"].value = "Fréquence du canal"
    sheet["G1"].value = "Ouverture Maximale"
    sheet["H1"].value = "Numéro de série"
    sheet.column_dimensions['A'].width = 20
    sheet.column_dimensions['B'].width = 20
    sheet.column_dimensions['C'].width = 20
    sheet.column_dimensions['D'].width = 20
    sheet.column_dimensions['E'].width = 20
    sheet.column_dimensions['F'].width = 20
    sheet.column_dimensions['G'].width = 20
    sheet.column_dimensions['H'].width = 20
    return sheet

def ajoute_info_radar_excel(sheet, resultats):
    for lists in resultats :            # Récupere les tableaux dans le tableau
            sheet.append(lists)
    return sheet

def creer_dossier_data():
    path = os.getcwd()
    if not os.path.isdir(f"{path}\\data") :
        os.mkdir('data')
    else :
        pass

if __name__ == '__main__':
    main()   