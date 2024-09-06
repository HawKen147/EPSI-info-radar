from getpass import getpass
import connexion_http
import connexion_https
import creation_excel as CEX


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
        driver = connexion_https.connexion_https(ip_debut_radar)       #Se connecte au radar en https, sinon retourne false
        if driver == False:
            driver = connexion_http.connexion_http(ip_debut_radar)        #Se connecte au radar en http, sinon retourne false
            if driver == False:
                print(f"Il y a eu une erreur, impossible de récuperer les informations de {ip_debut_radar}")
                tab_resultat.append([ip_debut_radar])
        if driver :
            tab_resultat = recupere_info_radar(driver, login, password, ip_debut_radar, tab_resultat)       #Fonction qui récupère les informations des radars
        ip_debut_radar = recupere_prochaine_ip(ip_debut_radar, ip_fin_radar)        #Fonction qui vérifie si la prochaine IP est dans la plage IP
        if ip_debut_radar == False :        #Si la prochaine IP est FALSE, on sort de la boucle
            break
    CEX.creation_excel(tab_resultat)        #Fonction qui crée le fichier excel

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
        tab_resultat = connexion_https.recupere_info_radar_https(driver, login, password, temp_tab, tab_resultat)       #Récupere les informations des radars avec la connexion https (balises http son differentes selon les versions http et https)   
        return tab_resultat
    else : 
        tab_resultat = connexion_http.recupere_info_radar_http(driver, login, password, temp_tab, tab_resultat)        #Récuperer les informations des radars avec la connexion http
        return tab_resultat

#Appel la fonction principale
if __name__ == '__main__':
    main()   