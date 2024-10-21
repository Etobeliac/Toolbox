import streamlit as st
import pandas as pd
import openai

def run():
    st.header("GPT Bulk Processing")

    # Entrée pour la clé API OpenAI
    api_key = st.text_input("Entrez votre clé API OpenAI", type="password")

    # Sélection du modèle
    model_choice = st.selectbox("Choisissez le modèle", ["gpt-4o", "gpt-4o-mini"])

    # Exemple de DataFrame vide que l'utilisateur peut éditer
    df = pd.DataFrame({
        'Prompt': [''],
        'Résultat': ['']
    })

    # Éditeur de données expérimental pour permettre l'édition directe
    edited_df = st.experimental_data_editor(df)

    if st.button("Traiter les prompts") and api_key:
        openai.api_key = api_key
        for index, row in edited_df.iterrows():
            if row['Prompt']:
                response = openai.Completion.create(
                    engine=model_choice,
                    prompt=row['Prompt'],
                    max_tokens=150
                )
                edited_df.at[index, 'Résultat'] = response.choices[0].text.strip()

    # Afficher le DataFrame avec les résultats mis à jour
    st.write(edited_df)

if __name__ == "__main__":
    run()
