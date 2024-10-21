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
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

if option1 == 'Scrap URL brouillon WP':
    # Importer et exécuter le script scrap-url-brouillon-wp.py
    module = load_module('scrap_url_brouillon_wp', os.path.join('scripts', 'scrap-url-brouillon-wp.py'))
    module.scrap_brouillon_site()
    
elif option1 == 'GPT Bulk':
    # Importer et exécuter le script gpt-bulk.py
    module = load_module('gpt_bulk', os.path.join('scripts', 'gpt-bulk.py'))
    module.run()
    
else:
    # Importer et exécuter le script fichier3.py
    module = load_module('fichier3', os.path.join('scripts', 'fichier3.py'))
    module.run()
