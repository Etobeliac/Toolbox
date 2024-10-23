import streamlit as st
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
import io
import csv
import random
import re
import html

# Liste des ancres possibles
ancres = [
    "Voir la suite", "Continuer la lecture", "Poursuivre la lecture", "Aller plus loin",
    "Approfondir le sujet", "Découvrir plus en détail", "En savoir plus sur le sujet",
    "Plongez au cœur du sujet", "Découvrez tout ce qu'il faut savoir", "Lire l'intégralité de l'article",
    "Accéder à la ressource", "Consultez la page dédiée", "Visitez la page", "Cliquez pour en savoir plus",
    "Plus d'infos", "Informations", "Détails complets", "Voir tout", "Afficher plus",
    "Découvrir le contenu", "Explorer le sujet", "En apprendre plus sur ce thème",
    "Tout savoir sur ce sujet", "Comprendre le sujet", "Analyse approfondie", "Décryptage",
    "Point de vue", "Perspective", "Avis d'expert", "Conseils d'expert", "Ressources utiles",
    "Liens utiles", "Documentation", "Références", "Astuces et conseils", "Trucs et astuces",
    "Bonnes pratiques", "Meilleures pratiques", "Guide complet", "Tutoriel", "FAQ",
    "Questions fréquentes", "Assistance", "Support", "Aide", "Contactez l'équipe",
    "Nous joindre", "Demander de l'aide", "Obtenir de l'aide", "Soumettre une question",
    "Poser une question à l'expert", "Participer à la discussion", "Rejoindre la conversation",
    "Partager votre avis", "Laisser un commentaire", "Donner votre feedback", "Votre opinion nous intéresse",
    "Témoignages", "Ce qu'ils en disent", "Avis clients", "Voir les avis", "Lire les témoignages",
    "Partagez votre expérience", "Expériences", "Retour d'expérience", "Cas client",
    "Exemples concrets", "Études de cas", "Success stories", "Histoires de réussite", "Inspiration",
    "Idées", "Solutions", "Innovations", "Actualités", "Nouveautés", "Dernières nouvelles",
    "À la une", "En direct", "Tendances", "Tendances actuelles", "Le meilleur de",
    "Sélection", "Choix de la rédaction", "Coup de cœur", "Recommandations", "Suggestions",
    "Conseils personnalisés", "Offres spéciales", "Promotions", "Exclusivités", "Bons plans",
    "Codes promo", "Réductions", "Meilleures offres", "Ventes flash", "Découvrir les offres",
    "Profiter des offres", "Bénéficier des offres", "S'inscrire à la newsletter", "Recevoir les actualités"
    # Ajoutez-en d'autres si nécessaire
]


@st.cache_data(ttl=3600)  # Cache les résultats pendant 1 heure
def get_draft_urls_and_content(username, password, base_url):
    url = f"{base_url}/wp-json/wp/v2/posts?status=draft&per_page=100"
    all_posts = []
    page = 1
    
    while True:
        page_url = f"{url}&page={page}"
        response = requests.get(page_url, auth=HTTPBasicAuth(username, password))
        
        if response.status_code != 200:
            break
        
        posts = response.json()
        if not posts:
            break
        
        all_posts.extend(posts)
        page += 1

    urls_and_content = []
    for post in all_posts:
        categories = []
        if 'categories' in post:
            categories_ids = post['categories']
            for category_id in categories_ids:
                category_response = requests.get(f"{base_url}/wp-json/wp/v2/categories/{category_id}", auth=HTTPBasicAuth(username, password))
                if category_response.status_code == 200:
                    category_name = category_response.json().get('name', '')
                    categories.append(category_name)
        
        content_html = post.get('content', {}).get('rendered', '')
        content_html = html.unescape(content_html)  # Décodage des entités HTML
        
        # Ajouter l'insertion d'ancre ici
        modified_content = insert_anchor(content_html)
        
        urls_and_content.append({
            'URL du site': base_url,
            'URL du brouillon': post['link'],
            'Thématique': ', '.join(categories),
            'Contenu': content_html,
            'Contenu modifié': modified_content
        })

    return urls_and_content

def insert_anchor(content):
    # Diviser le contenu en paragraphes
    paragraphs = re.split(r'(?<=</p>)\s*(?=<p>)', content)
    
    if len(paragraphs) > 1:
        # Choisir aléatoirement un paragraphe (sauf le dernier)
        insert_index = random.randint(0, len(paragraphs) - 2)
        
        # Choisir une ancre aléatoire
        anchor = random.choice(ancres)
        
        # Insérer l'ancre à la fin du paragraphe choisi
        paragraphs[insert_index] = paragraphs[insert_index][:-4] + f' <a href="#">{anchor}</a></p>'
        
        # Rejoindre les paragraphes
        return ''.join(paragraphs)
    else:
        # Si un seul paragraphe, ajouter l'ancre à la fin
        anchor = random.choice(ancres)
        return content[:-4] + f' <a href="#">{anchor}</a></p>'

def scrap_brouillon_site():
    st.title("Récupérateur d'URLs et Contenu des Articles en Brouillon WordPress")

    username = st.text_input("Nom d'utilisateur WordPress")
    password = st.text_input("Mot de passe WordPress", type="password")
    base_urls = st.text_area("URLs de base de vos sites WordPress (une par ligne)")

    if st.button("Récupérer les URLs et le Contenu"):
        if not username or not password or not base_urls:
            st.error("Veuillez remplir tous les champs.")
        else:
            base_urls_list = [url.strip() for url in base_urls.split("\n") if url.strip()]
            all_data = []
            progress_bar = st.progress(0)

            for i, base_url in enumerate(base_urls_list):
                st.write(f"Traitement du site : {base_url}")
                
                data = get_draft_urls_and_content(username, password, base_url)
                if data:
                    all_data.extend(data)
                    st.write(f"Nombre d'articles trouvés pour {base_url}: {len(data)}")
                else:
                    st.write(f"Aucun article trouvé pour {base_url}")
                
                progress_bar.progress((i + 1) / len(base_urls_list))

            st.success("Récupération terminée.")

            if all_data:
                st.success(f"Articles en brouillon récupérés avec succès. Total: {len(all_data)} articles.")
                
                df = pd.DataFrame(all_data)
                st.write("Aperçu des données récupérées (avec un extrait du contenu) :")
                preview_df = df[['URL du site', 'URL du brouillon', 'Thématique', 'Contenu', 'Contenu modifié']].head(10).copy()
                preview_df['Contenu'] = preview_df['Contenu'].str[:100] + '...'
                preview_df['Contenu modifié'] = preview_df['Contenu modifié'].str[:100] + '...'
                st.write(preview_df)

                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False, quoting=csv.QUOTE_ALL, encoding='utf-8-sig', sep=';')
                csv_data = csv_buffer.getvalue()
                
                st.download_button(
                    label="Télécharger tous les résultats (CSV)",
                    data=csv_data.encode('utf-8-sig'),
                    file_name="articles_brouillons.csv",
                    mime="text/csv"
                )
            else:
                st.info("Aucun article en brouillon trouvé.")

    if st.button("Réinitialiser"):
        st.experimental_rerun()
