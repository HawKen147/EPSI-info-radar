from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Fonction qui permet de se logger a l'interface web du radar
def connexion_radar(login, password, driver):
    try :
        login_label = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "usernameInput")))
        login_label.click()
        login_label.send_keys(login)
        password_label = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "passwordInput")))
        password_label.click()
        password_label.send_keys(password)
        valider_button = driver.find_element(By.CLASS_NAME, "mat-button-wrapper")
        valider_button.click()
        return driver
    except Exception as e :
        print(f"Erreur lors de la connexion au radar : {e}")

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
    
def acces_page_operation(driver):
    try :
        #On attend que l'élément qui bloque la page pour cliquer disparaisse
        WebDriverWait(driver, 30).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-backdrop"))             
    )
        #On change de page, une fois l'élément cliquable est disponible
        #On arrive sur la page "Opération"
        page_réseau = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, "Opération")))
        page_réseau.click()
        return driver
    except Exception as e:
        print(f"Impossible d'acceder a la page Opération : {e}")