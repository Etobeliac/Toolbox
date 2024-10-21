import streamlit as st
import importlib.util
import os

# Titre de l'application
st.title('Mon Application avec Dérouleurs')

# Barre latérale pour la navigation
st.sidebar.header('Menu')

# Dérouleur 1 - Mettre à jour le nom de l'option
option1 = st.sidebar.selectbox('G-News', ['Scrap URL brouillon WP', 'GPT Bulk', 'Fichier 3'])

def load_module(module_name, file_path):
    if not os.path.isfile(file_path):
        st.error(f"Le fichier {file_path} est introuvable. Veuillez vérifier le chemin.")
        return None
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

if option1 == 'Scrap URL brouillon WP':
    # Chemin relatif au fichier scrap-url-brouillon-wp.py
    file_path = os.path.join('scripts', 'scrap-url-brouillon-wp.py')
    module = load_module('scrap_url_brouillon_wp', file_path)
    if module:
        # Diagnostic: Afficher les attributs du module pour vérifier ce qui est disponible
        st.write("Attributs du module chargé:", dir(module))
        # Assurez-vous que la fonction est bien nommée `scrap_brouillon_site`
        module.scrap_brouillon_site()

elif option1 == 'GPT Bulk':
    # Importer et exécuter le script gpt-bulk.py
    file_path = os.path.join('scripts', 'gpt-bulk.py')
    module = load_module('gpt_bulk', file_path)
    if module:
        module.run()

else:
    # Importer et exécuter le script fichier3.py
    file_path = os.path.join('scripts', 'fichier3.py')
    module = load_module('fichier3', file_path)
    if module:
        module.run()

