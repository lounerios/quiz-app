from django.db import models

class QuizResult(models.Model):
    quizName = models.CharField(max_length=64)
    correctAnswers = models.CharField(max_length=16)
    userName = models.CharField(max_length=64)

class QuizAnswer(models.Model):
    questionId = models.IntegerField()
    questionAnswer = models.CharField(max_length=256)