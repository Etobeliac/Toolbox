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

        # Vérifier s'il y a une image à télécharger
        image_id = None
        if isinstance(image_url, str) and image_url.startswith(('http://', 'https://')):
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
                else:
                    print(f"Erreur lors du téléchargement de l'image : {image_response.text}")

                # Supprimer le fichier local après l'upload
                os.remove(image_path)

        # Publier l'article via l'API REST (avec ou sans image)
        response = publish_post_via_rest_api(url, username, app_password, title, content, image_id, status, date)

        if response.status_code == 201:
            print(f"Article '{title}' publié/planifié avec succès ! ID de l'article : {response.json()['id']}")
        else:
            print(f"Erreur lors de la publication de l'article '{title}': {response.text}")
