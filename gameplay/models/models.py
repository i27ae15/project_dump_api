import uuid

from django.db import models


class StoryTopic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    english_name = models.CharField(max_length=100)
    spanish_name = models.CharField(max_length=100)


    def __str__(self):
        return f'{self.id} - {self.english_name}'
