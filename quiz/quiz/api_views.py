from rest_framework import viewsets
from quiz import models
from rest_framework.decorators import api_view
from quiz import serializers
from django.http.response import JsonResponse
import random
from rest_framework.parsers import JSONParser 
import json
from quiz.api_models import UserSubmit, Quiz, QuizQuestions, Question

@api_view(['GET'])
def get_quiz(request):
    random.seed(None)

    number_of_quizzes = Quiz.objects.count()
    q = random.randint(1, number_of_quizzes)
    quiz_name = 'Quiz '+str(q)

    quiz = Quiz.objects.get(name=quiz_name)
    quiz_data = serializers.QuizSerializer(quiz)

    return JsonResponse(quiz_data.data)


@api_view(['POST'])
def post_answers(request):
    correct_answers = 0
    data = request.data
    total_answers = 0
    for answer in data:
        total_answers = total_answers + 1
        question_id = answer['question']
        question = Question.objects.get(id=question_id)
        if question.correct_answer == answer['answer']:
            correct_answers += 1

    userSubmit = UserSubmit(correct_answers=correct_answers, total_answers=total_answers)
    userSubmit.save()

    jsonResponse = {}
    jsonResponse['correct_answers'] = str(correct_answers) + '/' + str(total_answers)
    
    return JsonResponse(jsonResponse)

@api_view(['GET'])
def rate(request):
    total_answers = UserSubmit.objects.count()
    percentage_rate = 0
    if total_answers > 0:
        answers = UserSubmit.objects.filter(correct_answers__gte=6).count()
        percentage_rate = 100 *(float(answers) / float(total_answers))

    jsonRate = {}
    jsonRate['rate'] = percentage_rate

    return JsonResponse(jsonRate)



