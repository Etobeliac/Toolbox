import streamlit as st
import os

# Titre de l'application
st.title('Mon Toolbox')

# Barre latérale pour la navigation
options = ['Accueil'] + [f for f in os.listdir('scripts') if f.endswith('.py')]
selected_option = st.sidebar.selectbox('Choisissez un outil', options)

# Affichage en fonction de l'option sélectionnée
if selected_option == 'Accueil':
    st.write('Utilisez la barre latérale pour accéder aux différents outils.')
else:
    script_path = os.path.join('scripts', selected_option)
    if os.path.exists(script_path):
        with open(script_path) as f:
            exec(f.read())
    else:
        st.error(f"Le fichier {selected_option} n'existe pas.")
