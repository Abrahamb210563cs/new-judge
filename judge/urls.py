from django.urls import path
from judge.views import all_questions, question_details

urlpatterns = [
    path('all/', all_questions, name='all_question'),
    path('all/<int:question_id>/', question_details, name='question_details'),
    
]
