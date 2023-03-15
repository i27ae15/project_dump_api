import os
import openai


from gameplay.models.models import StoryTopic


from dotenv import load_dotenv
load_dotenv()


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class PhraseGenerator:

    openai.api_key = OPENAI_API_KEY
    conversation = list()

    def __init__(self, topic:StoryTopic) -> None:
        self._topic = topic
        self._system_role = None

        if self._topic:
            self._system_role = f'Eres un generador de frases aleatorias con el tópico de "{self._topic.spanish_name}", \
            las frases que generes deben ser divertidas pero cortas, no mas de 5 palabras'
        else:
            self._system_role = 'Eres un generador de frases aleatorias con temática aleatoria, \
            las frases que generes deben ser divertidas pero cortas, no mas de 5 palabras'
        

        self.conversation.append({'role': 'system', 'content': self._system_role})
    

    def generate_phrases(self, num_phrases:int) -> list[str]:

        self.conversation.append({'role': 'user', 'content': f'Genera {num_phrases} frase'})

        phrases = list()
        for _ in num_phrases:
            phrase = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.conversation,
                temperature=0.7,
                max_tokens=256
            )
            phrases.append(phrase['choices'][0]['message']['content'])

        return self.clean_phrases(phrases)


    def clean_phrases(self, options:list[str]) -> list[str]:
        for i, option in enumerate(options):
            option = option.replace('"', '').replace('\n', '')
            options[i] = option
        return options


    def next_phrase(self) -> list[str]:
        return self.generate_phrases(1)
        

    def set_topic(self, topic:StoryTopic) -> None:
        self.topic = topic
