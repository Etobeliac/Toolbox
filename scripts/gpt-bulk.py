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

    # Utiliser st.data_editor pour permettre l'édition directe
    edited_df = st.data_editor(df, num_rows="dynamic")

    if st.button("Traiter les prompts") and api_key:
        openai.api_key = api_key
        
        for index, row in edited_df.iterrows():
            if row['Prompt']:
                try:
                    response = openai.ChatCompletion.create(
                        model=model_choice,
                        messages=[{"role": "user", "content": row['Prompt']}],
                        max_tokens=150
                    )
                    edited_df.at[index, 'Résultat'] = response.choices[0].message['content'].strip()
                except Exception as e:
                    st.error(f"Erreur lors de l'appel à l'API : {e}")

    # Afficher le DataFrame avec les résultats mis à jour
    st.write(edited_df)

if __name__ == "__main__":
    run()
