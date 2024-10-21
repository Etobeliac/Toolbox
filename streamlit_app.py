import streamlit as st
import importlib.util
import os

# Titre de l'application
st.title('Mon Application avec Dérouleurs')

# Barre latérale pour la navigation
st.sidebar.header('Menu')

# Dérouleur 1 - Ajouter l'option "Tutoriel"
option1 = st.sidebar.selectbox(
    'G-News', 
    ['Tutoriel', 'Scrap URL brouillon WP', 'GPT Bulk', 'Publication Article WP']
)

def load_module(module_name, file_path):
    if not os.path.isfile(file_path):
        st.error(f"Le fichier {file_path} est introuvable. Veuillez vérifier le chemin.")
        return None
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

if option1 == 'Tutoriel':
    # Afficher un tutoriel ou des explications
    st.header("Tutoriel - Guide d'Utilisation")
    st.write("""
    **Bienvenue dans l'application !**
    
    Cette application vous permet de réaliser différentes tâches via des scripts automatisés :
    
    1. **Scrap URL brouillon WP** : Récupère les URL et contenus des articles brouillons depuis votre site WordPress.
    2. **GPT Bulk** : Effectue du traitement de texte en masse via OpenAI GPT.
    3. **Publication Article WP** : Publie des articles sur vos sites WordPress directement à partir de données que vous fournissez.
    
    ### Comment Utiliser :
    
    - Sélectionnez l'option souhaitée dans le menu latéral pour accéder à la fonctionnalité correspondante.
    - Pour chaque fonctionnalité, vous pouvez entrer les informations nécessaires et lancer le processus.
    - Assurez-vous de remplir toutes les informations requises, surtout pour la publication d'articles.
    
    *Pour toute question supplémentaire, n'hésitez pas à contacter notre équipe de support.*
    """)

elif option1 == 'Scrap URL brouillon WP':
    # Chemin relatif au fichier scrap-url-brouillon-wp.py
    file_path = os.path.join('scripts', 'scrap-url-brouillon-wp.py')
    module = load_module('scrap_url_brouillon_wp', file_path)
    if module:
        module.scrap_brouillon_site()

elif option1 == 'GPT Bulk':
    # Importer et exécuter le script gpt-bulk.py
    file_path = os.path.join('scripts', 'gpt-bulk.py')
    module = load_module('gpt_bulk', file_path)
    if module:
        module.run()

elif option1 == 'Publication Article WP':
    # Importer et exécuter le script Publication-article-WP.py
    file_path = os.path.join('scripts', 'Publication-article-WP.py')
    module = load_module('publication_article_wp', file_path)
    if module:
        module.publish_articles()
