import streamlit as st
import pandas as pd
import re

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

# Crée un motif de regex pour détecter les ancres possibles
ancre_pattern = re.compile(r'\b(' + '|'.join(re.escape(ancre) for ancre in ancres) + r')\b', re.IGNORECASE)

def detect_and_modify_anchors(text):
    # Trouver toutes les ancres dans le texte
    matches = ancre_pattern.findall(text)
    
    # Si aucune ancre n'est trouvée, retourner une erreur
    if not matches:
        return text, "Erreur"
    
    # Remplacer les ancres trouvées par des liens HTML
    modified_text = re.sub(ancre_pattern, r'<a href="#">\1</a>', text)
    return modified_text, "OK"

def main():
    st.title("Détecteur et Modificateur d'Ancres dans les Articles")

    # Zone de texte pour coller des articles
    articles_input = st.text_area("Collez vos articles ici (un par ligne)", height=300)
    
    if st.button("Traiter les Articles"):
        if not articles_input:
            st.error("Veuillez entrer au moins un article.")
        else:
            # Diviser les articles en lignes
            articles_list = articles_input.split("\n")
            
            # Créer des listes pour stocker les résultats
            original_texts = []
            modified_texts = []
            statuses = []
            
            # Traiter chaque article
            for article in articles_list:
                modified_text, status = detect_and_modify_anchors(article)
                original_texts.append(article)
                modified_texts.append(modified_text)
                statuses.append(status)
            
            # Créer un DataFrame avec les résultats
            df = pd.DataFrame({
                "Article Original": original_texts,
                "Article Modifié (avec liens)": modified_texts,
                "Statut": statuses
            })
            
            # Afficher le DataFrame sur Streamlit
            st.write("Résultats de la détection et de la modification des ancres :")
            st.dataframe(df)

            # Option de téléchargement en CSV
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
            st.download_button(
                label="Télécharger les résultats (CSV)",
                data=csv_buffer.getvalue().encode('utf-8-sig'),
                file_name="resultats_ancres.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()
