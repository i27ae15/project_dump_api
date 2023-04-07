from rest_framework import serializers


class LoginBodySerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        fields = ('email', 'password')