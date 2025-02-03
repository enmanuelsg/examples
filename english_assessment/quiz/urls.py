from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('quiz_selection/', views.quiz_selection, name='quiz_selection'),
    path('start_quiz/', views.start_quiz, name='start_quiz'),
    path('quiz_question/', views.quiz_question, name='quiz_question'),
]
