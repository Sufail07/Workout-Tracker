from django.shortcuts import render
from rest_framework.decorators import  api_view, permission_classes, action
from .models import Exercise, WorkoutExercise, WorkoutPlan
from .serializers import RegisterSerializer, ExerciseSerializer, WorkoutExerciseSerializer, WorkoutPlanSerializer
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

# Create your views here.

# Rate limiting
class GetWorkoutsThrottle(UserRateThrottle):
    rate =  '5/min'


# registration view
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

# basic crud of workoutplans
class WorkoutPlanViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutPlanSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = []
    
    def get_queryset(self):
        cache_key = f'workout_data_{self.request.user.id}'
        workouts = cache.get(cache_key)

        if workouts is None:
            queryset = WorkoutPlan.objects.filter(user=self.request.user)
            serializer = WorkoutPlanSerializer(queryset, many=True)
            workouts = serializer.data
            cache.set(cache_key, workouts, timeout=60*5)
        else:
            ids = [w['id'] for w in workouts]
            return WorkoutPlan.objects.filter(id__in=ids)
                    
        return queryset
    
    # Rate limiting GET requests to the endpoint
    def list(self, request, *args, **kwargs):
        self.throttle_classes = [GetWorkoutsThrottle]
        queryset = self.filter_queryset(self.get_queryset())
        serializer = WorkoutPlanSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    # Invalidating cache during creation, update and deletion
    def perform_create(self, serializer):
        plan = serializer.save(user=self.request.user)
        cache.delete(f'completed_workouts_{self.request.user.id}')
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
        cache.delete(f'completed_workout_{request.user.id}')
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
    
    # Implementing caching
    def get_queryset(self):
        cache_key = 'exercise_data'
        exercise_id = cache.get(cache_key)
        
        if exercise_id is None:
            queryset = Exercise.objects.all()
            exercise_ids = list(queryset.values_list("id", flat=True))
            cache.set(cache_key, exercise_ids, timeout=60*10)
        else:
            queryset = Exercise.objects.filter(id__in=exercise_ids)
            
        return queryset
    
    # Implementing rate limiting/throttling
    def list(self, request, *args, **kwargs):
        self.throttle_classes = [GetWorkoutsThrottle]
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
            
    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


