import streamlit as st
import importlib

# Titre de l'application
st.title('Mon Application avec Dérouleurs')

# Barre latérale pour la navigation
st.sidebar.header('Menu')

# Dérouleur 1
option1 = st.sidebar.selectbox('G-News', ['Fichier 1', 'GPT Bulk', 'Fichier 3'])

if option1 == 'Fichier 1':
    # Importer et exécuter le script fichier1.py
    module = importlib.import_module('scripts.fichier1')
    module.run()
elif option1 == 'GPT Bulk':
    # Importer et exécuter le script gpt_bulk.py
    module = importlib.import_module('scripts.gpt_bulk')
    module.run()
else:
    # Importer et exécuter le script fichier3.py
    module = importlib.import_module('scripts.fichier3')
    module.run()
