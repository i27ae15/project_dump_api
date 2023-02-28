import os
import time


import openai


from gameplay.models.models import StoryTopic


from dotenv import load_dotenv
load_dotenv()


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def clean_options(options:list[str]) -> list[str]:
    for i, option in enumerate(options):
        option = option.replace('"', '').replace('\n', '')
        options[i] = option
    return options


def generate_options(options_to_generate:int, topic:StoryTopic) -> list[str]:
    openai.api_key = OPENAI_API_KEY
    current_options = []

    if topic: 
        prompt = f'Genera una frase aleatoria, de no mas de 5 palabras, con temática de {topic.spanish_name}, \
            no te preocupes por la gramática, solo por la temática.'
    else:
        prompt = 'Genera una frase aleatoria, de no mas de 5 palabras, con temática aleatoria.'
        
    for _ in range(options_to_generate):
        response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=0.8, max_tokens=256)
        current_options.append(response['choices'][0]['text'])
    
    return clean_options(current_options)
