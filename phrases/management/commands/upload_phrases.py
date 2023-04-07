import os

from django.core.management.base import BaseCommand

from phrases.models.models import Phrase, StoryTopic


class Command(BaseCommand):


    def handle(self, *args, **kwargs):

        topic:StoryTopic = StoryTopic.objects.create(name='aleatorio', language=1) 
        absolute_route = os.path.join(os.getcwd(), 'phrases.txt')

        with open(absolute_route, 'r', encoding='UTF-8') as file:

            lines = file.readlines()

            for line in lines:
                cleaned_line = line.strip().replace('\n', '')
                if cleaned_line[-1] == '.': cleaned_line = cleaned_line[:-1]

                Phrase.objects.create(topic=topic, phrase=cleaned_line)

