from rest_framework import serializers

from users.models import User


class CreateUserSerializer(serializers.ModelSerializer):


    def create(self, validated_data):

        return User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
        )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username', 'password')

    


