import streamlit as st
import pandas as pd
import io
import csv
from bs4 import BeautifulSoup

def update_anchor_href(text, new_url):
    # Assurez-vous que le texte est une chaîne et qu'il n'est pas vide
    if not isinstance(text, str) or not text.strip():
        return text, "Erreur"

    # Utiliser BeautifulSoup pour parser le HTML et modifier les href
    soup = BeautifulSoup(text, "html.parser")
    modified = False

    # Trouver toutes les balises <a> et modifier celles avec href="#"
    for a_tag in soup.find_all("a", href="#"):
        a_tag['href'] = new_url
        modified = True

    if modified:
        return str(soup), "OK"
    else:
        return text, "Erreur"

def main():
    st.title("Détecteur et Modificateur d'Ancres avec Liens Personnalisés")

    # Exemple de données initiales pour le tableau
    data = {
        "Article": [
            '<p>Les ajustements de suspension sont cruciaux. <a href="#">Découvrez ici</a> pour en savoir plus.</p>',
            '<p>Le design influence l’expérience. <a href="#">En savoir plus ici</a>.</p>'
        ],
        "Lien": ["https://nouveau-lien.com", "https://votre-lien.com"]
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
                modified_text, status = update_anchor_href(article, link)
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
