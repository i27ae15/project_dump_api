import uuid

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .enums import PhraseLanguage


class StoryTopic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    language:int = models.IntegerField(choices=PhraseLanguage.choices, default=PhraseLanguage.ENGLISH)
    name:str = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.id} - {self.name}'
    

class Phrase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    topic:StoryTopic = models.ForeignKey(StoryTopic, on_delete=models.CASCADE, related_name='phrases')

    phrase:str = models.CharField(max_length=256)


    def __str__(self):
        return f'{self.id} - {self.topic.name}'

