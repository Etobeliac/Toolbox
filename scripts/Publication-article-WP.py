# scripts/Publication-article-WP.py

import pandas as pd
import requests
from datetime import datetime
import os

# Chemin vers les fichiers Excel
file_sites = r'C:\Users\celes\OneDrive\Bureau\PYTHON SCRIPT\SCRIPT AUTOMATIQUE HOMEMADE\Liste_sites_PBN.xlsx'
file_articles = r'C:\Users\celes\OneDrive\Bureau\PYTHON SCRIPT\SCRIPT AUTOMATIQUE HOMEMADE\Historique.xlsx'
local_image_folder = r'C:\Users\celes\OneDrive\Bureau\PYTHON SCRIPT\SCRIPT AUTOMATIQUE HOMEMADE\image'

# Créer le dossier s'il n'existe pas
if not os.path.exists(local_image_folder):
    os.makedirs(local_image_folder)

# Lire les fichiers Excel
df_sites = pd.read_excel(file_sites)

try:
    df_articles = pd.read_excel(file_articles)
    if 'Feature image' not in df_articles.columns:
        raise KeyError("La colonne 'Feature image' est manquante dans le fichier Excel.")
except Exception as e:
    print(f"Erreur lors de la lecture du fichier Excel : {e}")
    exit()

# Fonction pour télécharger l'image à partir d'une URL
def download_image(image_url, local_folder, file_name):
    response = requests.get(image_url)
    if response.status_code == 200:
        local_path = os.path.join(local_folder, file_name)
        with open(local_path, 'wb') as file:
            file.write(response.content)
        return local_path
    else:
        print(f"Erreur lors du téléchargement de l'image : {response.status_code}")
        return None

# Fonction pour télécharger l'image sur WordPress
def upload_image(url, username, app_password, image_path, alt_text):
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
    return response

# Fonction pour publier via l'API REST
def publish_post_via_rest_api(url, username, app_password, title, content, image_id, status='draft', date=None):
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'title': title,
        'content': content,
        'status': status,
        'date': date,
        'featured_media': image_id
    }
    response = requests.post(
        f"{url}/wp-json/wp/v2/posts",
        headers=headers,
        json=data,
        auth=(username, app_password)
    )
    return response

# Fonction principale à appeler depuis Streamlit
def publish_articles():
    # Parcourir chaque ligne du fichier Excel pour les sites
    for index, site_row in df_sites.iterrows():
        url = site_row['URL'].rstrip('/')
        username = site_row['ID']
        app_password = '1kBF ex6l 8c73 hVLk AF8y 8Pdz'  # Utilisez le mot de passe d'application ici

        print(f"Connexion à {url} avec l'utilisateur {username}.")

        # Date actuelle
        current_date = pd.to_datetime('today').date()

        # Parcourir chaque article pour publier
        for _, article_row in df_articles.iterrows():
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

            # Télécharger l'image à partir de l'URL
            image_path = download_image(image_url, local_image_folder, file_name)
            if image_path:
                # Télécharger l'image sur WordPress
                image_response = upload_image(url, username, app_password, image_path, alt_text)
                if image_response.status_code == 201:
                    image_id = image_response.json()['id']
                    new_image_url = image_response.json()['source_url']
                    print(f"Image téléchargée avec succès ! ID de l'image : {image_id}")

                    # Remplacer l'ancienne URL de l'image par la nouvelle URL interne
                    content = content.replace(image_url, new_image_url)

                    # Publier l'article via l'API REST
                    response = publish_post_via_rest_api(url, username, app_password, title, content, image_id, status, date)

                    if response.status_code == 201:
                        print(f"Article '{title}' publié/planifié avec succès ! ID de l'article : {response.json()['id']}")
                    else:
                        print(f"Erreur lors de la publication de l'article '{title}': {response.text}")
                else:
                    print(f"Erreur lors du téléchargement de l'image : {image_response.text}")

                # Supprimer le fichier local après l'upload
                os.remove(image_path)

