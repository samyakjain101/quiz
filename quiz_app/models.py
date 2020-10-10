import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    title = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.SmallIntegerField()

    def __str__(self):
        return self.question

class UQuiz(models.Model):
    user = models.models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.models.ForeignKey(Quiz, on_delete=models.CASCADE)
    # start = models.DateTimeField() #when he started quiz
    
    def __str__(self):
        return str(self.user + " attempt " + self.quiz)

class UAns(models.Model):
    uquiz = models.ForeignKey(UQuiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    myAns = models.SmallIntegerField()
    MARK_FOR_REVIEW = 1                
    DONT_MARK_FOR_REVIEW = 2   
    STATUS_CHOICES = (
        (MARK_FOR_REVIEW, 'Mark for review'),
        (DONT_MARK_FOR_REVIEW, 'Dont mark for review'),
    )
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0)
    

    def __str__(self):
        return str((self.user + " ans"))
