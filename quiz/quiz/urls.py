from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from quiz import views
from quiz.user_views import home_view, signup_view, login_view, results_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('results/', results_view, name='results'),
    path('logout/', logout_view, name='logout'),
    url(r'api/quiz', views.get_quiz),
    url(r'api/answers/', views.post_answers),


]