from django import forms
from judge.models import CodeSubmission

LANGUAGE_CHOICES = [
    ("py", "Python"),
    ("c", "C"),
    ("cpp", "C++"),
]

class CodeSubmissionForm(forms.ModelForm):
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    code = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control code-input'}))
    input_data = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control input-data', 'rows': 3}), required=False)

    class Meta:
        model = CodeSubmission
        fields = ["language", "code", "input_data"]