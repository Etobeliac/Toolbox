import streamlit as st
import pandas as pd
import openai

def run():
    st.header("GPT Bulk Processing")

    # Entrée pour la clé API OpenAI
    api_key = st.text_input("Entrez votre clé API OpenAI", type="password")

    # Sélection du modèle
    model_choice = st.selectbox("Choisissez le modèle", ["gpt-4o", "gpt-4o-mini"])

    # Exemple de DataFrame avec des prompts
    df = pd.DataFrame({
        'Prompt': ['Quel est le sens de la vie?', 'Comment fonctionne une voiture?'],
        'Résultat': ['', '']
    })

    if st.button("Traiter les prompts") and api_key:
        openai.api_key = api_key
        for index, row in df.iterrows():
            if row['Prompt']:
                response = openai.Completion.create(
                    engine=model_choice,
                    prompt=row['Prompt'],
                    max_tokens=150
                )
                df.at[index, 'Résultat'] = response.choices[0].text.strip()

    # Afficher le DataFrame avec les résultats
    st.write(df)

if __name__ == "__main__":
    run()
