from django.db import models

class Question(models.Model):
    question = models.CharField(max_length=256)
    correct_answer = models.CharField(max_length=256)
    incorrect_answer_1 = models.CharField(max_length=256)
    incorrect_answer_2 = models.CharField(max_length=256)
    incorrect_answer_3 = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'questions'


class Quiz(models.Model):
    name = models.CharField(max_length=16)
    questions = models.ManyToManyField(Question, through="QuizQuestions")

    class Meta:
        managed = False
        db_table = 'quiz'


class QuizQuestions(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'quiz_questions'