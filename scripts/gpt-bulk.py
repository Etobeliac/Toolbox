import streamlit as st
import pandas as pd
import openai

def run():
    st.header("Traitement en masse GPT")

    # Configuration de l'API OpenAI (à remplacer par vos clés)
    openai.api_key = "votre_clé_api"  # Remplacez par votre clé API réelle
    model_engine = "text-davinci-003"  # Choisissez le modèle approprié

    # Création d'un DataFrame pour les prompts et les résultats
    df = pd.DataFrame({'Prompt': [], 'Résultat': []})

    # Zone d'édition pour les prompts
    edited_df = st.data_editor(df)

    # Bouton pour lancer le traitement
    if st.button("Traiter les prompts"):
        for index, row in edited_df.iterrows():
            prompt = row['Prompt']
            if prompt:
                try:
                    # Appel à l'API OpenAI
                    response = openai.Completion.create(
                        engine=model_engine,
                        prompt=prompt,
                        max_tokens=1024,
                        n=1,
                        stop=None,
                        temperature=0.7
                    )

                    # Récupération du résultat
                    result = response.choices[0].text.strip()
                    edited_df.at[index, 'Résultat'] = result

                except openai.error.APIError as e:
                    st.error(f"Erreur de l'API OpenAI : {e}")
                except Exception as e:
                    st.error(f"Erreur inattendue : {e}")

        # Mise à jour du DataFrame avec les nouveaux résultats
        st.data_editor(edited_df)

if __name__ == "__main__":
    run()
