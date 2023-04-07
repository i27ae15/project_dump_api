from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken, APIView


from users.models import User


from users.serializers.model_serializers import CreateUserSerializer
from users.serializers.body_serializers import LoginBodySerializer


from drf_yasg.utils import swagger_auto_schema


class ObtainAuthTokenView(ObtainAuthToken):
    
    @swagger_auto_schema(
        operation_description="Iniciar sesión",
        request_body=LoginBodySerializer,
        responses={
            200: "User token",
            400: "Bad request",
        },
    )
    def post(self, request, *args, **kwargs):
        
        request.data['username'] = request.data['email']

        response = super(ObtainAuthTokenView, self).post(request, *args, **kwargs)
        token:Token = Token.objects.get(key=response.data['token'])
        token.user:User = token.user
           
        return Response(
            {
                'token': token.key, 
                'name': token.user.get_full_name(),
                'id': token.user.pk,
            }
        )
    


class UserView(APIView):

    @swagger_auto_schema(
        operation_description="Create a new user",
        request_body=CreateUserSerializer,
        responses={
            201: CreateUserSerializer,
            400: "Bad request",
        },
    )
    def post(self, request,):

        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = serializer.data.copy()
        data.pop('password')
        print(data)

        return Response(data, status=status.HTTP_201_CREATED)


