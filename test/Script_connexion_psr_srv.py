from selenium import webdriver
from getpass import getpass
from selenium.webdriver.edge.options import Options  # Correction de l'import
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



def main():
    login = input("Entrer le login pour se connecter aux radars : ")
    password = getpass("Entrer le mot de passe pour se connecter aux radars : ")
    ip_debut_radar = input("Entrer la premiere adresse ip de la plages des radars : ")
    while len(ip_debut_radar.split('.')) != 4:
        ip_debut_radar = input("Erreur, Entrer la premiere adresse ip de la plages des radars : ")
    ip_fin_radar = input("Entrer la derniere adresse ip de la plages des radars : ")
    resultat = True
    while resultat :
        resultat = boucle_sur_radars(ip_debut_radar, ip_fin_radar, login, password)


def boucle_sur_radars(ip_debut_radar, ip_fin_radar, login, password):
    if ip_fin_radar == '' :            # Qu'une seule adresse IP à sélectionner
        resultat = connection_au_radar(ip_debut_radar, login, password)
        print("Fin de la connexion au webdriver")
        return False
    else :
        ip_radar = ip_debut_radar
        while recupere_prochaine_ip != -1 :
            resultat = connection_au_radar(ip_radar, login, password)
            ip_radar = recupere_prochaine_ip(ip_radar, ip_fin_radar)
        


def recupere_prochaine_ip(ip_radar, ip_fin_radar):
    octets = list(map(lambda x: int(x), ip_radar.split('.')))
    fin_octets = list(map(lambda x: int(x), ip_fin_radar.split('.')))
    if octets[-1] <= fin_octets[-1]:
        octets[-1] += 1
        ip_adresse = (f"{octets[0]}.{octets[1]}.{octets[2]}.{octets[3]}")
        return ip_adresse
    elif octets[-2] == fin_octets[-2]:
        return -1

def connection_au_radar(ip_radar, login, password):
    resultat_https = connection_https(ip_radar, login, password)
    if resultat_https == False :
        resultat_http = connection_http(ip_radar, login, password)
        if resultat_http == False :
            return -1
        elif resultat_http == 1 :
            print("Warning, led de couleur Orange")
            return 1
        elif resultat_http == 0 :
            print("OK, led de couleur Verte")
            return 0
        else :
            print("Critique, Led de couleur Rouge")
            return -1
    elif resultat_https == 1 :
            print("Warning, led de couleur Orange")
            return 1
    elif resultat_https == 0 :
        print("OK, led de couleur Verte")
        return 0
    else :
        print("Critique, Led de couleur Rouge")
        return -1      

def connection_https(ip_radar, login, password):
    # Essaye avec HTTPS :
    try :
        # Configurer les options pour le mode headless
        edge_options = Options()
        edge_options.add_argument("--headless")
        driver = webdriver.edge(options=edge_options)
        driver.get(f"https://{ip_radar}")
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
        #Attend que la page se charge
        time.sleep(5)
        # Trouver la div avec le texte "Connexion vers le PSR-Server"
        target_div = driver.find_element(By.XPATH, "//div[contains(text(), 'Connexion vers le PSR-Server')]")
        # Sélectionner la div précédente (celle qui contient l'image)
        previous_div = target_div.find_element(By.XPATH, "preceding-sibling::div")
        # Trouver l'élément image dans cette div
        image_element = previous_div.find_element(By.TAG_NAME, "img")
        # Récupérer le lien de l'image
        image_src = image_element.get_attribute('src')
        # Afficher le lien de l'image
        #print(f'Lien de l\'image: {image_src}')
        image_src = image_src.split("/")
        driver.quit()
        if image_src[-1] == "status-ok.png" : #led de couleur verte
            return 0
        elif image_src[-1] == "status-starting.png":   #led de couleur orange
            return 1
        else :
            return -1 # Led état rouge

    except Exception as e:
        print("il y a une erreur, nouvelle essaie avec http")
        return False

def connection_http(ip_radar, login, password):
    # essaie avec HTTP
    try :
        # Options pour Edge
        edge_options = Options()
        edge_options.add_argument("--headless")  # Mode headless (sans interface graphique)
        # Instanciation du driver Edge
        driver = webdriver.Edge(options=edge_options)
        driver.get(f"http://{ip_radar}")
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
        # Attend que la page se charge
        time.sleep(10)
        # Trouver la div avec le texte "Connexion vers le PSR-Server"
        target_div = driver.find_element(By.XPATH, "//div[contains(text(), 'Connexion vers le PSR-Server')]")
        # Sélectionner la div précédente (celle qui contient l'image)
        previous_div = target_div.find_element(By.XPATH, "preceding-sibling::div")
        # Trouver l'élément image dans cette div
        image_element = previous_div.find_element(By.TAG_NAME, "img")
        # Récupérer le lien de l'image
        image_src = image_element.get_attribute('src')
        # Afficher le lien de l'image
        image_src = image_src.split("/")
        driver.quit()
        if image_src[-1] == "status-ok.png" : #led de couleur verte
            print("etat de la led : Verte")
            return 0
        elif image_src[-1] == "status-starting.png":   #led de couleur orange
            return 1
        else :
            return -1 # Led état rouge
    except Exception as e:
        print(f"il y a une erreur dans la connexion http : {e}")


if __name__ == '__main__':
    main()