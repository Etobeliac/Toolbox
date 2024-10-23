import streamlit as st
import pandas as pd
import re
import io
import csv

# Regex pour détecter les balises <a> existantes et mettre à jour leur href
ancre_pattern = re.compile(r'(<a\s+[^>]*href=["\'][^"\']*["\'])([^>]*>.*?</a>)', re.IGNORECASE)

def update_existing_anchors(text, new_url):
    # Assurez-vous que le texte est une chaîne et qu'il n'est pas vide
    if not isinstance(text, str) or not text.strip():
        return text, "Erreur"

    # Fonction pour remplacer le lien href dans les balises <a>
    def replace_href(match):
        opening_tag, rest_of_tag = match.groups()
        # Mettre à jour uniquement le href sans changer l'ancre texte
        updated_tag = re.sub(r'href=["\'][^"\']*["\']', f'href="{new_url}"', opening_tag)
        return f"{updated_tag}{rest_of_tag}"

    # Appliquer la mise à jour des liens href dans les balises <a>
    modified_text = re.sub(ancre_pattern, replace_href, text)
    return modified_text, "OK"

def main():
    st.title("Détecteur et Modificateur d'Ancres avec Liens Personnalisés")

    # Exemple de données initiales pour le tableau
    data = {
        "Article": [
            '<p>Les ajustements de suspension sont cruciaux. <a href="#">Découvrez ici</a> pour en savoir plus.</p>'
        ] * 5,
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
                modified_text, status = update_existing_anchors(article, link)
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
