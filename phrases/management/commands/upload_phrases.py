import os

from django.core.management.base import BaseCommand

from phrases.models.models import Phrase, StoryTopic


class Command(BaseCommand):


    def handle(self, *args, **kwargs):

        topic:StoryTopic = StoryTopic.objects.get(id='e4c39256-56e0-4083-bd9a-70e86de21dc0')
        absolute_route = os.path.join(os.getcwd(), 'phrases.txt')

        with open(absolute_route, 'r', encoding='UTF-8') as file:

            lines = file.readlines()

            for line in lines:
                cleaned_line = line.strip().replace('\n', '')
                if cleaned_line[-1] == '.': cleaned_line = cleaned_line[:-1]

                Phrase.objects.create(topic=topic, phrase=cleaned_line)

