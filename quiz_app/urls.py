from django.urls import path
from .views import *

app_name = 'quiz_app'

urlpatterns = [
    path('quiz/available', AvailableQuiz.as_view(), name="available_quiz"),
    path('quiz/check/<quiz_id>', attempt_quiz, name="attempt_quiz"),
    # path('quiz/result/<quiz_id>', QuizResult.as_view(), name="quiz_result"),
    # path('quiz/live/<quiz_id>', LiveQuiz.as_view(), name="live_quiz"),
    # path('ajax/live/quiz',save_answer, name="ajax_save_live_quiz"),
    path('live/quiz/<quiz_id>',liveQuiz, name="live_quiz_new"),
]
