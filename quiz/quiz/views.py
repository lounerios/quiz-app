from rest_framework import viewsets
from quiz import models
from rest_framework.decorators import api_view
from quiz import serializers
from django.http.response import JsonResponse
import random

@api_view(['GET'])
def get_quiz(request):
    random.seed(None)

    number_of_quizzes = models.Quiz.objects.count()
    q = random.randint(1, number_of_quizzes)
    quiz_name = 'Quiz '+str(q)

    quiz = models.Quiz.objects.get(name=quiz_name)
    quiz_data = serializers.QuizSerializer(quiz)
    return JsonResponse(quiz_data.data)
