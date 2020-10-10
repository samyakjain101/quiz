import uuid
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.utils import timezone
from .models import *
# Create your views here.

class AvailableQuiz(TemplateView):
    template_name = "quiz_app/available_quiz.html"
    def get_context_data(self, **kwargs):
        quizzes = Quiz.objects.filter(start_date__lt=timezone.now(),end_date__gt=timezone.now())
        context = {
            'quizzes' : quizzes
        }
        return context

def attempt_quiz(request, **kwargs):

    # Check if quiz_id is valid uuid 
    try:
        quiz_id = uuid.UUID(kwargs['quiz_id']).hex
    except ValueError:
        raise PermissionDenied()

    try: 
        quiz = Quiz.objects.get(id = quiz_id)
    except Quiz.DoesNotExist:
        raise PermissionDenied()

    #Check if user is attempting quiz first time.
    #If not PermissionDenied else create quiz object
    obj, created = QuizRecord.objects.get_or_create(user=request.user, quiz=quiz)
    if created:
        return redirect('quiz_app:live_quiz', quiz_id=quiz_id)
    else:
        return redirect('quiz_app:quiz_result', quiz_id=quiz_id)

class LiveQuiz(TemplateView):
    template_name = "quiz_app/live_quiz.html"
    def get_context_data(self, **kwargs):

        try:
            quiz_id = uuid.UUID(kwargs['quiz_id']).hex
        except ValueError:
            raise PermissionDenied()

        try: 
            quiz = Quiz.objects.get(id = quiz_id)
        except Quiz.DoesNotExist:
            raise PermissionDenied()

        # Using Paginator

        questions = quiz.question_set.all()
        paginator = Paginator(questions, 1) # Show 1 question per page.

        page_number = self.request.GET.get('page')
        if not page_number:
            page_number = 1
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj' : page_obj,
        }
        return context

class QuizResult(TemplateView):
    template_name = "quiz_app/quiz_result.html"
    def get_context_data(self, **kwargs):
        context = {}
        try:
            quiz_id = uuid.UUID(kwargs['quiz_id']).hex
        except ValueError:
            raise PermissionDenied()

        try:
            quiz = Quiz.objects.get(id=quiz_id)
            record = QuizRecord.objects.get(user=self.request.user, quiz=quiz)
            score = 0
            total_attempted = 0
            total_questions = record.quiz.question_set.all().count()
            for r in record.quizanswerrecord_set.all():
                total_attempted += 1 
                if r.myAns.is_correct:
                    score += 1

            context['quiz'] = quiz
            context['score'] = score
            context['total_attempted'] = total_attempted
            context['total_questions'] = total_questions

        except Quiz.DoesNotExist or QuizRecord.DoesNotExist:
            print("Something does not exist")
            pass

        return context