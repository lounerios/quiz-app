from rest_framework import viewsets
from quiz import models
from rest_framework.decorators import api_view
from quiz import serializers
from django.http.response import JsonResponse
import random
from rest_framework.parsers import JSONParser 

@api_view(['GET'])
def get_quiz(request):
    random.seed(None)

    number_of_quizzes = models.Quiz.objects.count()
    q = random.randint(1, number_of_quizzes)
    quiz_name = 'Quiz '+str(q)

    quiz = models.Quiz.objects.get(name=quiz_name)
    quiz_data = serializers.QuizSerializer(quiz)

    return JsonResponse(quiz_data.data)


@api_view(['POST'])
def post_answers(request):
    correct_answers = 0
    answers_data = JSONParser().parse(request) 
    answers = serializers.AnswersSerializer(data=answers_data)
    print(answers.correct_answers)
#    for answer in request.data:
#        question_id = answer['question']
#        question = models.Question.objects.get(id=question_id)
#        if question.correct_answer == answer['answer']:
#            correct_answers += 1

#    jsonResponse = {}
#    jsonResponse['Correct Answers'] = correct_answers 

#    return JsonResponse(jsonResponse)

