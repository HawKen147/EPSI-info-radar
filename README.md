# DataRadarPy, pour les radars EPSI

DataRadarPy est un script python qui permet de récuperer les differentes informations des radars.
Le script récupere les informations depuis la page web du radar. il faut donc connaitre l'adresse IP des radars.

## Comment utiliser le script ?

Pour utiliser le script il faut télécharger le fichier ZIP DataRadarPy et s'assurer que firefox soit bien installer sur la machine.
Si firefox n'est pas installer le script ne marchera pas en enverra une erreur (Driver location not found). Firefox doit etre dans le répertoire courant C:\Program Files\Mozilla Firefox\firefox.exe.
La deuxième étape consiste a lancé le script. Rendez vous dans le répertoire ou le script a été installer, et lancer le depuis la console cmd. Le script va démarrer en vous demandant de rentrer le login, le mot de passe et la plage d'adresse ip. La plage d'adresse ip doit etre comme cela : 
- IP_debut IP_fin
Si il y'a une erreur lorsque vous rentrez les informations, il ne sera pas possible de revenir en arrière, il faudra arreter le script (crtl + c) et le relancer.
Une fois le script lancé il s'éxecutera, lorsqu'il arrivera sur la dernier adresse IP il ecrira les infomations dans le fichiers Excel.

## Les informations que le script récupere (V 1.0)

Le script (V1.0) récupere certaines informations qui sont disponibles selon la version mais aussi le type de radar.
- Les radars SR n'ont pas de mode (caractéristique d'installation)
- Les PSR-200, PSR-500 n'ont que la version du firmware qui est disponible
- Les ESW n'ont pas d'ouverture maximal contrairement au SR
Les radars qui n'ont pas les informations, auront dans le fichier excel, la valeur "Non disponible"

### Les informations selon la version des radars
Les radars ayant le firmware 1.5.2 (ou ultérieur), ne peuvent se connecter qu'en HTTPS.
Le script permet de récuperer les informations suivantes : 
- le type de radar (ESW, SR, PSR-200, PSR-500); (Actuellement, seul les ESW sont sous la version 1.5.2)
- La version du firmware du radar
- La distance de la zone
- Le mode du radar
- La fréquence du canal
- Le numéro de série du radar (Seulement pour les radars avec le firmware 1.5.2)

Pour les versions antérieurs à la version 1.5.2, la connexion se fait en http.
Les informations récuperées sont les suivantes :
- Le type de radar (ESW, SR, PSR-200, PSR-500)
- La version du firmware
- La distance de la zone
- Le mode du radar
- La fréquence du canal

## Les erreurs possibles du script
Le script enverra une erreur, si l'information n'est pas disponible. La bibliothèque python [selenium](https://www.selenium.dev/) affichera dans le terminal les erreurs possibles. N'hésitez pas a me contacter si vous avez des erreurs.
Le script essayera de se connecter en HTTPS en premier, si il n'y arrive pas une erreur en envoyé dans le terminal et le script essayera en HTTP. Si il n'y arrive toujours pas en HTTP, alors le script affichera l'adresse IP dans le fichier excel avec toutes les autres cellules vides.
Si le script n'arrive pas a récupérer une informations d'un radar, il écrira 'Erreur' dans la cellule, en renverra une erreur dans le terminal.

![Screenshot d'une execution du script avec un echec de connexion HTTPS et un nouvelle essaie pour HTTP.](https://www.aht.li/3870439/Capture_decran_2024-09-06_141820.png)


