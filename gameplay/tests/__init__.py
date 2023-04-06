from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


from utils.testing import print_success, print_starting, print_error


class EvaluateStoryViewTestCase(APITestCase):

    def setUp(self):
        self.url = reverse('evaluate_story')


    def evaluate_story_success(self):
        print_starting()
        # Crear un objeto de datos de prueba válido para el body de la petición
        data = {'story': 'Esta es una historia de prueba.'}

        # Hacer la petición POST a la vista
        response = self.client.post(self.url, data, format='json')

        # Verificar que la respuesta es exitosa (status code 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar que la respuesta contiene la clave 'score'
        self.assertIn('score', response.json())

        # Verificar que el valor de la clave 'score' es un entero entre 1 y 10
        score = response.json()['score']
        self.assertIsInstance(score, int)
        self.assertGreaterEqual(score, 1)
        self.assertLessEqual(score, 10)

        print_success()
        

    def evaluate_story_bad_request(self):
        print_starting()

        # Crear un objeto de datos de prueba inválido para el body de la petición
        data = {'story': ''}

        # Hacer la petición POST a la vista
        response = self.client.post(self.url, data)

        # Verificar que la respuesta es un error de petición inválida (status code 400)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        print_success()


    def evaluate_story_not_found(self):
        print_starting()
        
        # Crear un objeto de datos de prueba válido para el body de la petición
        data = {'story': 'Esta historia no existe.'}

        # Hacer la petición POST a una URL que no existe
        url = reverse('evaluate-story-not-found')
        response = self.client.post(url, data)

        # Verificar que la respuesta es un error de recurso no encontrado (status code 404)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        print_success()
