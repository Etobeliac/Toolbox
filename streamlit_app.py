import streamlit as st
import importlib.util
import os

# Titre de l'application
st.title('Mon Application avec Dérouleurs')

# Barre latérale pour la navigation
st.sidebar.header('Menu')

# Dérouleur 1
option1 = st.sidebar.selectbox('G-News', ['Fichier 1', 'GPT Bulk', 'Fichier 3'])

def load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

if option1 == 'Fichier 1':
    # Importer et exécuter le script fichier1.py
    module = load_module('fichier1', os.path.join('scripts', 'fichier1.py'))
    module.run()
elif option1 == 'GPT Bulk':
    # Importer et exécuter le script gpt-bulk.py
    module = load_module('gpt_bulk', os.path.join('scripts', 'gpt-bulk.py'))
    module.run()
else:
    # Importer et exécuter le script fichier3.py
    module = load_module('fichier3', os.path.join('scripts', 'fichier3.py'))
    module.run()
