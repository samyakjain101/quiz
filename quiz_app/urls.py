from django.urls import path
from .views import *

app_name = 'quiz_app'

urlpatterns = [
    path('quiz/available', AvailableQuiz.as_view(), name="available_quiz"),
    path('quiz/check/<quiz_id>', attempt_quiz, name="attempt_quiz"),
    path('quiz/result/<quiz_id>', QuizResult.as_view(), name="quiz_result"),
    # path('ajax/live/quiz',save_answer, name="ajax_save_live_quiz"),
    path('live/quiz/<quiz_id>',liveQuiz, name="live_quiz_new"),
    path('live/quiz/end/<quiz_id>',end_quiz, name="end_quiz"),
    path('quiz/results',Results.as_view(), name="results"),
]
