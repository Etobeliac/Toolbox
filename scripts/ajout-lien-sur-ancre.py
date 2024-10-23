import streamlit as st
import pandas as pd
import random
import re
import io

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
]

def insert_anchor_randomly(content, anchor_html):
    # Diviser le contenu en paragraphes
    paragraphs = content.split("</p>")
    if len(paragraphs) > 1:
        # Choisir aléatoirement un paragraphe pour ajouter l'ancre
        insert_index = random.randint(0, len(paragraphs) - 2)
        paragraphs[insert_index] += f" {anchor_html}"
    return "</p>".join(paragraphs)

def format_anchor(url, text):
    # Créer une ancre avec le lien et le texte fourni
    return f'<a href={url}>{text}</a>'

def main():
    st.title("Ajout Automatique de Liens sur Ancres dans les Articles")
    
    # Exemple de données initiales pour le tableau
    data = {
        "Article": ["Collez ou modifiez votre article ici..."] * 3,
        "Lien": ["https://votre-lien.com"] * 3
    }

    # Créer un DataFrame à partir des données initiales
    df = pd.DataFrame(data)

    # Afficher et permettre l'édition du tableau
    st.write("Remplissez le tableau ci-dessous avec vos articles et les liens correspondants :")
    edited_df = st.experimental_data_editor(df, num_rows="dynamic", key="editor")

    if st.button("Traiter les Articles"):
        if edited_df.empty:
            st.error("Veuillez entrer au moins un article et un lien.")
        else:
            # Créer des listes pour stocker les résultats
            original_texts = []
            modified_texts = []
            links = []

            # Traiter chaque article
            for _, row in edited_df.iterrows():
                article = row["Article"]
                link = row["Lien"]

                # Choisir une ancre aléatoire
                random_anchor_text = random.choice(ancres)

                # Créer l'ancre HTML avec le lien fourni
                formatted_anchor = format_anchor(link, random_anchor_text)

                # Ajouter l'ancre dans un paragraphe aléatoire
                modified_article = insert_anchor_randomly(article, formatted_anchor)

                original_texts.append(article)
                modified_texts.append(modified_article)
                links.append(link)

            # Créer un DataFrame avec les résultats
            results_df = pd.DataFrame({
                "Article Original": original_texts,
                "Lien": links,
                "Article Modifié (avec liens)": modified_texts
            })

            # Afficher le DataFrame sur Streamlit
            st.write("Résultats de la détection et de la modification des ancres :")
            st.dataframe(results_df)

            # Option de téléchargement en CSV
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
