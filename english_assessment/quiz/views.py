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
    question_ids = list(Question.objects.values_list('id', flat=True))
    if len(question_ids) < 5:
        return render(request, 'quiz/quiz_selection.html', {'error': 'Not enough questions.'})

    # Create QuizAttempt and force session save
    attempt = QuizAttempt.objects.create(user=request.user, score=0)
    request.session['quiz_attempt_id'] = attempt.id
    request.session.modified = True  # Force session to save

    selected_ids = random.sample(question_ids, 5)
    request.session['quiz_questions'] = selected_ids
    request.session['current_question'] = 0
    request.session['score'] = 0  # Optional: Can now be removed since score is calculated from DB

    return redirect('quiz_question')

@login_required
def quiz_question(request):
    # Validate session data first
    quiz_questions = request.session.get('quiz_questions')
    quiz_attempt_id = request.session.get('quiz_attempt_id')
    current_index = request.session.get('current_question', 0)

    # Redirect to start if session is invalid
    if not quiz_questions or not quiz_attempt_id:
        return redirect('start_quiz')

    # Handle completed quiz
    if current_index >= len(quiz_questions):
        try:
            attempt = QuizAttempt.objects.get(id=quiz_attempt_id)
            # Calculate score from actual answers
            attempt.score = attempt.answers.filter(is_correct=True).count()
            attempt.save()
            # Cleanup session
            for key in ['quiz_questions', 'current_question', 'quiz_attempt_id', 'score']:
                if key in request.session:
                    del request.session[key]
            return render(request, 'quiz/result.html', {'score': attempt.score})
        except QuizAttempt.DoesNotExist:
            # Handle invalid attempt ID
            return redirect('start_quiz')

    # Get current question
    question_id = quiz_questions[current_index]
    question = get_object_or_404(Question, id=question_id)

    # Process answer submission
    if request.method == 'POST':
        selected_option = request.POST.get('option')
        is_correct = (selected_option == question.correct_option)

        try:
            # Save answer to database
            attempt = QuizAttempt.objects.get(id=quiz_attempt_id)
            Answer.objects.create(
                quiz_attempt=attempt,
                question=question,
                selected_option=selected_option,
                is_correct=is_correct
            )
        except QuizAttempt.DoesNotExist:
            return redirect('start_quiz')

        # Prepare feedback and advance
        request.session['current_question'] = current_index + 1
        feedback = 'Correct!' if is_correct else f'Incorrect. The right answer was {question.correct_option}'
        return render(request, 'quiz/question.html', {
            'question': question,
            'feedback': feedback,
            'answered': True
        })

    # Display unanswered question
    return render(request, 'quiz/question.html', {'question': question})