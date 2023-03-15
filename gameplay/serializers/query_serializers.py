from django.utils.translation import gettext_lazy as _


from rest_framework import serializers


from phrases.models.models import StoryTopic


class GeneratePhrasesQuerySerializer(serializers.Serializer):

    options_to_generate = serializers.IntegerField(min_value=1, max_value=5)
    topic_id = serializers.UUIDField(default=None, allow_null=True)

    
    def validate(self, attrs):
        self.__convert_to_objects(attrs)
        return super().validate(attrs)
    

    def __convert_to_objects(self, attrs:dict) -> dict:
        if topic := attrs.get('topic_id'):
            try: attrs['topic'] = StoryTopic.objects.get(pk=topic)
            except StoryTopic.DoesNotExist: raise serializers.ValidationError(_('The topic does not exist'))
            

