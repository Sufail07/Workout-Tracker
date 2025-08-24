from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Exercise(models.Model):
    CATEGORY_CHOICES = [
        ('cardio', 'Cardio'),
        ('strength', 'Strength'),
        ('flexibility', 'Flexibility')
    ]
    
    MUSCLE_GROUP_CHOICES = [
        ('chest', 'Chest'),
        ('back', 'Back'),
        ('legs', 'Legs'),
        ('arms', 'Arms'),
        ('core', 'Core'),
    ]
    name = models.CharField(max_length=35)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=True, blank=True)
    muscle_group = models.CharField(max_length=20, choices=MUSCLE_GROUP_CHOICES, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'
    
class WorkoutPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    scheduled_time = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    exercises = models.ManyToManyField(Exercise, through='WorkoutExercise')
    
    def __str__(self):
        return f'{self.name}'

class WorkoutExercise(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='workout_exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weights = models.FloatField()
    
    def __str__(self):
        return f'{self.exercise.name} - {self.workout_plan.name}'
    
