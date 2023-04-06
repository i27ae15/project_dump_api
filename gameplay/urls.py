from django.urls import path

from gameplay.views import GeneratePhrasesView, StoryTopicView, EvaluateStoryView

urlpatterns = [
    path('generate-phrases/', GeneratePhrasesView.as_view(), name='generate_phrases'),
    path('story-topics/', StoryTopicView.as_view(), name='story_topics'),
    path('evaluate-story/', EvaluateStoryView.as_view(), name='evaluate_story'),
]
