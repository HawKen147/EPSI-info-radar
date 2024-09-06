from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Fonction qui fait HTTP et HTTPS pour les ESW
#Fonction qui récupere la fréquence du channel
#Récupere la page web et retourne la fréquence si elle a été trouvé
#Sinon retourne une erreur
def recupere_mode_frequence_ESW(driver):
    try:
        frequence_channel  = driver.find_element(By.XPATH, "//div[@id='mat-select-value-1']//span[contains(@class, 'mat-select-value-text')]//span").text
        print(f"#######################################################\n Voici la frequence du channel : {frequence_channel}")
        return frequence_channel
    except Exception as e :
        print(f"Impossible de récuperer le canal de fréquence : {e}")
        return "Erreur"
    
####################################################
################### Partie HTTPS ###################
####################################################

#Fonction qui récupère la version du firmware en HTTPS
#Récupere la page web et retourne la version du firmware si elle a été trouvé
#Sinon retourne une erreur
def recupere_firmware_version_https(driver):
    try :
        #Trouve l'élément 'SYSTEM'
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'SYSTEM')]")))
        firmware_element = driver.find_element(By.XPATH, "//div[contains(text(), 'SYSTEM')]")
        #Trouve la div suivante (la version du firmware)
        WebDriverWait(driver, 30).until(
            lambda driver: firmware_element.find_element(By.XPATH, "following-sibling::div").text.strip() != ""
        )
        #Récupére et affiche la version du firmware
        firmware_version = firmware_element.find_element(By.XPATH, "following-sibling::div").text.strip()
        print(f"#######################################################\nVoici la version du firmware : {firmware_version}")
        return firmware_version
    except Exception as e :
        print(f"Impossible de récuperer la version du firmware : {e}")
        return "Erreur"
    
#Fonction qui récupere le numéro de série du radar, ne fonctionne que pour les ESW sous la version 1.5.2 ou ulterieur
#Récupere la page web et retourne la version du firmware si elle a été trouvé
#Sinon retourne une erreur
def recupere_numero_serie_https(driver):
    try :
        #trouve l'element numéro de série
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'SN')]")))
        div_numero_serie = driver.find_element(By.XPATH, "//div[contains(text(), 'SN')]")
        WebDriverWait(driver, 30).until(        #Vérifie si la div contient du texte avant de continuer
            lambda driver: div_numero_serie.find_element(By.XPATH, "following-sibling::div").text.strip() != ""
        )
        numero_serie = div_numero_serie.find_element(By.XPATH, "following-sibling::div").text.strip()
        if numero_serie == "" :
            return False
        print(f"#######################################################\nVoici le numero de série : {numero_serie}")
        return numero_serie
    except Exception as e :
        print(f"Impossible de récuperer le numéro de serie : {e}")
        return "Erreur"



#Fonction qui récupère la distance de la zone du radar en HTTPS
#Récupere la page web et retourne la distance si elle a été trouvé
#Sinon retourne une erreur
def recupere_distance_https(driver):
    try :
        #Récupere le channel du radar
        # Accès à l'élément input
        parametre_distance = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@formcontrolname='maxOperationalRange']"))
        )
        # Récupération de la valeur de l'input
        WebDriverWait(driver, 30).until(        #Vérifie si la div contient du texte avant de continuer
            lambda driver: parametre_distance.find_element(By.XPATH, "//input[@formcontrolname='maxOperationalRange']").get_attribute("value")!= ""
        )
        valeur_distance = parametre_distance.get_attribute("value")
        print(f"#######################################################\nVoici la distance : {valeur_distance}")
        return valeur_distance
    except Exception as e :
        print(f"Impossible de récuperer la distance de la zone : {e}")
        return "Erreur"

#Fonction qui récupere le mode du radar en HTTPS
#Récupere la page web et retourne le mode du radar si elle a été trouvé
#Sinon retourne une erreur
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
            print(f"#######################################################\nVoici le mode : {channel_mode[0]}")
            return channel_mode[0]
        except Exception as e:
            print(f"Impossible de récuperer le mode du channel : {e}")
            return "Erreur"
        


####################################################
################### Partie HTTP ####################
####################################################

#Fonction qui récupere la version du firmware en HTTP
#Récupere la page web et retourne la version du firmware si elle a été trouvé
#Sinon retourne une erreur
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
        print(f"#######################################################\nVoici la version du firmware : {firmware_version}")
        return firmware_version
    except Exception as e :
        print(f"Impossible de récuperer la version du firmware : {e}")
        return "Erreur"
    
#Fonction qui récupere la distance de la zone radar en HTTP
#Récupere la page web et retourne la distance de la zone si elle a été trouvé
#Sinon retourne une erreur
def recupere_distance_http(driver):
    try :    
        #Récupere le channel du radar
        # Accès à l'élément input
        parametre_distance = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@formcontrolname='scopeMax']"))
        )
        # Récupération de la valeur de l'input
        valeur_distance = parametre_distance.get_attribute("value")
        print(f"#######################################################\nVoici la distance : {valeur_distance}")
        return valeur_distance
    except Exception as e :
        print(f"Impossible de récuperer la distance de la zone : {e}")
        return "Erreur"

#Fonction qui récupere le mode du radar
#Récupere la page web et retourne le mode du radar si il a été trouvé
#Sinon retourne une erreur
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
        print(f"#######################################################\nVoici le mode du channel : {channel_mode[0]}")
        return channel_mode[0]
    except Exception as e :
        print(f"Impossible de récuperer le mode : {e}")
        return "Erreur"
    

#Fonction qui récupere la version du firmware en HTTP
#Récupere la page web et retourne la version du firmware si elle a été trouvé
#Sinon retourne une erreur
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
        print(f"#######################################################\nVoici la version du firmware : {firmware_version}")
        return firmware_version
    except Exception as e :
        print(f"Impossible de récuperer la version du firmware : {e}")
        return "Erreur"
    
#Fonction qui récupere la distance de la zone radar en HTTP
#Récupere la page web et retourne la distance de la zone si elle a été trouvé
#Sinon retourne une erreur
def recupere_distance_http(driver):
    try :    
        #Récupere le channel du radar
        # Accès à l'élément input
        parametre_distance = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@formcontrolname='scopeMax']"))
        )
        # Récupération de la valeur de l'input
        valeur_distance = parametre_distance.get_attribute("value")
        print(f"#######################################################\nVoici la distance : {valeur_distance}")
        return valeur_distance
    except Exception as e :
        print(f"Impossible de récuperer la distance de la zone : {e}")
        return "Erreur"

#Fonction qui récupere le mode du radar
#Récupere la page web et retourne le mode du radar si il a été trouvé
#Sinon retourne une erreur
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
        print(f"#######################################################\nVoici le mode du channel : {channel_mode[0]}")
        return channel_mode[0]
    except Exception as e :
        print(f"Impossible de récuperer le mode : {e}")
        return "Erreur"