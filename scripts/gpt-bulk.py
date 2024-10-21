import streamlit as st
import pandas as pd
from openai import OpenAI

def run():
    st.header("GPT Bulk Processing")

    # Entrée pour la clé API OpenAI
    api_key = st.text_input("Entrez votre clé API OpenAI", type="password")

    # Sélection du modèle, avec l'ajout de "gpt-4o-mini"
    model_choice = st.selectbox("Choisissez le modèle", ["gpt-4", "gpt-4o-mini"])

    # Exemple de DataFrame vide que l'utilisateur peut éditer
    df = pd.DataFrame({
        'Prompt': [''],
        'Résultat': ['']
    })

    # Utiliser st.data_editor pour permettre l'édition directe
    edited_df = st.data_editor(df, num_rows="dynamic")

    if st.button("Traiter les prompts") and api_key:
        # Instantiate the OpenAI client
        client = OpenAI(api_key=api_key)
        
        for index, row in edited_df.iterrows():
            if row['Prompt']:
                try:
                    # Use the new client-based method for chat completions
                    response = client.chat.completions.create(
                        model=model_choice,
                        messages=[{"role": "user", "content": row['Prompt']}],
                        max_tokens=150
                    )
                    edited_df.at[index, 'Résultat'] = response.choices[0].message.content.strip()
                except Exception as e:
                    st.error(f"Erreur lors de l'appel à l'API : {e}")

    # Afficher le DataFrame avec les résultats mis à jour
    st.write(edited_df)

if __name__ == "__main__":
    run()
