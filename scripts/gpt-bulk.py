import streamlit as st
import pandas as pd
import openai

# Créer un DataFrame vide avec deux colonnes: 'Prompt' et 'Résultat'
df = pd.DataFrame(columns=['Prompt', 'Résultat'])

# Interface utilisateur
st.title("GPT Bulk Processing")

# Entrée pour la clé API OpenAI
api_key = st.text_input("Entrez votre clé API OpenAI", type="password")

# Sélection du modèle
model_choice = st.selectbox("Choisissez le modèle", ["gpt-4o", "gpt-4o-mini"])

# Boutons pour ajouter un prompt et traiter les prompts
if st.button("Ajouter un prompt"):
    df = df.append({'Prompt': '', 'Résultat': ''}, ignore_index=True)

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

# Afficher le DataFrame sous forme de table éditable
edited_df = st.experimental_data_editor(df)

# Mettre à jour le DataFrame avec les modifications de l'utilisateur
df.update(edited_df)
