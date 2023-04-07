import os
import openai
import random
import threading


from django.db.models.query import QuerySet


from .models.models import StoryTopic

from phrases.models.models import Phrase


from dotenv import load_dotenv


from print_pp.logging import Print

load_dotenv()


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class PhraseGenerator:

    openai.api_key = OPENAI_API_KEY

    def __init__(self, topic:StoryTopic, testing=True) -> None:
        self._topic = topic
        self.testing = testing
        self.conversation = list()
    

    def generate_phrases(self, num_phrases:int) -> list[str]:
        phrases = list()
        prompt = [{'role': 'user', 'content': f'Generame frases aleatorias de entre 8 a 10 palabras cada una, haz que estas frases tanga sentido y coloca un ~ al final de la frase (genera {num_phrases})'}]

        if self.testing:
            for _ in range(num_phrases):
                if self.testing:
                    phrases_set:QuerySet[Phrase] = Phrase.objects.all()
                    phrase = phrases_set[random.randint(0, phrases_set.count())].phrase
                    phrases.append(phrase)
                    Print('generating testing phrase', _)
        else:
            Print('generating phrase')
            phrase = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=prompt,
                temperature=0.7,
                max_tokens=256
            )
            Print(phrase)
            phrases.append(phrase['choices'][0]['message']['content'])
            

        cleaned_phrases = self.clean_phrases(phrases)
        if not self.testing:
            threading.Thread(target=self.save_phrases_to_db, kwargs={'phrases':cleaned_phrases}).start()
        return cleaned_phrases


    def clean_phrases(self, options:list[str]) -> list[str]:
        to_return = list()

        for option in options:
            option_split = option.split('~')

            for option in option_split:
                option = option.replace('"', '').replace('\n', '')
                
                try:
                    # in case the option are being enumerated (1. option) we remove the number
                    int(option[0])
                    option = option[2:]
                except ValueError:
                    pass
                
                if not option:
                    continue

                to_return.append(option)

        return to_return


    def next_phrase(self) -> list[str]:
        return self.generate_phrases(1)
        

    def set_topic(self, topic:StoryTopic) -> None:
        self.topic = topic

    
    def save_phrases_to_db(self, phrases:list[str]) -> None:

        topic = self._topic if self._topic else StoryTopic.objects.get(name='aleatorio')
        Print(topic)
        for phrase in phrases:
            Phrase.objects.create(phrase=phrase, topic=topic)
            Print('phrase saved to db')

