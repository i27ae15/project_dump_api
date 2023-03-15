from rest_framework import serializers

from phrases.models.models import StoryTopic


class StoryTopicModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryTopic
        fields = ('id', 'english_name', 'spanish_name')
        read_only_fields = ('id',)
