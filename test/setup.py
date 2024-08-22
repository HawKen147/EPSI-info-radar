import sys
from cx_Freeze import setup, Executable

# Spécifiez le script que vous souhaitez transformer en exécutable
script_name = "Script_connexion_psr_srv.py"

# Options pour cx_Freeze
build_exe_options = {
    "packages": ["selenium", "getpass", "time"],  # Inclure les packages nécessaires
    "excludes": ["tkinter"],  # Exclure 'tkinter' si vous n'en avez pas besoin
    "include_files": []  # Inclure des fichiers supplémentaires si nécessaire
}

# Définir la base en fonction de la plateforme
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Utiliser "Win32GUI" pour les applications GUI, ou laissez à None pour un script console

# Configuration de cx_Freeze
setup(
    name="get_radar_state",
    version="1.0",
    description="Description de votre application",
    options={"build_exe": build_exe_options},
    executables=[Executable(script_name, base=None)]    #base=None permet d'utiliser la console avec les input de python
)
