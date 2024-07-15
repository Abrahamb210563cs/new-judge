from django.contrib import admin
from judge.models import Question, CodeSubmission, TestCase

admin.site.register(Question)
admin.site.register(CodeSubmission)
admin.site.register(TestCase)
