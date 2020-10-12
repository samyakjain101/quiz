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
        return str(self.id)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_number = models.SmallIntegerField()
    question = models.TextField()

    class Meta:
        ordering = ("question_number",)
    def __str__(self):
        return str(self.question)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.CharField(max_length=50)
    position = models.SmallIntegerField()
    is_correct = models.BooleanField(default=False)

    class Meta:
        unique_together = [
            # no duplicated choice per question
            ("question", "choice"),
        ]
        ordering = ("position",)

    def __str__(self):
        return str(self.choice)

class QuizRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    start = models.DateTimeField(default=datetime.now()) #when he started quiz first time
    end_time = models.DateTimeField(editable = False, blank=True, null=True)
    # completed = models.BooleanField(default=False)

    class Meta:
        unique_together = [
            ("user", "quiz"),
        ]
    def __str__(self):
        return str(self.user)
    
    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         # Object created
    #         if self.quiz.end_date - timezone.now() >= self.quiz.duration:
    #             self.end_time = timezone.now() + self.quiz.duration
    #         else:
    #             self.end_time = self.quiz.end_date - timezone.now()
    #     super().save(*args, **kwargs)

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