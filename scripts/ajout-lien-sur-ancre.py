# ajout-lien-sur-ancre.py

import streamlit as st
import pandas as pd
import re
import io
import csv
import random
import html

# Liste des ancres possibles (identique à celle fournie dans votre code)
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

def insert_anchor(content, new_link):
    """
    Insère aléatoirement une ancre dans le contenu avec le lien fourni.
    """
    paragraphs = re.split(r'(?<=</p>)\s*(?=<p>)', content)

    if len(paragraphs) > 1:
        insert_index = random.randint(0, len(paragraphs) - 2)
        anchor = random.choice(ancres)
        paragraphs[insert_index] = paragraphs[insert_index][:-4] + f' <a href="{new_link}">{anchor}</a></p>'
        return ''.join(paragraphs)
    else:
        anchor = random.choice(ancres)
        return content[:-4] + f' <a href="{new_link}">{anchor}</a></p>'

def main():
    st.title("Ajout de Liens sur les Ancres Présentes")
    st.write("Fonctionnalité pour insérer des liens sur les ancres aléatoires dans les articles.")
    
    # Exemple simple pour montrer comment la fonction fonctionne
    content = "<p>Ceci est un paragraphe test.</p><p>Un autre paragraphe test.</p>"
    new_link = "https://votre-lien.com"
    modified_content = insert_anchor(content, new_link)
    
    st.write("Avant :")
    st.write(content)
    st.write("Après :")
    st.write(modified_content)

if __name__ == "__main__":
    main()
