from django.urls import path
from .views import *

app_name = 'quiz_app'

urlpatterns = [
    path('available_quiz/', AvailableQuiz.as_view(), name="available_quiz"),
]
