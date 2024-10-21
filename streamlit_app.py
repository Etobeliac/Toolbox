import streamlit as st
import os

# Titre de l'application
st.title('Mon Toolbox')

# Barre latérale pour la navigation
options = ['Accueil'] + [f for f in os.listdir('scripts') if f.endswith('.py')]
selected_option = st.sidebar.selectbox('', options)

# Affichage en fonction de l'option sélectionnée
if selected_option == 'Accueil':
    st.write('Utilisez la barre latérale pour accéder aux différents outils.')
else:
    script_path = os.path.join('scripts', selected_option)
    with open(script_path) as f:
        exec(f.read())
# Barre latérale pour la navigation
options = ['G News'] + [f for f in os.listdir('scripts') if f.endswith('.py')]
selected_option = st.sidebar.selectbox('', options)
