from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
import requests
from quiz.game_models import GameQuestion, GameQuiz, GameAnswer, GameResult
from quiz.models import QuizResult

def home_view(request):
    if request.user.is_authenticated:
        #Check if form is submitted
        if request.method == 'POST':
            answers = []
            
            quizId = request.POST.get('quiz', None)
            quizName = request.POST.get('quizName', None)

            for key in request.POST:
                if 'question' in key:
                    questionId = key.split('_')[1]
                    answer = request.POST[key]
                    gameAnswer = GameAnswer(questionId, answer)

                    answers.append(gameAnswer.__dict__)

            response = requests.post('http://127.0.0.1:8000/api/answers/'+quizId, json=answers)

            quizResult = GameResult(**response.json())

            userQuizResult = QuizResult(quizName=quizName, correctAnswers=quizResult.correct_answers, userName=request.user)
            userQuizResult.save()

            return render(request, 'result.html', {'result': quizResult})

        else:
            response = requests.get('http://127.0.0.1:8000/api/quiz')
            quiz = GameQuiz(**response.json())

            return render(request, 'home.html', {'user': request.user, 'quiz': quiz})
    else:
        return redirect('login')


def login_view(request):
    form = AuthenticationForm(request.POST)

    if 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html', {'form': form})    

def signup_view(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')

    return render(request, 'signup.html', {'form': form})