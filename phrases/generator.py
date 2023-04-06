import os
import openai
import random


from django.db.models.query import QuerySet


from .models.models import StoryTopic

from phrases.models.models import Phrase


from dotenv import load_dotenv


from print_pp.logging import Print

load_dotenv()


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class PhraseGenerator:

    openai.api_key = OPENAI_API_KEY
    conversation = list()

    def __init__(self, topic:StoryTopic, testing=True) -> None:
        self._topic = topic
        self._system_role = None
        self.testing = testing

        if self._topic:
            self._system_role = f'Eres un generador de frases aleatorias con el tópico de "{self._topic.spanish_name}", \
            las frases que generes deben ser divertidas pero cortas, no mas de 5 palabras'
        else:
            self._system_role = 'Eres un generador de frases aleatorias con temática aleatoria, \
            las frases que generes deben ser divertidas pero cortas, no mas de 5 palabras'
        

        self.conversation.append({'role': 'system', 'content': self._system_role})
    

    def generate_phrases(self, num_phrases:int) -> list[str]:
        phrases = list()
        self.conversation.append({'role': 'user', 'content': f'Genera {num_phrases} frase, y al final de cada frase coloca un ~'})

        for _ in range(num_phrases):
            if self.testing:
                phrases_set:QuerySet[Phrase] = Phrase.objects.all()
                phrases.append(phrases_set[random.randint(0, phrases_set.count())].phrase)
                Print('generating testing phrase', _)
            else:
                Print('generating phrase', _)
                phrase = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=self.conversation,
                    temperature=0.7,
                    max_tokens=256
                )
                Print(phrase)
                phrases.append(phrase['choices'][0]['message']['content'])
            

        return self.clean_phrases(phrases)


    def clean_phrases(self, options:list[str]) -> list[str]:
        to_return = list()

        for option in options:
            option_split = option.split('~')

            for option in option_split:
                option = option.replace('"', '').replace('\n', '')
                to_return.append(option)

        return to_return


    def next_phrase(self) -> list[str]:
        return self.generate_phrases(1)
        

    def set_topic(self, topic:StoryTopic) -> None:
        self.topic = topic

