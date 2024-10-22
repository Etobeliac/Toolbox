import pandas as pd
import requests
from datetime import datetime
import os
import streamlit as st

# Dossier pour les images
local_image_folder = 'images'

# Créer le dossier s'il n'existe pas
if not os.path.exists(local_image_folder):
    os.makedirs(local_image_folder)

# Fonction pour télécharger l'image à partir d'une URL
def download_image(image_url, local_folder, file_name):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        local_path = os.path.join(local_folder, file_name)
        with open(local_path, 'wb') as file:
            file.write(response.content)
        return local_path
    except requests.RequestException as e:
        st.error(f"Erreur lors du téléchargement de l'image : {e}")
        return None

# Fonction pour télécharger l'image sur WordPress
def upload_image(url, username, app_password, image_path, alt_text):
    try:
        headers = {
            'Content-Disposition': f'attachment; filename={os.path.basename(image_path)}',
        }
        files = {
            'file': open(image_path, 'rb'),
            'alt_text': (None, alt_text)
        }
        response = requests.post(
            f"{url}/wp-json/wp/v2/media",
            headers=headers,
            files=files,
            auth=(username, app_password)
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erreur lors de l'upload de l'image sur WordPress : {e}")
        return None

# Fonction pour publier via l'API REST
def publish_post_via_rest_api(url, username, app_password, title, content, image_id=None, status='draft', date=None):
    try:
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            'title': title,
            'content': content,
            'status': status,
            'date': date,
        }
        # Ajouter l'image uniquement si image_id est présent
        if image_id is not None:
            data['featured_media'] = image_id

        response = requests.post(
            f"{url}/wp-json/wp/v2/posts",
            headers=headers,
            json=data,
            auth=(username, app_password)
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erreur lors de la publication de l'article : {e}")
        return None

# Fonction principale pour Streamlit
def publish_articles():
    st.title("Publication d'Articles sur WordPress")

    # Éditeur de tableau pour les informations de sites
    st.subheader("Informations des Sites")
    site_columns = ['URL', 'ID', 'Mot de passe d\'application']
    site_data = pd.DataFrame(columns=site_columns)
    edited_sites = st.data_editor(site_data, num_rows="dynamic", key="site_editor")

    # Éditeur de tableau pour les informations des articles
    st.subheader("Informations des Articles")
    article_columns = ['Titre', 'Contenu HTML', 'Feature image', 'DATE DE PUBLICATION']
    article_data = pd.DataFrame(columns=article_columns)
    edited_articles = st.data_editor(article_data, num_rows="dynamic", key="article_editor")

    # Bouton pour publier les articles
    if st.button("Publier les Articles"):
        # Parcourir chaque ligne du tableau de sites
        for _, site_row in edited_sites.iterrows():
            url = site_row['URL'].rstrip('/')
            username = site_row['ID']
            app_password = site_row['Mot de passe d\'application']

            # Date actuelle
            current_date = pd.to_datetime('today').date()

            # Parcourir chaque article pour publier
            for _, article_row in edited_articles.iterrows():
                post_date = pd.to_datetime(article_row['DATE DE PUBLICATION']).date()

                # Préparer les données de l'article
                title = article_row['Titre']
                content = article_row['Contenu HTML']
                image_url = article_row['Feature image']
                status = 'publish' if post_date <= current_date else 'future'
                date = post_date.strftime('%Y-%m-%dT%H:%M:%S')

                # Utiliser le titre de l'article pour le nom de fichier et le texte alternatif
                file_name = f"{title.replace('/', '-')}.jpg"
                alt_text = title

                image_id = None

                # Télécharger et uploader l'image seulement si une URL est fournie
                if image_url:
                    image_path = download_image(image_url, local_image_folder, file_name)
                    if image_path:
                        image_response = upload_image(url, username, app_password, image_path, alt_text)
                        if image_response:
                            image_id = image_response.get('id')
                            new_image_url = image_response.get('source_url')
                            st.write(f"Image téléchargée avec succès ! ID de l'image : {image_id}")

                            # Remplacer l'ancienne URL de l'image par la nouvelle URL interne
                            content = content.replace(image_url, new_image_url)
                        else:
                            st.error(f"Erreur lors de l'upload de l'image pour l'article '{title}'")

                        # Supprimer le fichier local après l'upload
                        os.remove(image_path)

                # Publier l'article via l'API REST, avec ou sans image
                post_response = publish_post_via_rest_api(url, username, app_password, title, content, image_id, status, date)

                if post_response:
                    st.success(f"Article '{title}' publié/planifié avec succès ! ID de l'article : {post_response.get('id')}")
                else:
                    st.error(f"Erreur lors de la publication de l'article '{title}'")
