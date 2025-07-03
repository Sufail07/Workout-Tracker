from django.shortcuts import render
from rest_framework.decorators import  api_view, permission_classes, action
from .models import Exercise, WorkoutPlan
from .serializers import RegisterSerializer, ExerciseSerializer, WorkoutPlanSerializer
from rest_framework import generics, viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class WorkoutPlanViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutPlanSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return WorkoutPlan.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        workout = self.get_object()

        if workout.user != request.user:
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        if workout.completed == True:
            return Response({'detail': 'Workout already completed'})
        
        workout.completed = True
        workout.save()
        return Response({'status': 'Workout marked as completed'})

    @action(detail=False, methods=['get'])
    def get_completed(self, request, pk=None):
        completed_workouts = WorkoutPlan.objects.filter(user=request.user, completed=True)
        serializer = WorkoutPlanSerializer(completed_workouts, many=True)
        return Response({'workouts': serializer.data})
        