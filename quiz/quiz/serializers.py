from quiz import models
from rest_framework import serializers
import random

class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = models.Question
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
        model = models.Quiz
        fields = ('id', 'name', 'questions')


class AnswerSerializer(serializers.Serializer):
    question_id: serializers.IntegerField()
    answer: serializers.CharField(max_length=256)

class AnswersSerializer(serializers.Serializer):
    answers = AnswerSerializer(many=True, read_only=True)
    correct_answers = serializers.SerializerMethodField()

    def get_correct_answers(self, obj):
        print(obj.answers)

    class Meta:
        fields = ('correct_answers')


