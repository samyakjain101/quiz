import uuid
import json
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponse
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
    #If not then redirect to results else create quiz object
    obj, created = QuizRecord.objects.get_or_create(user=request.user, quiz=quiz)
    if created:
        return redirect('quiz_app:live_quiz', quiz_id=quiz_id)
    else:
        return redirect('quiz_app:quiz_result', quiz_id=quiz_id)

class LiveQuiz(TemplateView):
    template_name = "quiz_app/quiz_questions.html"
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

        questions = quiz.question_set.all().order_by('question_number')
        paginator = Paginator(questions, 1) # Show 1 question per page.

        page_number = self.request.GET.get('page')
        if not page_number:
            page_number = 1
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj' : page_obj,
            'allPages' : paginator.page_range,
        }

        try:
            record = QuizRecord.objects.get(user=self.request.user, quiz = page_obj.object_list[0].quiz)
            answer = QuizAnswerRecord.objects.get(record = record, question = page_obj.object_list[0]).myAns
            context['answer'] = answer
        except (QuizRecord.DoesNotExist, QuizAnswerRecord.DoesNotExist):
            #If this exception is called this means user has not answered this question till now.
            #Do nothing
            pass

        all_status = [0]*questions.count()
        for x in QuizAnswerRecord.objects.filter(record = record).order_by("question__question_number"):
            all_status[x.question.question_number - 1] = x.status
        context['all_status'] = all_status
        
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
                if r.myAns and r.myAns.is_correct:
                    score += 1

            context['quiz'] = quiz
            context['score'] = score
            context['total_attempted'] = total_attempted
            context['total_questions'] = total_questions

        except (Quiz.DoesNotExist, QuizRecord.DoesNotExist):
            raise PermissionDenied()

        return context

def save_answer(request):
    jsonr = {}
    if request.is_ajax():
        current_user = request.user
        to_do = request.GET.get('to_do')
        question_id = request.GET.get('question_id')
        choice_id = request.GET.get('choice_id')
        
        try:
            question = Question.objects.get(id=question_id)
            if choice_id:   
                choice = Choice.objects.get(id=choice_id)
            else:
                choice = None
            quiz_record = QuizRecord.objects.get(user=current_user, quiz=question.quiz)

        except (Question.DoesNotExist, Choice.DoesNotExist, QuizRecord.DoesNotExist):
            raise PermissionDenied()

        try:
            quiz = QuizAnswerRecord.objects.get(record=quiz_record, question=question)

            if to_do == "saveAndNext":
                jsonr['message'] = "Choice Updated"
                quiz.status = QuizAnswerRecord.SAVE_AND_NEXT
            elif to_do == "markForReview":
                quiz.status = QuizAnswerRecord.MARK_FOR_REVIEW
                jsonr['message'] = "Marked For Review"

            quiz.myAns = choice
            quiz.save()

        except QuizAnswerRecord.DoesNotExist:
            if to_do == "saveAndNext":
                jsonr['message'] = "Your response is saved"
                status = QuizAnswerRecord.SAVE_AND_NEXT
            elif to_do == "markForReview":
                jsonr['message'] = "Marked For Review"
                status = QuizAnswerRecord.MARK_FOR_REVIEW

            QuizAnswerRecord.objects.create(
                record=quiz_record, 
                question=question,
                myAns=choice,
                status=status
            )
        
    return HttpResponse(json.dumps(jsonr), content_type='application/json')