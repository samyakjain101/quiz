import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta,datetime
delta = timedelta(minutes=30,)

# Create your models here.
class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    title = models.CharField(max_length=50)
    duration = models.DurationField(default = delta)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.TextField()
    
    def __str__(self):
        return str(self.question)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.CharField(max_length=50)
    is_correct = models.BooleanField(default=False)

    class Meta:
        unique_together = [
            # no duplicated choice per question
            ("question", "choice"),
        ]

    def __str__(self):
        return str(self.choice)

class QuizRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    start = models.DateTimeField(default=timezone.now) #when he started quiz first time
    is_submitted = models.BooleanField(default=False)
    class Meta:
        unique_together = [
            ("user", "quiz"),
        ]
    def __str__(self):
        return str(self.user)

class QuizAnswerRecord(models.Model):
    record =  models.ForeignKey(QuizRecord,on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    myAns = models.ForeignKey(Choice, on_delete=models.CASCADE, blank=True, null=True)
    MARK_FOR_REVIEW = 1                
    SAVE_AND_NEXT = 2   
    STATUS_CHOICES = (
        (MARK_FOR_REVIEW, 'Mark for review'),
        (SAVE_AND_NEXT, 'Save & Next'),
    )
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0)
    class Meta:
        unique_together = [
            ("record", "question"),
        ]