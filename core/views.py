from rest_framework.decorators import action
from .models import Exercise, WorkoutPlan
from .serializers import RegisterSerializer, ExerciseSerializer, WorkoutPlanSerializer
from rest_framework import generics, viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

# Rate limiting
class GetWorkoutsThrottle(UserRateThrottle):
    rate =  '5/min'

class ThrottledTokenObtainPairView(TokenObtainPairView):
    throttle_scope = 'login'


# registration view
class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

# basic crud of workoutplans
'''
Implemented rate limiting GET request to the workoutplan endpoint to 5 requests per minute by a user.
Handled caching with timeout set to 5 minutes
'''
class WorkoutPlanViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutPlanSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = []
    
    def get_queryset(self):
        return WorkoutPlan.objects.filter(user=self.request.user)
    
    
    def get_throttles(self):
        if self.action == 'list':
            return [GetWorkoutsThrottle()]
        return super().get_throttles()
    
    def list(self, request, *args, **kwargs):
        cache_key = f'workout_data_{self.request.user.id}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = WorkoutPlanSerializer(queryset, many=True)
        cache.set(cache_key, serializer.data, timeout=60*5)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    
    # Invalidating cache during creation, update and deletion
    def perform_create(self, serializer):
        plan = serializer.save(user=self.request.user)
        cache.delete(f'workout_data_{self.request.user.id}')
        return plan
        
    def perform_update(self, serializer):
        plan = serializer.save()
        cache.delete(f'completed_workouts_{self.request.user.id}')
        cache.delete(f'workout_data_{self.request.user.id}')
        return plan
    
    def perform_destroy(self, instance):
        user_id = instance.user.id
        instance.delete()
        cache.delete(f'completed_workouts_{self.request.user.id}')
        cache.delete(f'workout_data_{user_id}')
    
    # endpoint to mark a workout as completed
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        workout = self.get_object()

        if workout.user != request.user:
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        if workout.completed == True:
            return Response({'detail': 'Workout already completed'})
        
        workout.completed = True
        workout.save()
        cache.delete(f'completed_workouts_{request.user.id}')
        return Response({'status': 'Workout marked as completed'})

    # endpoint to get completed workouts
    @action(detail=False, methods=['get'])
    def get_completed(self, request, pk=None):
        cache_key = f'completed_workouts_{request.user.id}'
        completed_workouts = cache.get(cache_key)
        
        if completed_workouts is None:
            queryset = WorkoutPlan.objects.filter(user=request.user, completed=True)
            serializer = WorkoutPlanSerializer(queryset, many=True)
            completed_workouts = serializer.data
            cache.set(cache_key, completed_workouts, timeout=60*5)
            
        return Response({'workouts': completed_workouts})
        

# CRUD for exercises 
class ExerciseViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]
    
    # Implementing caching with timeout set for 10 minutes for getting all the existing exercises.
    def get_queryset(self):
        return Exercise.objects.all()
    
    def get_throttles(self):
        if self.action == 'list':
            return [GetWorkoutsThrottle()]
        return super().get_throttles()
            
    # Implementing caching
    def list(self, request, *args, **kwargs):
        cache_key = 'exercise_data'
        if cache.get(cache_key) is None:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            cache.set(cache_key, data, timeout=60*10)
        else:
            data = cache.get(cache_key)
            
        return Response(data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs['pk']
        cache_key = f'exercise:{pk}'
        data = cache.get(cache_key)
        
        if data is None:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            data = serializer.data
            cache.set(cache_key, data, timeout=60*5)

        return Response(data, status=status.HTTP_200_OK)
    
    # Allowed creation of multiple exercises at a time, and invalidated exercise cache         
    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        cache.delete('exercise_data')
            
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


