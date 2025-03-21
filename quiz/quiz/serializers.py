from quiz.api_models import Quiz, Question
from rest_framework import serializers
import random

class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ('id', 'question', 'answers')
    
    def get_answers(self, obj):
        answers = []
        answers.append(obj.correct_answer)
        answers.append(obj.incorrect_answer_1)
        answers.append(obj.incorrect_answer_2)
        answers.append(obj.incorrect_answer_3)

        random.shuffle(answers)

        return answers

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Quiz
        fields = ('id', 'name', 'questions')



