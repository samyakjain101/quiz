import uuid
import json
import pytz
from datetime import timedelta, datetime #for timer 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from .models import *

# Create your views here.

class AvailableQuiz(LoginRequiredMixin ,TemplateView):
    template_name = "quiz_app/available_quiz.html"
    def get_context_data(self, **kwargs):
        # quizzes = Quiz.objects.filter(start_date__lt=timezone.now(),end_date__gt=timezone.now())
        quizzes = Quiz.objects.filter(start_date__lt=timezone.now()).order_by('-start_date')
        context = {
            'quizzes' : quizzes
        }
        return context

@login_required
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
    #If not Permission Denied.
    if quiz.start_date <= timezone.now() and quiz.end_date > timezone.now():
        obj, created = QuizRecord.objects.get_or_create(user=request.user, quiz=quiz)
        if created:
            QuizAnswerRecord.objects.bulk_create(
                [QuizAnswerRecord(record = obj, question = x) for x in quiz.question_set.all()]
            )
        else:
            if obj.start + quiz.duration < timezone.now() or obj.is_submitted:
                raise PermissionDenied()
        return redirect('quiz_app:live_quiz_new', quiz_id=quiz_id)
    else:
        raise PermissionDenied()

@login_required
def liveQuiz(request, quiz_id):
    context = {}
    try:
        quiz = Quiz.objects.get(id = uuid.UUID(quiz_id).hex)
        quiz_record = QuizRecord.objects.get(user=request.user, quiz=quiz)
    except (ValueError, Quiz.DoesNotExist, QuizRecord.DoesNotExist):
        raise PermissionDenied()
    
    if quiz.start_date > timezone.now() or quiz_record.is_submitted:
        raise PermissionDenied()

    questions = quiz_record.quizanswerrecord_set.all().order_by('id')

    # Using Paginator
    paginator = Paginator(questions, 1) # Show 1 question per page.
    page_number = request.GET.get('page')
    if not page_number:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    context = {
        'quiz' : quiz,
        'page_obj' : page_obj,
        'records' : questions,
    }

    #timer contexts adding
    recordStartDate = quiz_record.start
    gmt5 = pytz.timezone(settings.TIME_ZONE)
    recordStartDate = recordStartDate.astimezone(gmt5)
    quizDuration = quiz.duration
    context['years'],context['months'],context['days'],context['hours'],context['minutes'],context['seconds'] = startTimer(quiz.end_date,recordStartDate,quizDuration)
    context['expiryUrl'] = reverse('quiz_app:available_quiz')

    #Save Answer if there.
    to_do = request.GET.get('to_do')
    if to_do:
        question_id = request.GET.get('question_id')
        choice_id = request.GET.get('choice_id')
        try:
            question = QuizAnswerRecord.objects.get(id=question_id)
            if choice_id:   
                choice = Choice.objects.get(id=choice_id)
            else:
                choice = None

            if to_do == "saveAndNext" and choice:
                question.status = QuizAnswerRecord.SAVE_AND_NEXT
            elif to_do == "markForReview":
                question.status = QuizAnswerRecord.MARK_FOR_REVIEW

            question.myAns = choice
            question.save()

        except (Choice.DoesNotExist, QuizAnswerRecord.DoesNotExist):
            raise PermissionDenied()
    else:
        pass

    return render(request, template_name="quiz_app/quiz_questions.html", context=context)

def startTimer(quizEndDate,recordStartDate,quizDuration):
    #below for timer
    #For setting time for js timer:
    # (end date - start date) = Total duration or Td
    Td = quizEndDate - recordStartDate
    if Td > quizDuration:  # case 1: Td > d -> timerDuration = d
        timerDuration = quizDuration
    elif Td < quizDuration: # case 2: Td < d -> timerDuration = Td
        timerDuration = Td 
    elif Td == quizDuration: # case 3: Td == d -> timerDuration = d
        timerDuration = quizDuration
    
    recordEndDate = recordStartDate + timerDuration
    
    if recordEndDate < datetime.now(tz=recordEndDate.tzinfo):
        raise PermissionDenied()

    return recordEndDate.year, recordEndDate.month, recordEndDate.day, recordEndDate.hour, recordEndDate.minute, recordEndDate.second

class Results(LoginRequiredMixin ,TemplateView):
    template_name = "quiz_app/results.html"
    def get_context_data(self, **kwargs):
        results = QuizRecord.objects.filter(user=self.request.user, quiz__end_date__lt=timezone.now())
        context = {
            'results' : results
        }
        return context

class QuizResult(LoginRequiredMixin ,TemplateView):
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
            if quiz.end_date < timezone.now():
                #Quiz has ended and no one can give it now.
                #Can show results now.
                score = 0
                total_attempted = 0
                records = record.quizanswerrecord_set.all()
                total_questions = records.count()
                for r in record.quizanswerrecord_set.all():
                    if r.myAns:
                        total_attempted += 1 
                        if r.myAns.is_correct:
                            score += 1

                allRecord = record.quizanswerrecord_set.all() # this is list of all ques
                context['allRecord'] = allRecord
                context['quiz'] = quiz
                context['score'] = score
                context['total_attempted'] = total_attempted
                context['total_questions'] = total_questions
            else:
                raise PermissionDenied

        except (Quiz.DoesNotExist, QuizRecord.DoesNotExist):
            raise PermissionDenied()

        return context

@login_required
def end_quiz(request, quiz_id):
    try:
        quiz_id = uuid.UUID(quiz_id).hex
    except ValueError:
        raise PermissionDenied()

    try:
        quiz = Quiz.objects.get(id=quiz_id)
        record = QuizRecord.objects.get(user=request.user, quiz=quiz)
    except (Quiz.DoesNotExist, QuizRecord.DoesNotExist):
        raise PermissionDenied()

    record.is_submitted = True
    record.save()
    return redirect('quiz_app:available_quiz')