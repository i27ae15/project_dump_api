from django.urls import path

from gameplay.views import GeneratePhrasesView, StoryTopicView

urlpatterns = [
    path('generate-phrases/', GeneratePhrasesView.as_view(), name='generate-phrases'),
    path('story-topics/', StoryTopicView.as_view(), name='story-topics'),
]
