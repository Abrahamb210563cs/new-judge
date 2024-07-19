from django.db import models

# Create your models here.
class Question(models.Model):
    name=models.CharField(max_length=50)
    statement = models.TextField(default="No statement provided")

    def __str__(self):
        return self.name
    

from django.contrib.auth.models import User
from judge.models import Question

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    code = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

class TestCase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    input = models.TextField()
    expected_output = models.TextField()

    def __str__(self):
        return f"Test Case for {self.question.name}"
    


class CodeSubmission(models.Model):
    language = models.CharField(max_length=10)
    input_data = models.TextField(null=True, blank=True)
    output_data = models.TextField(null=True, blank=True)
    code = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    verdict = models.CharField(max_length=20, null=True, blank=True)