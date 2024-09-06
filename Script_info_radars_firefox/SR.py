from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Fonction qui récupere la portée max du radar (SR)
def recupere_portee_max(driver):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mat-input-3"]')))
        div_portee_max = driver.find_element(By.XPATH, '//*[@id="mat-input-3"]')
        portee_max = div_portee_max.get_attribute("value")
        print(f"#######################################################\nVoici la portée max du radar : {portee_max}")
        return portee_max
    except Exception as e :
        print(f"Impossible de récuperer la portée max du radar : {e}")
        return "Erreur"
    

#Fonction qui récupere l'ouverture maximal, disponible que pour les radars SR
def recupere_ouverture_max(driver):
    try:
        div_ouverture_max = driver.find_element(By.ID, "mat-input-4")
        ouverture_max = div_ouverture_max.get_attribute("value")
        print(f"#######################################################\nVoici l'ouverture maximal du SR' : {ouverture_max}")
        return ouverture_max
    except Exception as e :
        print(f"Impossible de récuperer l'ouverture maximal pour le SR : {e}")
        return "Erreur"
    
#Fonction qui recupere la fréquence du channel pour les SR
#Récupere la page web et retourne la fréquence si elle a été trouvé
#Sinon retourne une erreur
def recupere_mode_frequence_SR(driver):
    try :
        frequence_channel_SR = driver.find_element(By.XPATH, "/html/body/app-root/app-main-layout/div/main/ng-component/div/form/app-radar-properties-container/mat-accordion/mat-expansion-panel/div/div/app-radar-properties/app-frequency-channel-container/app-frequency-channels/mat-form-field/div/div[1]/div/mat-select/div/div[1]/span/span").text
        print(f"#######################################################\nVoici la frequence du channel : {frequence_channel_SR}")
        return frequence_channel_SR
    except Exception as e :
        print(f"Impossible de récuperer le chacanalnnel de fréquence : {e}")
        return "Erreur"