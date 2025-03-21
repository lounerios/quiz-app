from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
import requests
from quiz.game_models import GameQuestion, GameQuiz, GameAnswer, GameResult
from quiz.models import QuizResult, QuizAnswer

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
                    quizAnswer = QuizAnswer(questionId=questionId, questionAnswer=answer)
                    quizAnswer.save()
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

def results_view(request):
    if request.user.is_authenticated:
        results = QuizResult.objects.filter(userName=request.user)

        return render(request, 'results.html', {'results': results})

    else:
        return redirect('login')

def stats_view(request):
    if request.user.is_authenticated:
        response = requests.get('http://127.0.0.1:8000/api/rate')
        rate = response.json()['rate']
        return render(request, 'stats.html', {'rate': rate})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
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
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')

        return render(request, 'signup.html', {'form': form})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    else:
        return redirect('login')