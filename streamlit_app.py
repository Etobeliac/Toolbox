import streamlit as st
import os
import importlib.util

# Titre de l'application
st.title('Mon Application avec Dérouleurs')

# Barre latérale pour la navigation
st.sidebar.header('Menu')

# Dérouleur 1
option1 = st.sidebar.selectbox('G-News', ['Fichier 1', 'GPT Bulk', 'Fichier 3'])

if option1 == 'Fichier 1':
    st.write('Contenu du Fichier 1')
elif option1 == 'GPT Bulk':
    # Charger et exécuter le script gpt-bulk.py
    script_path = os.path.join('scripts', 'gpt-bulk.py')
    spec = importlib.util.spec_from_file_location("gpt_bulk", script_path)
    gpt_bulk = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gpt_bulk)
    gpt_bulk.run()  # Assurez-vous que gpt-bulk.py a une fonction run()
else:
    st.write('Contenu du Fichier 3')
