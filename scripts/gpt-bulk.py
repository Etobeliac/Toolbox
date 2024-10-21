import openai

def gpt_bulk(prompt, model="text-davinci-003", max_tokens=1024, temperature=0.7):
    """
    Génère du texte à partir d'un prompt en utilisant l'API OpenAI.

    Args:
        prompt (str): Le prompt à utiliser pour la génération de texte.
        model (str, optional): Le modèle GPT à utiliser. Defaults to "text-davinci-003".
        max_tokens (int, optional): Le nombre maximum de tokens dans la réponse. Defaults to 1024.
        temperature (float, optional): Le paramètre de température pour contrôler la créativité. Defaults to 0.7.

    Returns:
        str: Le texte généré.
    """

    try:
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=temperature
        )
        return response.choices[0].text.strip()
    except openai.error.APIError as e:
        print(f"Erreur de l'API OpenAI : {e}")
        return None
