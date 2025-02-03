from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from .models import Question, QuizAttempt, Answer
import random

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quiz_selection')
    else:
        form = RegistrationForm()
    return render(request, 'quiz/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('quiz_selection')
        else:
            error = "Invalid username or password."
            return render(request, 'quiz/login.html', {'error': error})
    return render(request, 'quiz/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def quiz_selection(request):
    return render(request, 'quiz/quiz_selection.html')

@login_required
def start_quiz(request):
    # Ensure at least 5 questions are available
    question_ids = list(Question.objects.values_list('id', flat=True))
    if len(question_ids) < 5:
        return render(request, 'quiz/quiz_selection.html', {'error': 'Not enough questions in the database.'})
    # Randomly select 5 questions
    selected_ids = random.sample(question_ids, 5)
    request.session['quiz_questions'] = selected_ids
    request.session['current_question'] = 0
    request.session['score'] = 0
    return redirect('quiz_question')

@login_required
def quiz_question(request):
    quiz_questions = request.session.get('quiz_questions')
    current_index = request.session.get('current_question', 0)
    if current_index >= len(quiz_questions):
        # Record quiz attempt
        score = request.session.get('score', 0)
        QuizAttempt.objects.create(user=request.user, score=score)
        # Clear quiz session data
        for key in ['quiz_questions', 'current_question', 'score']:
            if key in request.session:
                del request.session[key]
        return render(request, 'quiz/result.html', {'score': score})
    question_id = quiz_questions[current_index]
    question = get_object_or_404(Question, id=question_id)
    context = {'question': question}
    if request.method == 'POST':
        selected_option = request.POST.get('option')
        is_correct = (selected_option == question.correct_option)
        if is_correct:
            request.session['score'] += 1
            feedback = 'Correct!'
        else:
            feedback = f'Incorrect! The correct answer is {question.correct_option}.'
        # Optional: Record the answer in detail
        # Advance to next question
        request.session['current_question'] = current_index + 1
        context.update({'feedback': feedback, 'answered': True})
        return render(request, 'quiz/question.html', context)
    return render(request, 'quiz/question.html', context)
