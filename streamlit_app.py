import streamlit as st
import os
import importlib.util

# Titre de l'application
st.title('Mon Toolbox')

# Barre latérale pour la navigation
options = ['Accueil'] + [f for f in os.listdir('scripts') if f.endswith('.py')]
selected_option = st.sidebar.selectbox('Choisissez un outil', options)

# Affichage en fonction de l'option sélectionnée
if selected_option == 'Accueil':
    st.write('Utilisez la barre latérale pour accéder aux différents outils.')
else:
    module_name = selected_option.replace('.py', '')
    spec = importlib.util.spec_from_file_location(module_name, os.path.join('scripts', selected_option))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.run()
