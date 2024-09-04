import os
import os.path

chemin = os.path.join(os.getcwd(), 'geckodriver.exe')
print(os.path.isfile(chemin))
print(chemin)

for i in range(3) :
    print(i)