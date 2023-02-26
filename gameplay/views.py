import os

import openai

from dotenv import load_dotenv

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


from gameplay.models.models import StoryTopic
from gameplay.serializers.query_serializers import GeneratePhrasesQuerySerializer
from gameplay.serializers.model_serializers import StoryTopicModelSerializer


from drf_yasg.utils import swagger_auto_schema


from print_pp.logging import Print


load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class GeneratePhrasesView(APIView):


    @swagger_auto_schema(
        operation_description='Generates a list of phrases with the given topic',
        query_serializer=GeneratePhrasesQuerySerializer,
        responses={
            200: 'Success',
            400: 'Bad request',
            404: 'Not found',
        }
    )
    def get(self, request):
        
        query_serializer = GeneratePhrasesQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        query_data = query_serializer.validated_data

        options = self.generate_options(query_data['options_to_generate'], query_data.get('topic'))
        print(options)
        return Response(options, status=status.HTTP_200_OK)
        
    
    def generate_options(self, options_to_generate:int, topic:StoryTopic) -> list[str]:
        openai.api_key = OPENAI_API_KEY
        current_options = []

        if topic: 
            prompt = f'Genera una frase aleatoria, de no mas de 5 palabras, con temática de {topic.spanish_name}, no te preocupes por la gramática, solo por la temática.'
        else:
            prompt = 'Genera una frase aleatoria, de no mas de 5 palabras, con temática aleatoria.'
            
        for _ in range(options_to_generate):
            response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=0.8, max_tokens=256)
            current_options.append(response['choices'][0]['text'])
        
        return self.clean_options(current_options)


    def clean_options(self, options:list[str]) -> list[str]:
        for i, option in enumerate(options):
            option = option.replace('"', '').replace('\n', '')
            options[i] = option
        return options



class StoryTopicView(APIView):


    @swagger_auto_schema(
        operation_description='Returns a list of all the story topics',
        responses={
            200: 'Success',
            400: 'Bad request',
            404: 'Not found',
        }
    )
    def get(self, request):
        story_topics = StoryTopic.objects.all()
        serializer = StoryTopicModelSerializer(story_topics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
