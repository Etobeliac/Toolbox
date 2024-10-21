import streamlit as st
import os

# Titre de l'application
st.title('Mon Application avec Dérouleurs')

# Barre latérale pour la navigation
st.sidebar.header('Menu')

# Dérouleur 1
option1 = st.sidebar.selectbox('G-News', ['Fichier 1', 'GPT Bulk', 'Fichier 3'])

if option1 == 'Fichier 1':
    # Importer et exécuter le script fichier1.py
    import fichier1
    fichier1.run()
elif option1 == 'GPT Bulk':
    # Importer et exécuter le script gpt_bulk.py
    import gpt_bulk
    gpt_bulk.run()
else:
    # Importer et exécuter le script fichier3.py
    import fichier3
    fichier3.run()
