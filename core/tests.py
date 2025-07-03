from django.test import TestCase
from .models import Exercise
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

# Create your tests here.


class ExerciseModelTest(TestCase):
    def test_create_exercise(self):
        exercise = Exercise.objects.create(name='Push-up', description='Push-up for chest', category='strength', muscle_group='chest')
        self.assertEquals(exercise.name, 'Push-up')

class WorkoutAPITest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_register_user(self):
        data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'password2': 'newpassword123',
            'email': 'newuser@gmail.com'
        }
        response = self.client.post('/api/register/', data)
        print(response.data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

def get_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

class AuthWorkoutTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass')
        self.token = get_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ self.token)

    def test_get_workouts(self):
        response = self.client.get('/api/workouts/')
        self.assertEquals(response.status_code, 200)