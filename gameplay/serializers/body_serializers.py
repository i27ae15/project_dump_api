from rest_framework import serializers


class EvaluateStoryBodySerializer(serializers.Serializer):

    story = serializers.CharField(max_length=1000)

    def validate(self, data):
        if len(data['story']) < 10:
            raise serializers.ValidationError('Story is too short')
        return data



