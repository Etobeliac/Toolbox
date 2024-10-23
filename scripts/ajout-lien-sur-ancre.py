import streamlit as st
import pandas as pd
import re
import io
import csv

# Liste des ancres possibles
ancres = [
    "Voir la suite", "Continuer la lecture", "Poursuivre la lecture", "Aller plus loin",
    "Approfondir le sujet", "Découvrir plus en détail", "En savoir plus sur le sujet",
    "Plongez au cœur du sujet", "Découvrez tout ce qu'il faut savoir", "Lire l'intégralité de l'article",
    "Accéder à la ressource", "Consultez la page dédiée", "Visitez la page", "Cliquez pour en savoir plus",
    "Plus d'infos", "Informations", "Détails complets", "Voir tout", "Afficher plus", "Découvrir le contenu",
    "Explorer le sujet", "En apprendre plus sur ce thème", "Tout savoir sur ce sujet", "Comprendre le sujet",
    "Analyse approfondie", "Décryptage", "Point de vue", "Perspective", "Avis d'expert", "Conseils d'expert",
    "Ressources utiles", "Liens utiles", "Documentation", "Références", "Astuces et conseils", "Trucs et astuces",
    "Bonnes pratiques", "Meilleures pratiques", "Guide complet", "Tutoriel", "FAQ", "Questions fréquentes",
    "Assistance", "Support", "Aide", "Contactez l'équipe", "Nous joindre", "Demander de l'aide", "Obtenir de l'aide",
    "Soumettre une question", "Poser une question à l'expert", "Participer à la discussion", "Rejoindre la conversation",
    "Partager votre avis", "Laisser un commentaire", "Donner votre feedback", "Votre opinion nous intéresse",
    "Témoignages", "Ce qu'ils en disent", "Avis clients", "Voir les avis", "Lire les témoignages",
    "Partagez votre expérience", "Expériences", "Retour d'expérience", "Cas client", "Exemples concrets",
    "Études de cas", "Success stories", "Histoires de réussite", "Inspiration", "Idées", "Solutions", "Innovations",
    "Actualités", "Nouveautés", "Dernières nouvelles", "À la une", "En direct", "Tendances", "Tendances actuelles",
    "Le meilleur de", "Sélection", "Choix de la rédaction", "Coup de cœur", "Recommandations", "Suggestions",
    "Conseils personnalisés", "Offres spéciales", "Promotions", "Exclusivités", "Bons plans", "Codes promo",
    "Réductions", "Meilleures offres", "Ventes flash", "Découvrir les offres", "Profiter des offres",
    "Bénéficier des offres", "S'inscrire à la newsletter", "Recevoir les actualités"
]

# Crée un motif de regex pour détecter les balises <a> avec des ancres existantes
ancre_pattern = re.compile(
    r'(<a\s+[^>]*href=["\'].*?["\'][^>]*>)(.*?)</a>',
    re.IGNORECASE
)

def detect_and_update_anchors(text, url):
    # Vérifier si le texte est une chaîne valide et non vide
    if not isinstance(text, str) or not text.strip():
        return text, "Erreur"

    # Fonction pour remplacer le lien des ancres existantes
    def replace_href(match):
        opening_tag = match.group(1)
        anchor_text = match.group(2)

        # Vérifier si l'ancre correspond à notre liste d'ancres définies
        if any(re.fullmatch(re.escape(a), anchor_text, re.IGNORECASE) for a in ancres):
            # Mettre à jour le href de l'ancre existante avec le lien fourni
            updated_tag = re.sub(r'href=["\'].*?["\']', f'href="{url}"', opening_tag)
            return f"{updated_tag}{anchor_text}</a>"
        else:
            # Si le texte d'ancre ne correspond pas, ne pas modifier
            return match.group(0)

    # Appliquer la mise à jour des ancres dans le texte
    modified_text = re.sub(ancre_pattern, replace_href, text)
    return modified_text, "OK"

def main():
    st.title("Détecteur et Modificateur d'Ancres avec Liens Personnalisés")

    # Exemple de données initiales pour le tableau
    data = {
        "Article": ["Collez ou modifiez votre article ici..."] * 5,
        "Lien": ["https://votre-lien.com"] * 5
    }

    # Créer un DataFrame à partir des données initiales
    df = pd.DataFrame(data)

    # Afficher et permettre l'édition du tableau
    st.write("Remplissez le tableau ci-dessous avec vos articles et les liens correspondants :")
    edited_df = st.data_editor(df, num_rows="dynamic", key="editor")

    if st.button("Traiter les Articles"):
        if edited_df.empty:
            st.error("Veuillez entrer au moins un article et un lien.")
        else:
            # Créer des listes pour stocker les résultats
            original_texts = []
            modified_texts = []
            links = []
            statuses = []

            # Traiter chaque article
            for _, row in edited_df.iterrows():
                article = row["Article"]
                link = row["Lien"]
                modified_text, status = detect_and_update_anchors(article, link)
                original_texts.append(article)
                modified_texts.append(modified_text)
                links.append(link)
                statuses.append(status)

            # Créer un DataFrame avec les résultats
            results_df = pd.DataFrame({
                "Article Original": original_texts,
                "Lien": links,
                "Article Modifié (avec liens)": modified_texts,
                "Statut": statuses
            })

            # Afficher le DataFrame sur Streamlit
            st.write("Résultats de la détection et de la modification des ancres :")
            st.dataframe(results_df)

            # Option de téléchargement en CSV avec encodage correct et délimitation par point-virgule
            csv_buffer = io.StringIO()
            results_df.to_csv(csv_buffer, index=False, encoding='utf-8-sig', sep=';', quoting=csv.QUOTE_ALL)
            st.download_button(
                label="Télécharger les résultats (CSV)",
                data=csv_buffer.getvalue().encode('utf-8-sig'),
                file_name="resultats_ancres.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()
