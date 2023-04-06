from django.contrib import admin

from .models.models import StoryTopic, Phrase

admin.site.register(StoryTopic)
admin.site.register(Phrase)
