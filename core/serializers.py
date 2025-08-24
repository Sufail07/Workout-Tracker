from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Exercise, WorkoutExercise, WorkoutPlan


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Passwords do not match')
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

        
class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'
        
        
class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise_name = serializers.CharField(source='exercise.name', read_only=True)

    class Meta:
        model = WorkoutExercise
        fields = ['id', 'exercise', 'exercise_name', 'sets', 'reps', 'weights']

class WorkoutPlanSerializer(serializers.ModelSerializer):
    workout_exercises = WorkoutExerciseSerializer(many=True, required=False)

    class Meta:
        model = WorkoutPlan
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        exercises_data = validated_data.pop('workout_exercises', [])
        if not isinstance(exercises_data, list):
            raise TypeError(f"Expected list of exercises, got {type(exercises_data)}")
        
        workout_plan = WorkoutPlan.objects.create(**validated_data)
        for exercise in exercises_data:
            WorkoutExercise.objects.create(workout_plan=workout_plan, **exercise)
        return workout_plan
