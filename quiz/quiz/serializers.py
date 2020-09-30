from quiz import models
from rest_framework import serializers

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Question
        fields = ('id', 'question', 'correct_answer', 'incorrect_answer_1', 
        'incorrect_answer_2', 'incorrect_answer_3')

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.Quiz
        fields = ('id', 'name', 'questions')