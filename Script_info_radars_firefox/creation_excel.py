import openpyxl
import os
import os.path

#Fonction qui créer le fichier excel
#Récupere les resultats des radars sous forme de list de list
def creation_excel(resultats):
    print(f"#######################################################\nCréation du fichier excel...\n#######################################################")
    workbook = openpyxl.Workbook()
    nom_fichier = save_excel()
    sheet = workbook.active
    sheet = ajoute_info_dans_excel(sheet, resultats)
    creer_dossier_data()
    workbook.save(f"{os.getcwd()}\\data\\{nom_fichier}")        #Sauvegarde le fichier excel dans le dossier data du repertoire ou est situé le script
    print(f"Le fichier excel : {nom_fichier}, est disponible ici {os.getcwd()}\\data")
    print(f"####################################################### Fin execution du script #######################################################")

#Fonction qui incrémente le nom du fichier si il est deja existant
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

#Fonction qui ajoute les info radar dans la page du fichier excel
def ajoute_info_dans_excel(sheet, resultats):
    sheet = ajoute_titre_excel(sheet)
    sheet = ajoute_info_radar_excel(sheet, resultats)
    return sheet

#Fonction qui fait la mise en page du fichier excel
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

#Fonction qui ajoute les information des radars dans le fichier excel
#Boucle sur la list de list [[info,radar,1], [info,radar,2],[...]...]
def ajoute_info_radar_excel(sheet, resultats):
    for lists in resultats :            # Récupere les tableaux dans le tableau
            sheet.append(lists)
    return sheet

#Fonction qui vérifie si le dossier data exist, si il n'existe pas le crée
def creer_dossier_data():
    path = os.getcwd()
    if not os.path.isdir(f"{path}\\data") :
        os.mkdir('data')
    else :
        pass