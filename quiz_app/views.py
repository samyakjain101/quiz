from django.shortcuts import render
from django.views.generic import TemplateView
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