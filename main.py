from selenium import webdriver
from getpass import getpass
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

"""
login = input("Entrer le login pour se connecter aux radars : ")
password = input("Entrer le mot de passe pour se connecter aux radars : ")
ip_radar = input("Entrer l'adresse ip du radar : ")"""

ip_radar = "192.168.0.31"

####################
#essaie avec https
"""try :
    driver = webdriver.Firefox()
    driver.get(f"https://{ip_radar}")

except Exception as e:
   print("il y a une erreur, nouvelle essaie avec http")
finally :
    driver.quit()
"""
try :
    driver = webdriver.Firefox()
    driver.get(f"http://{ip_radar}")
    login_label = driver.find_element(By.ID, "usernameInput")
    login_label = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "usernameInput")))
    login_label.click()
    login_label.send_keys("admin")
    password_label = driver.find_element(By.ID, "passwordInput")
    password_label = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "passwordInput")))
    password_label.click()
    password_label.send_keys("admin")
    valider_button = driver.find_element(By.CLASS_NAME, "mat-button-wrapper")
    valider_button.click()

    time.sleep(5)
    # Trouver l'élément 'FIRMWARE'
    firmware_element = driver.find_element(By.XPATH, "//div[contains(text(), 'FIRMWARE')]")
    # Trouver la div suivante (la version du firmware)
    firmware_version_element = firmware_element.find_element(By.XPATH, "following-sibling::div")
    # Récupérer et afficher la version du firmware
    firmware_version = firmware_version_element.text.strip()
    print(f'Version du firmware: {firmware_version}')

    #Accede a la page "Opération"
    page_réseau = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Opération")))
    page_réseau.click()

    #Récupere le channel du radar
    time.sleep(5)
    parametre_channel = WebDriverWait(driver, 10).until(
       EC.visibility_of_element_located((By.ID, "mat-select-value-1"))
    )
    print(f"La valeur du Channel est : {parametre_channel.text}")
    #print(parametre_channel.text)    # extrait la veleur du input du channel du radar

    # Accès à l'élément input
    parametre_distance = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@formcontrolname='scopeMax']"))
    )

    # Récupération de la valeur de l'input
    valeur_distance = parametre_distance.get_attribute("value")
    print(f"Valeur de la distance : {valeur_distance}")

    buttons = driver.find_elements(By.CLASS_NAME, 'mat-button-toggle-button')

    # Parcourir tous les boutons pour trouver celui qui est "aria-pressed=true"
    for button in buttons:
        if button.get_attribute('aria-pressed') == 'true':
            # Récupérer l'ID du bouton
            button_id = button.get_attribute('id')

            # Récupérer l'image associée au mode
            img_element = button.find_element(By.TAG_NAME, 'img')
            img_src = img_element.get_attribute('src')

            # Afficher le résultat
            print(f'Bouton pressé ID: {button_id}')
            print(f'Image Source: {img_src}')
            break  # On peut arrêter la boucle après avoir trouvé le bouton pressé
    time.sleep(10)

except Exception as e:
    print(f"il y a une erreur : {e}")



##################################################################################################################################
### Le radar est connecté au PSR serveur : <img _ngcontent-toy-c83="" class="dg-icons" src="./assets/img/icons/status-ok.png"> ###
##################################################################################################################################


"""radar_ip_list = input ("Entrer la plage d'adresse ip des radars (exemple : 192.168.0.1 192.168.0.200) : ")"""

"""adresse_ip_debut, adresse_ip_fin = radar_ip_list.split(' ')
debut_ip_octet_1, debut_ip_octet_2, debut_ip_octet_3, debut_ip_octet_4  = adresse_ip_debut.split('.')
fin_ip_octet_1, fin_ip_octet_2, fin_ip_octet_3, fin_ip_octet_4  = adresse_ip_fin.split('.')

while debut_ip_octet_4 != fin_ip_octet_4 :"""
    